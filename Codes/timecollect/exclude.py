import csv
import os

def main():
    # 文件路径
    csv_file = "malware_time.csv"
    txt_file = "malware_benign.txt"
    output_file = "filtered_malware_time.csv"
    
    # 从txt文件读取需要排除的包版本
    exclude_set = set()
    with open(txt_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('//'):
                # 替换##为/以匹配csv中的格式
                line = line.replace('##', '/')
                exclude_set.add(line)
    
    # 读取CSV并写入新的CSV，排除在txt中出现的包版本
    with open(csv_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for row in reader:
            # 构建包版本的标识符，格式为 package_name/version
            package_version = f"{row['package_name']}/{row['version']}"
            
            # 如果该包版本不在排除列表中，则写入新文件
            if package_version not in exclude_set:
                writer.writerow(row)
    
    print(f"已过滤掉 {len(exclude_set)} 个包版本")
    print(f"结果已保存到 {output_file}")

if __name__ == "__main__":
    main()