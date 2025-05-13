#!/usr/bin/env python3
import os
import sys
import glob
import shutil
import subprocess
import time
from multiprocessing import Pool
from pathlib import Path

# 可以直接在这里修改的配置参数
# ====================================================
# 要使用的处理进程数
PROCESS_COUNT = 24
# 恶意样本目录
MALWARE_DIR = "/home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_malware"
# 良性样本目录
BENIGN_DIR = "/home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_benign"
# 输出根目录
OUTPUT_ROOT = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output/genie"
# 良性样本输出目录
BENIGN_OUTPUT_DIR = os.path.join(OUTPUT_ROOT, "benign")
# 恶意样本输出目录
MALWARE_OUTPUT_DIR = os.path.join(OUTPUT_ROOT, "malware")
# 是否分析恶意样本
ANALYZE_MALWARE = True
# 是否分析良性样本
ANALYZE_BENIGN = True
# 是否使用混淆检测查询
USE_OBFUSCATOR_QUERIES = True
# 扫描模式：逐个扫描(INDIVIDUAL)或批量扫描(BATCH)
SCAN_MODE = "BATCH"  # 可选值: "INDIVIDUAL" 或 "BATCH"
# ====================================================

# GENIE目录结构
GENIE_ROOT = "/home2/wenbo/Documents/NPMAnalysis/Tools/GENIE"
GENIE_SNAPSHOT = os.path.join(GENIE_ROOT, "snapshot")
GENIE_REGISTRY = os.path.join(GENIE_SNAPSHOT, "1_Registry/NPM")
GENIE_CODEBASE = os.path.join(GENIE_SNAPSHOT, "2_CodeBase/NPM")
GENIE_DATABASE = os.path.join(GENIE_SNAPSHOT, "3_DataBase/NPM")
GENIE_QUERY_OUTPUT = os.path.join(GENIE_SNAPSHOT, "4_query/output")
GENIE_MALWARE_QUERIES = os.path.join(GENIE_ROOT, "queries/malware")
GENIE_OBFUSCATOR_QUERIES = os.path.join(GENIE_ROOT, "queries/obfuscator")

# 初始化目录
def init_directories():
    """确保所有需要的目录都存在"""
    for directory in [GENIE_REGISTRY, GENIE_CODEBASE, GENIE_DATABASE, GENIE_QUERY_OUTPUT,
                      BENIGN_OUTPUT_DIR, MALWARE_OUTPUT_DIR]:
        os.makedirs(directory, exist_ok=True)

# 获取包版本的唯一标识符
def get_package_id(package_path):
    """根据包路径生成唯一ID (包名-版本)"""
    package_dir = os.path.basename(package_path)
    return package_dir

# 检查包是否已经分析过
def is_already_analyzed(package_path, is_malware):
    """检查包是否已经分析过"""
    package_id = get_package_id(package_path)
    output_dir = MALWARE_OUTPUT_DIR if is_malware else BENIGN_OUTPUT_DIR
    
    expected_output = os.path.join(output_dir, f"{package_id}.csv")
    return os.path.exists(expected_output)

