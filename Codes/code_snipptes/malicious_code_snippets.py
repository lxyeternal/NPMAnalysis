import os
import json
import re
from pathlib import Path
import sys
import hashlib
from collections import defaultdict
import multiprocessing
from functools import partial
import time
# 将项目根目录添加到路径中，这样可以正确导入utils模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Codes.utils.llmquery import LLMAgent

# 定义路径
SOURCE_DIR = "/home2/wenbo/Documents/NPMAnalysis/Codes/tool_detect/tool_output/guarddog/malware"
TARGET_DIR = "/home2/wenbo/Documents/NPMAnalysis/Codes/code_snipptes/malware_snippets"
PROMPT_PATH = "/home2/wenbo/Documents/NPMAnalysis/Prompts/single_snippets_prompt.txt"

# 设置进程数
NUM_PROCESSES = 24  # 可以根据CPU核心数调整

def normalize_code(code_snippet):
    """标准化代码片段，移除可能的变化（如变量名、空格等）"""
    # 移除所有空白字符
    normalized = re.sub(r'\s+', '', code_snippet)
    # 转为小写
    normalized = normalized.lower()
    return normalized

def hash_code(code_snippet):
    """对代码片段生成哈希值，用于比较相似性"""
    normalized = normalize_code(code_snippet)
    return hashlib.md5(normalized.encode()).hexdigest()

def extract_malicious_locations(txt_content):
    """
    从报告中提取所有恶意代码的位置信息
    返回格式：{文件路径：[位置1信息, 位置2信息, ...]}
    同时返回匹配的数量
    """
    # 提取压缩包路径
    archive_pattern = r'Found \d+ potentially malicious indicators in (.*?)(\.tar\.gz|\.zip|\.tgz|\.whl)'
    archive_match = re.search(archive_pattern, txt_content)
    
    if not archive_match:
        print("警告: 无法提取压缩包路径")
        return None, 0, None
    
    # 完整的压缩包路径
    zip_path = archive_match.group(1) + archive_match.group(2)
    print(f"提取的压缩包路径: {zip_path}")
    
    # 构建解压后的基础目录路径 - 只替换zip_malware为unzip_malware
    unzip_base_path = zip_path.replace('zip_malware', 'unzip_malware')
    
    # 提取到版本目录的路径（去掉压缩包文件名）
    # 例如: /home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_malware/@abdallaeg##sap_access/0.0.0/
    unzip_dir = os.path.dirname(unzip_base_path)
    print(f"解压后的目录路径: {unzip_dir}")
    
    # 分割报告内容为行，便于处理
    lines = txt_content.split('\n')
    
    # 查找所有类型描述行和文件位置
    malicious_locations = {}
    current_type = ""
    match_count = 0
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # 匹配类型描述行（如：cmd-overwrite: found 1 source code matches）
        type_match = re.match(r'^([\w\-]+): found (\d+) .* matches', line)
        if type_match:
            current_type = type_match.group(1)
            match_count_str = type_match.group(2)
            try:
                match_count += int(match_count_str)
            except ValueError:
                pass
            print(f"找到类型描述: {current_type}")
            i += 1
            continue
        
        # 匹配文件位置行
        # 格式可能是: "* ... at package/file.py:21" 或 "* ... at package.json:8"
        location_match = re.search(r'\*.*?\s+at\s+([\w\-\.\/]+(?:\.js|\.json|\.py|\.ts)):(\d+)', line)
        if location_match and current_type:
            relative_path = location_match.group(1)
            line_number = location_match.group(2)
            
            print(f"找到文件位置: {relative_path}:{line_number}")
            
            # 构建本地文件路径 - 直接拼接版本目录和相对路径
            full_path = os.path.join(unzip_dir, relative_path)
            
            # 提取代码片段（可能有多行）
            code_lines = []
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                # 如果下一行是空行或者以*开始，说明代码片段结束
                if not next_line or next_line.startswith('*') or re.match(r'^[\w\-]+: found \d+ .* matches', next_line):
                    break
                # 删除开头的空格和制表符等缩进
                code_line = next_line
                code_lines.append(code_line)
                j += 1
            
            # 完整代码片段
            code_snippet = '\n'.join(code_lines)
            
            # 组合信息
            location_info = {
                'line_number': line_number,
                'type': current_type,
                'code_snippet': code_snippet,
                'full_match': line,
                'full_path': full_path,
                'relative_path': relative_path
            }
            
            # 将信息添加到对应文件路径下
            if full_path not in malicious_locations:
                malicious_locations[full_path] = []
                print(f"添加新的文件路径: {full_path}")
            
            malicious_locations[full_path].append(location_info)
            
            # 更新索引
            i = j
            continue
        
        i += 1
    
    if not malicious_locations:
        print("警告: 未找到任何恶意代码位置")
    else:
        print(f"共找到 {len(malicious_locations)} 个文件的恶意代码位置")
    
    return malicious_locations, match_count, unzip_dir

