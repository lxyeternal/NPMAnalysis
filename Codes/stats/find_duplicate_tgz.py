import os
import glob
from collections import defaultdict

def find_tgz_files(directory):
    """递归查找目录中的所有tgz文件"""
    tgz_files = []
    # 遍历目录
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".tgz"):
                tgz_files.append(os.path.join(root, file))
    return tgz_files

def main():
    # 设置目录路径
    benign_folder = "/home2/wenbo/Documents/NPMAnalysis/Dataset/zip_benign"
    malware_folder = "/home2/wenbo/Documents/NPMAnalysis/Dataset/zip_malware"
    
    # 查找所有tgz文件
    print(f"正在查找良性样本目录: {benign_folder}")
    benign_tgz_files = find_tgz_files(benign_folder)
    print(f"找到 {len(benign_tgz_files)} 个tgz文件")
    
    print(f"正在查找恶意样本目录: {malware_folder}")
    malware_tgz_files = find_tgz_files(malware_folder)
    print(f"找到 {len(malware_tgz_files)} 个tgz文件")
    
    # 提取文件名
    benign_filenames = [(os.path.basename(f), f) for f in benign_tgz_files]
    malware_filenames = [(os.path.basename(f), f) for f in malware_tgz_files]
    
    # 查找重复文件
    benign_names = [name for name, _ in benign_filenames]
    malware_names = [name for name, _ in malware_filenames]
    duplicates = set(benign_names).intersection(set(malware_names))
    
    # 统计每个目录内部的重复文件
    benign_internal_dups = find_internal_duplicates(benign_filenames)
    malware_internal_dups = find_internal_duplicates(malware_filenames)
    
    # 输出结果
    print("\n===== 统计结果 =====")
    print(f"良性样本文件数: {len(benign_tgz_files)}")
    print(f"恶意样本文件数: {len(malware_tgz_files)}")
    
    print(f"\n在两个目录之间发现 {len(duplicates)} 个重名文件:")
    for dup in sorted(duplicates):
        print(f"  - {dup}")
    
    print(f"\n良性样本目录内部发现 {sum(len(files) for files in benign_internal_dups.values())} 个重名文件:")
    for filename, occurrences in sorted(benign_internal_dups.items(), key=lambda x: len(x[1]), reverse=True):
        if len(occurrences) > 1:
            print(f"  - {filename} (出现 {len(occurrences)} 次)")
            for path in occurrences[:5]:  # 只显示前5个路径
                print(f"    {path}")
            if len(occurrences) > 5:
                print(f"    ... 等 {len(occurrences) - 5} 个路径")
    
    print(f"\n恶意样本目录内部发现 {sum(len(files) for files in malware_internal_dups.values())} 个重名文件:")
    for filename, occurrences in sorted(malware_internal_dups.items(), key=lambda x: len(x[1]), reverse=True):
        if len(occurrences) > 1:
            print(f"  - {filename} (出现 {len(occurrences)} 次)")
            for path in occurrences[:5]:  # 只显示前5个路径
                print(f"    {path}")
            if len(occurrences) > 5:
                print(f"    ... 等 {len(occurrences) - 5} 个路径")
    
    # 将结果保存到文件
    with open("tgz_duplicates_report.txt", "w", encoding="utf-8") as f:
        f.write("TGZ文件重名统计报告\n")
        f.write("===================\n\n")
        
        f.write(f"良性样本文件数: {len(benign_tgz_files)}\n")
        f.write(f"恶意样本文件数: {len(malware_tgz_files)}\n\n")
        
        f.write(f"在两个目录之间发现 {len(duplicates)} 个重名文件:\n")
        for dup in sorted(duplicates):
            f.write(f"  - {dup}\n")
        
        f.write(f"\n良性样本目录内部发现 {sum(len(files) for files in benign_internal_dups.values())} 个重名文件:\n")
        for filename, occurrences in sorted(benign_internal_dups.items(), key=lambda x: len(x[1]), reverse=True):
            if len(occurrences) > 1:
                f.write(f"  - {filename} (出现 {len(occurrences)} 次)\n")
                for path in occurrences:
                    f.write(f"    {path}\n")
        
        f.write(f"\n恶意样本目录内部发现 {sum(len(files) for files in malware_internal_dups.values())} 个重名文件:\n")
        for filename, occurrences in sorted(malware_internal_dups.items(), key=lambda x: len(x[1]), reverse=True):
            if len(occurrences) > 1:
                f.write(f"  - {filename} (出现 {len(occurrences)} 次)\n")
                for path in occurrences:
                    f.write(f"    {path}\n")
    
    print(f"\n报告已保存到: tgz_duplicates_report.txt")

def find_internal_duplicates(filename_tuples):
    """找出文件名列表中的重复项及其路径"""
    filename_to_paths = defaultdict(list)
    
    for filename, path in filename_tuples:
        # 将完整路径添加到对应文件名的列表中
        filename_to_paths[filename].append(path)
    
    # 只保留有重复的文件名
    return {filename: paths for filename, paths in filename_to_paths.items() if len(paths) > 1}

if __name__ == "__main__":
    main() 