# 处理单个包目录
def process_package(args):
    """处理单个包目录，执行完整的GENIE分析流程"""
    package_path, is_malware = args
    
    package_id = get_package_id(package_path)
    print(f"处理包: {package_id} ({'恶意' if is_malware else '良性'})")
    
    try:
        # 检查是否已分析
        if is_already_analyzed(package_path, is_malware):
            print(f"跳过已分析的包: {package_id}")
            return (package_id, True, "已分析，跳过")
        
        # 生成唯一的工作目录名，避免并行处理时的冲突
        unique_id = f"{package_id}_{int(time.time())}"
        
        # 1. 复制到CodeBase目录
        codebase_dir = os.path.join(GENIE_CODEBASE, unique_id)
        os.makedirs(codebase_dir, exist_ok=True)
        
        # 复制解压后的文件到CodeBase
        for item in os.listdir(package_path):
            s = os.path.join(package_path, item)
            d = os.path.join(codebase_dir, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)
        
        # 2. 创建CodeQL数据库
        database_dir = os.path.join(GENIE_DATABASE, unique_id)
        os.makedirs(database_dir, exist_ok=True)
        
        create_db_cmd = [
            'codeql', 'database', 'create',
            '--source-root=' + codebase_dir,
            '--language=javascript',
            '--verbosity=progress',
            database_dir
        ]
        
        db_process = subprocess.run(create_db_cmd, capture_output=True, text=True)
        if db_process.returncode != 0:
            print(f"为 {package_id} 创建数据库失败: {db_process.stderr}")
            # 清理工作目录
            shutil.rmtree(codebase_dir, ignore_errors=True)
            shutil.rmtree(database_dir, ignore_errors=True)
            return (package_id, False, "数据库创建失败")
        
        # 创建保存结果的合并文件
        merged_output_file = os.path.join(GENIE_QUERY_OUTPUT, f"{unique_id}-merged-results.csv")
        with open(merged_output_file, 'w') as merged_file:
            pass  # 创建空文件
        
        malware_detected = False
        obfuscation_detected = False
        detected_malware_types = []
        detected_obfuscator_types = []
        
        # 3. 根据扫描模式处理恶意代码查询
        if SCAN_MODE == "INDIVIDUAL":
            # 逐个扫描每个ql文件
            malware_queries = glob.glob(os.path.join(GENIE_MALWARE_QUERIES, "*.ql"))
            malware_successful_queries = 0
            total_malware_queries = len(malware_queries)
            
            print(f"  运行 {total_malware_queries} 个恶意代码查询...")
            
            # 运行每个恶意代码查询
            for query_file in malware_queries:
                query_name = os.path.basename(query_file).replace(".ql", "")
                query_output_file = os.path.join(GENIE_QUERY_OUTPUT, f"{unique_id}-{query_name}-results.csv")
                
                query_cmd = [
                    'codeql', 'database', 'analyze',
                    '--format=csv',
                    '--output=' + query_output_file,
                    database_dir,
                    query_file  # 单个查询文件
                ]
                
                try:
                    query_process = subprocess.run(query_cmd, capture_output=True, text=True)
                    
                    # 如果查询成功
                    if query_process.returncode == 0:
                        malware_successful_queries += 1
                        
                        # 检查是否检测到恶意代码
                        if os.path.exists(query_output_file) and os.path.getsize(query_output_file) > 0:
                            malware_detected = True
                            detected_malware_types.append(query_name)
                            
                            # 将恶意代码检测结果追加到合并文件
                            with open(query_output_file, 'r') as src, open(merged_output_file, 'a') as dest:
                                dest.write(f"# 查询: {query_name} (malware)\n")
                                dest.write(src.read())
                                dest.write("\n")
                    else:
                        print(f"  查询 {query_name} 失败: {query_process.stderr[:100]}...")
                except Exception as e:
                    print(f"  查询 {query_name} 执行异常: {str(e)}")
            
            print(f"  恶意代码查询完成: {malware_successful_queries}/{total_malware_queries} 成功")
            if detected_malware_types:
                print(f"  检测到恶意行为类型: {', '.join(detected_malware_types)}")
            
            # 4. 对每个混淆代码查询单独运行（如果启用）
            if USE_OBFUSCATOR_QUERIES:
                obfuscator_queries = glob.glob(os.path.join(GENIE_OBFUSCATOR_QUERIES, "*.ql"))
                obfuscator_successful_queries = 0
                total_obfuscator_queries = len(obfuscator_queries)
                
                print(f"  运行 {total_obfuscator_queries} 个混淆技术查询...")
                
                # 运行每个混淆代码查询
                for query_file in obfuscator_queries:
                    query_name = os.path.basename(query_file).replace(".ql", "")
                    query_output_file = os.path.join(GENIE_QUERY_OUTPUT, f"{unique_id}-{query_name}-results.csv")
                    
                    query_cmd = [
                        'codeql', 'database', 'analyze',
                        '--format=csv',
                        '--output=' + query_output_file,
                        database_dir,
                        query_file  # 单个查询文件
                    ]
                    
                    try:
                        query_process = subprocess.run(query_cmd, capture_output=True, text=True)
                        
                        # 如果查询成功
                        if query_process.returncode == 0:
                            obfuscator_successful_queries += 1
                            
                            # 检查是否检测到混淆技术
                            if os.path.exists(query_output_file) and os.path.getsize(query_output_file) > 0:
                                obfuscation_detected = True
                                detected_obfuscator_types.append(query_name)
                                
                                # 将混淆技术检测结果追加到合并文件
                                with open(query_output_file, 'r') as src, open(merged_output_file, 'a') as dest:
                                    dest.write(f"# 查询: {query_name} (obfuscator)\n")
                                    dest.write(src.read())
                                    dest.write("\n")
                        else:
                            print(f"  查询 {query_name} 失败: {query_process.stderr[:100]}...")
                    except Exception as e:
                        print(f"  查询 {query_name} 执行异常: {str(e)}")
                
                print(f"  混淆技术查询完成: {obfuscator_successful_queries}/{total_obfuscator_queries} 成功")
                if detected_obfuscator_types:
                    print(f"  检测到混淆技术类型: {', '.join(detected_obfuscator_types)}")
                    
            # 检查是否有成功的查询
            if malware_successful_queries == 0 and (not USE_OBFUSCATOR_QUERIES or obfuscator_successful_queries == 0):
                # 清理工作目录
                shutil.rmtree(codebase_dir, ignore_errors=True)
                shutil.rmtree(database_dir, ignore_errors=True)
                return (package_id, False, "所有查询都失败")
                
        else:  # SCAN_MODE == "BATCH"
            # 批量扫描整个目录
            print("  使用批量扫描模式...")
            
            # 3. 运行恶意代码查询
            malware_output_file = os.path.join(GENIE_QUERY_OUTPUT, f"{unique_id}-malware-results.csv")
            
            malware_analyze_cmd = [
                'codeql', 'database', 'analyze',
                '--format=csv',
                '--output=' + malware_output_file,
                database_dir,
                GENIE_MALWARE_QUERIES
            ]
            
            print("  运行恶意代码查询...")
            malware_process = subprocess.run(malware_analyze_cmd, capture_output=True, text=True)
            malware_success = malware_process.returncode == 0
            
            if malware_success:
                # 检查是否检测到恶意代码
                if os.path.exists(malware_output_file) and os.path.getsize(malware_output_file) > 0:
                    malware_detected = True
                    # 尝试从输出中提取查询名称
                    try:
                        with open(malware_output_file, 'r') as f:
                            first_line = f.readline().strip()
                            if first_line and len(first_line.split(',')) > 0:
                                query_name = first_line.split(',')[0].strip('"')
                                detected_malware_types.append(query_name)
                    except:
                        detected_malware_types.append("unknown-malware")
                    
                    # 将恶意代码检测结果追加到合并文件
                    with open(malware_output_file, 'r') as src, open(merged_output_file, 'a') as dest:
                        dest.write("# 批量恶意代码查询结果\n")
                        dest.write(src.read())
                        dest.write("\n")
                print("  恶意代码查询完成")
            else:
                print(f"  恶意代码分析失败: {malware_process.stderr[:100]}...")
            
            # 4. 运行混淆代码查询（如果启用）
            if USE_OBFUSCATOR_QUERIES:
                obfuscator_output_file = os.path.join(GENIE_QUERY_OUTPUT, f"{unique_id}-obfuscator-results.csv")
                
                obfuscator_analyze_cmd = [
                    'codeql', 'database', 'analyze',
                    '--format=csv',
                    '--output=' + obfuscator_output_file,
                    database_dir,
                    GENIE_OBFUSCATOR_QUERIES
                ]
                
                print("  运行混淆技术查询...")
                obfuscator_process = subprocess.run(obfuscator_analyze_cmd, capture_output=True, text=True)
                obfuscator_success = obfuscator_process.returncode == 0
                
                if obfuscator_success:
                    # 检查是否检测到混淆技术
                    if os.path.exists(obfuscator_output_file) and os.path.getsize(obfuscator_output_file) > 0:
                        obfuscation_detected = True
                        # 尝试从输出中提取查询名称
                        try:
                            with open(obfuscator_output_file, 'r') as f:
                                first_line = f.readline().strip()
                                if first_line and len(first_line.split(',')) > 0:
                                    query_name = first_line.split(',')[0].strip('"')
                                    detected_obfuscator_types.append(query_name)
                        except:
                            detected_obfuscator_types.append("unknown-obfuscator")
                        
                        # 将混淆技术检测结果追加到合并文件
                        with open(obfuscator_output_file, 'r') as src, open(merged_output_file, 'a') as dest:
                            dest.write("# 批量混淆技术查询结果\n")
                            dest.write(src.read())
                    print("  混淆技术查询完成")
                else:
                    print(f"  混淆技术分析失败: {obfuscator_process.stderr[:100]}...")
            
            # 检查是否有成功的查询
            if not malware_success and (USE_OBFUSCATOR_QUERIES and not obfuscator_success):
                # 清理工作目录
                shutil.rmtree(codebase_dir, ignore_errors=True)
                shutil.rmtree(database_dir, ignore_errors=True)
                return (package_id, False, "批量查询失败")
        
        # 6. 移动结果到最终目录
        output_dir = MALWARE_OUTPUT_DIR if is_malware else BENIGN_OUTPUT_DIR
        final_output_file = os.path.join(output_dir, f"{package_id}.csv")
        
        # 确保目标目录存在
        os.makedirs(os.path.dirname(final_output_file), exist_ok=True)
        
        # 复制合并结果文件到最终位置
        shutil.copy2(merged_output_file, final_output_file)
        
        # 7. 确定分析状态
        if malware_detected and obfuscation_detected:
            result_status = f"发现恶意代码({len(detected_malware_types)}种)和混淆技术({len(detected_obfuscator_types)}种)"
        elif malware_detected:
            result_status = f"发现恶意代码({len(detected_malware_types)}种)"
        elif obfuscation_detected:
            result_status = f"发现混淆技术({len(detected_obfuscator_types)}种)"
        else:
            result_status = "未发现恶意代码或混淆技术"
        
        # 8. 清理工作目录
        shutil.rmtree(codebase_dir, ignore_errors=True)
        shutil.rmtree(database_dir, ignore_errors=True)
        
        return (package_id, True, result_status, detected_malware_types, detected_obfuscator_types)
            
    except Exception as e:
        print(f"处理 {package_id} 时发生错误: {str(e)}")
        return (package_id, False, f"错误: {str(e)}")