def read_source_code(file_path):
    """读取源代码文件内容"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"读取文件 {file_path} 时出错: {e}")
        return None

def process_with_llm(code_content, detection_info, prompt_template):
    """
    使用LLM处理代码内容
    
    Args:
        code_content: 源代码内容
        detection_info: 检测信息
        prompt_template: 提示模板路径
    """
    try:
        # 从模板中读取prompt
        with open(prompt_template, 'r', encoding='utf-8') as f:
            prompt = f.read()
        
        # 准备代码和检测信息
        full_code = code_content
        
        # 添加检测信息到提示中，更清晰地标记问题行
        detection_context = "Detection information:\n"
        detection_context += f"- Line {detection_info['line_number']}: {detection_info['type']} found in file {detection_info['relative_path']}\n"
        detection_context += f"  Flagged code: {detection_info['code_snippet']}\n"
        
        # 替换模板中的代码部分，添加检测信息
        code_with_context = f"{detection_context}\nSource code:\n{full_code}"
        prompt = prompt.replace("{CODE}", code_with_context)
        
        # 创建LLM代理
        llm_agent = LLMAgent()
        
        # 准备消息
        messages = [
            {"role": "system", "content": "You are an expert malware code analyst."},
            {"role": "user", "content": prompt}
        ]
        
        # 获取LLM响应
        response = llm_agent.perform_query(messages)
        
        # 尝试解析JSON响应
        try:
            # 尝试从文本中提取JSON（如果LLM返回了额外文本）
            json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
            if json_match:
                extracted_context = json.loads(json_match.group(1))
            else:
                extracted_context = json.loads(response)
            
            return extracted_context
        except json.JSONDecodeError as e:
            print(f"无法解析LLM返回的JSON: {e}")
            print(f"原始响应: {response}")
            return None
        
    except Exception as e:
        print(f"LLM处理失败: {e}")
        return None

def process_package(package_name, version, txt_path):
    """处理单个包的恶意代码检测"""
    try:
        # 读取报告内容
        with open(txt_path, 'r', encoding='utf-8', errors='ignore') as f:
            txt_content = f.read()
        
        # 检查是否为良性代码
        if is_benign(txt_content):
            print(f"{package_name}/{version} 没有恶意代码，跳过")
            return None
        
        # 提取所有恶意代码位置
        malicious_locations, match_count, unzip_dir = extract_malicious_locations(txt_content)
        
        if not malicious_locations or match_count == 0:
            print(f"{package_name}/{version} 未找到恶意代码位置，跳过")
            return None
        
        print(f"{package_name}/{version} 找到 {match_count} 个恶意代码匹配")
        
        # 准备结果
        result = []
        
        # 处理每个文件的每个恶意代码位置
        for file_path, locations in malicious_locations.items():
            # 读取源代码
            code_content = read_source_code(file_path)
            if not code_content:
                print(f"无法读取源代码: {file_path}")
                continue
            
            # 处理文件中的每个恶意代码位置
            for location in locations:
                # 使用LLM处理代码
                print(f"使用LLM分析代码: {file_path}, 行 {location['line_number']}, 类型 {location['type']}")
                llm_result = process_with_llm(code_content, location, PROMPT_PATH)
                
                if not llm_result:
                    print(f"LLM处理失败: {file_path}")
                    continue
                
                # 提取恶意代码上下文和分析
                malicious_code = llm_result.get("malicious_code", "")
                behavior_summary = llm_result.get("behavior_summary", "")
                evasion_techniques = llm_result.get("evasion_techniques", "")
                
                # 如果LLM认为不是恶意代码，跳过
                if not malicious_code.strip():
                    print(f"LLM判断 {file_path} 行 {location['line_number']} 不包含恶意代码，跳过")
                    continue
                
                # 文件名（去掉路径）
                file_name = os.path.basename(file_path)
                
                # 创建符合要求格式的条目
                malicious_entry = {
                    "file": location['relative_path'],
                    "line_number": location['line_number'],
                    "type": location['type'],
                    "malicious_code": malicious_code,
                    "behavior_summary": behavior_summary,
                    "evasion_techniques": evasion_techniques,
                    "hash_value": hash_code(malicious_code)
                }
                
                # 添加到结果
                result.append(malicious_entry)
        
        if not result:
            print(f"{package_name}/{version} 未找到有效的恶意代码，跳过")
            return None
        
        # 添加元数据
        metadata = {
            "package_name": package_name,
            "version": version,
            "report_path": txt_path,
            "match_count": match_count,
            "unzip_dir": unzip_dir
        }
        
        # 最终结果
        final_result = {
            "metadata": metadata,
            "malicious_snippets": result
        }
        
        # 创建目标目录
        target_package_dir = os.path.join(TARGET_DIR, package_name)
        target_version_dir = os.path.join(target_package_dir, version)
        os.makedirs(target_version_dir, exist_ok=True)
        
        # 保存结果
        json_path = os.path.join(target_version_dir, "result.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(final_result, f, ensure_ascii=False, indent=2)
        
        print(f"已保存结果: {json_path}")
        return True
        
    except Exception as e:
        print(f"处理包 {package_name}/{version} 时出错: {e}")
        return None

def is_benign(txt_content):
    """判断报告是否表明代码是良性的（没有恶意代码）"""
    # 检查是否包含 "Found 0 potentially malicious indicators" 或 "benign"
    if "Found 0 potentially malicious indicators" in txt_content or "benign" in txt_content.lower():
        return True
    return False

def process_single_package(package_info):
    """处理单个包，用于多进程调用"""
    package_name, version, txt_path = package_info
    print(f"\n进程 {os.getpid()} 处理: {package_name}/{version}")
    return process_package(package_name, version, txt_path)

def collect_package_info():
    """收集所有需要处理的包信息"""
    package_info_list = []
    
    # 遍历源目录
    for package_name in os.listdir(SOURCE_DIR):
        package_dir = os.path.join(SOURCE_DIR, package_name)
        if not os.path.isdir(package_dir):
            continue
        
        # 遍历版本目录
        for version in os.listdir(package_dir):
            version_dir = os.path.join(package_dir, version)
            if not os.path.isdir(version_dir):
                continue
            
            # 检查result.txt是否存在
            txt_path = os.path.join(version_dir, "result.txt")
            if not os.path.exists(txt_path):
                continue
            
            # 检查是否已经处理过
            target_package_dir = os.path.join(TARGET_DIR, package_name)
            target_version_dir = os.path.join(target_package_dir, version)
            json_path = os.path.join(target_version_dir, "result.json")
            
            if os.path.exists(json_path):
                print(f"跳过已处理的包: {package_name}/{version}")
                continue
            
            package_info_list.append((package_name, version, txt_path))
    
    return package_info_list

def main():
    """主函数，使用多进程处理所有报告文件"""
    start_time = time.time()
    
    # 确保目标目录存在
    os.makedirs(TARGET_DIR, exist_ok=True)
    
    # 收集所有需要处理的包信息
    package_info_list = collect_package_info()
    print(f"找到 {len(package_info_list)} 个待处理的包")
    
    # 如果没有包需要处理，直接返回
    if not package_info_list:
        print("没有需要处理的包，退出")
        return
    
    # 创建进程池
    print(f"创建 {NUM_PROCESSES} 个进程的进程池")
    with multiprocessing.Pool(processes=NUM_PROCESSES) as pool:
        # 使用进程池处理所有包
        results = pool.map(process_single_package, package_info_list)
    
    # 统计处理结果
    processed = sum(1 for r in results if r is not None)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"\n处理完成: 成功处理 {processed} 个包，共 {len(package_info_list)} 个包")
    print(f"总耗时: {elapsed_time:.2f} 秒")

if __name__ == "__main__":
    main() 