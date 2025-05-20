import pandas as pd
import re
from datetime import datetime

# 读取CSV文件
df = pd.read_csv('filtered_malware_time.csv')

# 获取最后一列的列名
last_column = df.columns[-1]

# 创建一个函数来提取年份
def extract_year(time_str):
    if pd.isna(time_str) or time_str == '':
        return None
    
    try:
        # 尝试匹配不同的时间格式
        # 匹配 2020-01-01 格式
        match = re.search(r'(\d{4})-\d{2}-\d{2}', str(time_str))
        if match:
            return int(match.group(1))
        
        # 匹配 01/01/2020 格式
        match = re.search(r'\d{1,2}/\d{1,2}/(\d{4})', str(time_str))
        if match:
            return int(match.group(1))
        
        # 如果是时间戳格式
        if str(time_str).isdigit() and len(str(time_str)) >= 10:
            timestamp = int(str(time_str)[:10])  # 取前10位作为时间戳
            try:
                return datetime.fromtimestamp(timestamp).year
            except:
                pass
        
        return None
    except:
        return None

# 应用函数提取年份
df['year'] = df[last_column].apply(extract_year)

# 统计有时间的行数
rows_with_time = df[~pd.isna(df['year'])].shape[0]

# 统计每年的数量
year_counts = df['year'].value_counts().sort_index()

# 输出结果
print(f"有时间数据的行数: {rows_with_time}")
print("\n各年份数据统计:")
for year, count in year_counts.items():
    if not pd.isna(year):  # 排除NaN值
        percentage = (count / rows_with_time) * 100
        print(f"{int(year)}年: {count}个版本 ({percentage:.2f}%)")

# 无法识别时间格式的行数
no_time_rows = df.shape[0] - rows_with_time
print(f"\n无法识别时间格式的行数: {no_time_rows}")

# 计算总体覆盖率
coverage_rate = (rows_with_time / df.shape[0]) * 100
print(f"时间数据覆盖率: {coverage_rate:.2f}%")