def collect_packages():
    """收集所有需要分析的包目录"""
    packages = []
    
    if ANALYZE_MALWARE:
        for package_dir in sorted(glob.glob(os.path.join(MALWARE_DIR, "*"))):
            if os.path.isdir(package_dir):
                packages.append((package_dir, True))  # True表示恶意样本
    
    if ANALYZE_BENIGN:
        for package_dir in sorted(glob.glob(os.path.join(BENIGN_DIR, "*"))):
            if os.path.isdir(package_dir):
                packages.append((package_dir, False))  # False表示良性样本
    
    return packages

def main():
    # 初始化目录
    init_directories()
    
    # 收集包
    all_packages = collect_packages()
    
    # 过滤掉已分析的包
    packages_to_analyze = []
    skipped_packages = []
    
    for package_info in all_packages:
        package_path, is_malware = package_info
        if is_already_analyzed(package_path, is_malware):
            skipped_packages.append((get_package_id(package_path), is_malware))
        else:
            packages_to_analyze.append(package_info)
    
    if not packages_to_analyze:
        print("所有包都已经分析过，没有需要分析的新包")
        return
    
    print(f"总共找到 {len(all_packages)} 个包")
    print(f"跳过已分析的 {len(skipped_packages)} 个包")
    print(f"需要分析 {len(packages_to_analyze)} 个包")
    print(f"使用 {PROCESS_COUNT} 个进程进行分析")
    print(f"使用混淆检测查询: {'是' if USE_OBFUSCATOR_QUERIES else '否'}")
    print(f"扫描模式: {'逐个扫描' if SCAN_MODE == 'INDIVIDUAL' else '批量扫描'}")
    
    for i, (package_id, is_malware) in enumerate(skipped_packages[:10]):  # 只显示前10个
        print(f"  跳过: {package_id} ({'恶意' if is_malware else '良性'})")
    if len(skipped_packages) > 10:
        print(f"  ...以及 {len(skipped_packages) - 10} 个更多包")
    
    for i, (package_path, is_malware) in enumerate(packages_to_analyze[:10]):  # 只显示前10个
        print(f"  分析: {get_package_id(package_path)} ({'恶意' if is_malware else '良性'})")
    if len(packages_to_analyze) > 10:
        print(f"  ...以及 {len(packages_to_analyze) - 10} 个更多包")
    
    # 使用进程池处理文件
    start_time = time.time()
    with Pool(processes=PROCESS_COUNT) as pool:
        results = pool.map(process_package, packages_to_analyze)
    
    # 统计结果
    successful = sum(1 for r in results if r[1])
    malicious = sum(1 for r in results if r[1] and "发现恶意代码" in r[2])
    obfuscated = sum(1 for r in results if r[1] and "发现混淆技术" in r[2])
    
    # 统计各类恶意行为和混淆技术的检测次数
    malware_type_counts = {}
    obfuscator_type_counts = {}
    
    for r in results:
        if r[1]:  # 如果成功
            if len(r) > 3:  # 如果包含恶意类型信息
                # 统计恶意代码类型
                if len(r) > 3 and r[3]:
                    for malware_type in r[3]:
                        malware_type_counts[malware_type] = malware_type_counts.get(malware_type, 0) + 1
                
                # 统计混淆技术类型
                if len(r) > 4 and r[4]:
                    for obfuscator_type in r[4]:
                        obfuscator_type_counts[obfuscator_type] = obfuscator_type_counts.get(obfuscator_type, 0) + 1
    
    print(f"\n分析完成: 总计 {len(results)} 个包")
    print(f"成功: {successful}, 失败: {len(results) - successful}")
    print(f"检测到恶意包: {malicious}")
    
    # 显示恶意代码类型统计
    if malware_type_counts:
        print("\n恶意代码类型统计:")
        for malware_type, count in sorted(malware_type_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {malware_type}: {count} 个包")
    
    # 显示混淆技术类型统计
    if USE_OBFUSCATOR_QUERIES and obfuscator_type_counts:
        print("\n混淆技术类型统计:")
        for obfuscator_type, count in sorted(obfuscator_type_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"  {obfuscator_type}: {count} 个包")
    
    print(f"\n总耗时: {time.time() - start_time:.2f} 秒")

if __name__ == "__main__":
    main()