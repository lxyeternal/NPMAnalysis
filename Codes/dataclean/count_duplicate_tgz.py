#!/usr/bin/env python3
import os
import hashlib
import glob
from collections import defaultdict

# 定义目标目录
target_dir = '/home2/mynames/Documents/NPMAnalysis/Dataset/zip_malware'

# 用于存储文件名和哈希值的字典
file_hash_dict = defaultdict(list)
# 用于存储哈希值和文件的字典 (内容相同的文件)
hash_file_dict = defaultdict(list)

# 用于存储重复文件的计数
same_name_count = 0
same_name_same_hash_count = 0
same_hash_diff_name_count = 0
total_version_folders = 0
total_tgz_files = 0

# 获取所有包文件夹
package_folders = [f for f in os.listdir(target_dir) if os.path.isdir(os.path.join(target_dir, f))]

print(f"总共找到 {len(package_folders)} 个包文件夹")

# 遍历每个包文件夹
for package_folder in package_folders:
    package_path = os.path.join(target_dir, package_folder)
    
    # 获取所有版本文件夹
    version_folders = [f for f in os.listdir(package_path) if os.path.isdir(os.path.join(package_path, f))]
    total_version_folders += len(version_folders)
    
    # 遍历每个版本文件夹
    for version_folder in version_folders:
        version_path = os.path.join(package_path, version_folder)
        
        # 查找该版本文件夹下的所有tgz文件
        tgz_files = glob.glob(os.path.join(version_path, '*.tgz'))
        total_tgz_files += len(tgz_files)
        
        # 如果有tgz文件
        for tgz_file in tgz_files:
            file_name = os.path.basename(tgz_file)
            
            # 计算文件的哈希值
            with open(tgz_file, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            
            # 将文件名和哈希值存储到字典中
            file_hash_dict[file_name].append({
                'path': tgz_file,
                'hash': file_hash
            })
            
            # 将文件按哈希值分组
            hash_file_dict[file_hash].append({
                'path': tgz_file,
                'name': file_name
            })

print(f"总共找到 {total_version_folders} 个版本文件夹")
print(f"总共找到 {total_tgz_files} 个tgz文件")

# 分析重复文件(按文件名分组)
print("\n1. 按文件名分组，查找相同文件名且哈希值相同的文件：")
for file_name, occurrences in file_hash_dict.items():
    if len(occurrences) > 1:
        same_name_count += 1
        
        # 检查是否有相同哈希值的文件
        hashes = [item['hash'] for item in occurrences]
        unique_hashes = set(hashes)
        
        if len(unique_hashes) < len(occurrences):
            same_name_same_hash_count += 1
            print(f"文件名: {file_name}, 出现次数: {len(occurrences)}, 不同哈希值数量: {len(unique_hashes)}")
            
            # 打印相同哈希值的文件路径
            hash_to_paths = defaultdict(list)
            for item in occurrences:
                hash_to_paths[item['hash']].append(item['path'])
            
            for hash_value, paths in hash_to_paths.items():
                if len(paths) > 1:
                    print(f"  哈希值: {hash_value}")
                    for path in paths:
                        print(f"    - {path}")

# 分析重复文件(按哈希值分组)
print("\n2. 按哈希值分组，查找内容相同但文件名不同的文件：")
same_hash_groups = []

for file_hash, occurrences in hash_file_dict.items():
    if len(occurrences) > 1:
        # 检查是否有不同文件名
        names = [item['name'] for item in occurrences]
        unique_names = set(names)
        
        if len(unique_names) > 1:
            same_hash_diff_name_count += 1
            same_hash_groups.append({
                'hash': file_hash,
                'files': occurrences,
                'unique_names': len(unique_names)
            })

# 按不同文件名数量排序
same_hash_groups.sort(key=lambda x: x['unique_names'], reverse=True)

# 打印前10个有最多不同文件名的哈希组
for i, group in enumerate(same_hash_groups[:10]):
    print(f"\n哈希值 {i+1}: {group['hash']}")
    print(f"  内容相同的文件数量: {len(group['files'])}")
    print(f"  不同文件名数量: {group['unique_names']}")
    print("  文件列表:")
    for file_info in group['files'][:5]:  # 只显示前5个文件
        print(f"    - {file_info['name']} ({file_info['path']})")
    if len(group['files']) > 5:
        print(f"    ... 等共{len(group['files'])}个文件")

print(f"\n总结:")
print(f"1. 同名的tgz文件数量: {same_name_count}")
print(f"2. 同名且哈希值相同的tgz文件数量: {same_name_same_hash_count}")
print(f"3. 哈希值相同但文件名不同的组数: {same_hash_diff_name_count}") 