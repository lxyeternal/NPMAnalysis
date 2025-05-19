import pandas as pd
import requests
import json
import time
import re
from datetime import datetime
from collections import Counter
import sys

BATCH_SIZE = 50

#df = pd.read_csv('test.csv')
df = pd.read_csv('malware_packages2.csv') 
total_rows = len(df)

# 初始化timestamp列为对象类型，而不是默认的数值类型
df['timestamp'] = None  # 这会创建一个对象类型的列，可以存储字符串

base_url = "https://registry.npmjs.org/"

# 用于统计的变量
year_counts = Counter()
failed_count = 0
processed_count = 0

# 批量保存函数
def save_batch(dataframe, batch_num):
    temp_file = f'malware_time_batch_2{batch_num}.csv'
    dataframe.to_csv(temp_file, index=False)
    print(f"已保存批次 {batch_num} 到 {temp_file}")

# 显示进度
def show_progress(current, total):
    progress = current / total * 100
    sys.stdout.write(f"\r处理进度: [{current}/{total}] {progress:.2f}% 完成")
    sys.stdout.flush()

# 遍历CSV中的每一行
for index, row in df.iterrows():
    package_name = row['package_name'] 
    version = row['version']  
    
    url = base_url + package_name
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            package_data = response.json()
            if 'time' in package_data:
                # 尝试直接匹配版本
                if version in package_data['time']:
                    # 直接存储时间戳字符串
                    timestamp_str = package_data['time'][version]
                    df.at[index, 'timestamp'] = timestamp_str
                    
                    # 统计年份
                    try:
                        year = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00')).year
                        year_counts[year] += 1
                    except ValueError:
                        print(f"Invalid timestamp format: {timestamp_str}")
                else:
                    # 处理特殊情况：找到任何 security 版本
                    security_versions = []
                    
                    for ver in package_data['time']:
                        if ver != 'created' and ver != 'modified' and ver != 'unpublished':
                            if '-security.' in ver:
                                # 提取 security 后面的数字
                                match = re.search(r'-security\.(\d+)$', ver)
                                if match:
                                    security_num = int(match.group(1))
                                    security_versions.append((ver, security_num))
                    
                    # 如果找到了安全版本，选择编号最大的
                    if security_versions:
                        print(f"Found security variants for {package_name}: {security_versions}")
                        security_versions.sort(key=lambda x: x[1], reverse=True)  # 按安全补丁编号排序
                        best_match = security_versions[0][0]
                        timestamp_str = package_data['time'][best_match]
                        df.at[index, 'timestamp'] = timestamp_str
                        print(f"Version {version} not found directly, using {best_match} instead for package {package_name}")
                        
                        # 统计年份
                        try:
                            year = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00')).year
                            year_counts[year] += 1
                        except ValueError:
                            print(f"Invalid timestamp format: {timestamp_str}")
                    else:
                        # 尝试找到最接近的版本号
                        available_versions = [v for v in package_data['time'] if v not in ['created', 'modified' , 'unpublished']]
                        if available_versions:
                            # 简单方案：选择版本列表中的最后一个(通常是最新版本)
                            closest_version = available_versions[-1]
                            timestamp_str = package_data['time'][closest_version]
                            df.at[index, 'timestamp'] = timestamp_str
                            print(f"Version {version} not found, using closest version {closest_version} for package {package_name}")
                            
                            # 统计年份
                            try:
                                year = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00')).year
                                year_counts[year] += 1
                            except ValueError:
                                print(f"Invalid timestamp format: {timestamp_str}")
                        else:
                            # 真的找不到任何可用版本
                            print(f"Version {version} and no alternatives found for package {package_name}")
                            failed_count += 1
            else:
                print(f"No time data found for package {package_name}")
                failed_count += 1
        else:
            print(f"Failed to get data for package {package_name}, status code: {response.status_code}")
            failed_count += 1
    except Exception as e:
        print(f"Error processing package {package_name}: {str(e)}")
        failed_count += 1
    # 更新处理计数
    processed_count += 1
    
    # 显示进度
    show_progress(processed_count, total_rows)
    
    # 每处理BATCH_SIZE个条目，保存一次结果
    if processed_count % BATCH_SIZE == 0:
        save_batch(df[:processed_count], processed_count // BATCH_SIZE)
  
    # 添加延迟以避免API请求过于频繁
    time.sleep(1)

# 保存最后的批次
if processed_count % BATCH_SIZE != 0:
    save_batch(df, (processed_count // BATCH_SIZE) + 1)

# 合并所有批次并保存最终结果
df.to_csv('malware_time_final.csv', index=False)
print("\n已保存所有数据到 malware_time_final.csv")

# 输出统计结果
print("\n=== 统计结果 ===")
print(f"总包数量: {len(df)}")
print(f"未能获取时间戳的包数量: {failed_count}")
print(f"成功获取时间戳的包数量: {len(df) - failed_count}")
print("\n按年份分布:")
for year in sorted(year_counts.keys()):
    print(f"{year}年: {year_counts[year]}个包")

# 计算百分比
if len(df) > 0:
    success_rate = (len(df) - failed_count) / len(df) * 100
    print(f"\n成功率: {success_rate:.2f}%")