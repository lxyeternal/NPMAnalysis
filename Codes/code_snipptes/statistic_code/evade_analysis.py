#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @File     : evade_analysis.py
# @Project  : NPMAnalysis
# @Description：分析恶意代码片段并规范化其行为和规避技术

import sys
sys.path.append("/home2/wenbo/Documents/NPMAnalysis/Codes")
import os
import json
import copy
import hashlib
from typing import List, Dict, Set, Any, Tuple
from utils.llmquery import LLMAgent

class MalwareAnalyzer:
    def __init__(self, base_dir: str):
        """
        初始化恶意代码分析器
        
        Args:
            base_dir: 包含恶意代码片段的基础目录
        """
        self.base_dir = base_dir
        self.llm_agent = LLMAgent()
        self.known_behaviors: Set[str] = set()
        self.known_evasions: Set[str] = set()
        
        # 缓存已分析的恶意代码，避免重复分析
        # 格式: {代码哈希: (behavior_formal, evasion_formal)}
        self.analyzed_code_cache: Dict[str, Tuple[List[str], List[str]]] = {}
        
        # 分析统计
        self.total_snippets = 0
        self.analyzed_snippets = 0
        self.cached_snippets = 0
        self.skipped_snippets = 0
        
        # 初始化一些常见的行为和规避技术类别
        self._initialize_common_categories()
        
        # 预扫描所有JSON文件，收集已有的behavior_formal和evasion_formal
        self._prescan_all_json_files()
    
    def _initialize_common_categories(self):
        """初始化一些常见的行为和规避技术类别"""
        # 恶意行为分类 - 更加精确的分类
        common_behaviors = [
            # 数据相关
            "data_exfiltration",           # 数据外泄（主动发送数据到外部服务器）
            "sensitive_data_collection",   # 敏感数据收集（系统信息、用户信息等）
            "credential_theft",            # 凭证窃取（密码、token等）
            
            # 执行相关
            "remote_code_execution",       # 远程代码执行
            "arbitrary_command_execution", # 任意命令执行
            "malicious_download",          # 恶意下载（下载其他恶意组件）
            
            # 持久化相关
            "persistence_installation",    # 持久化安装（确保恶意代码持续运行）
            "backdoor_installation",       # 后门安装
            
            # 控制相关
            "command_and_control",         # 命令与控制（C2）
            "botnet_activity",             # 僵尸网络活动
            
            # 权限相关
            "privilege_escalation",        # 权限提升
            "unauthorized_access",         # 未授权访问
            
            # 其他
            "cryptocurrency_mining",       # 加密货币挖矿
            "denial_of_service",           # 拒绝服务
        ]
        
        # NPM特有的规避技术 - 更加具体的分类
        common_evasions = [
            # 代码混淆技术
            "string_obfuscation",          # 字符串混淆
            "base64_encoding",             # Base64编码
            "hex_encoding",                # 十六进制编码
            "code_splitting",              # 代码分割（将恶意代码分散在多个文件中）
            "dynamic_evaluation",          # 动态评估（eval, new Function等）
            
            # 检测规避
            "sandbox_detection",           # 沙箱检测
            "environment_detection",       # 环境检测（检测是否在开发环境中）
            "timing_based_evasion",        # 基于时间的规避（延迟执行）
            "conditional_execution",       # 条件执行（基于特定条件才执行恶意代码）
            
            # NPM特有技术
            "dependency_confusion",        # 依赖混淆攻击
            "typosquatting",               # 域名欺骗（包名相似）
            "install_script_abuse",        # 安装脚本滥用
            "postinstall_hook_abuse",      # postinstall钩子滥用
            "preinstall_hook_abuse",       # preinstall钩子滥用
            
            # API滥用
            "legitimate_api_abuse",        # 合法API滥用
            "built_in_module_abuse",       # 内置模块滥用
            "native_code_execution",       # 原生代码执行
            
            # 错误处理
            "silent_error_handling",       # 静默错误处理
            "error_suppression",           # 错误抑制
            
            # 网络技术
            "domain_generation",           # 域名生成
            "network_traffic_blending",    # 网络流量混合（伪装成正常流量）
            "encrypted_communication",     # 加密通信
        ]
        
        for behavior in common_behaviors:
            self.known_behaviors.add(behavior)
            
        for evasion in common_evasions:
            self.known_evasions.add(evasion)
    
    def _prescan_all_json_files(self):
        """
        预扫描所有JSON文件，收集已有的behavior_formal和evasion_formal
        这样即使程序中断重启，也能保持已知类别的连续性
        """
        print("预扫描所有JSON文件，收集已有的分类...")
        
        total_packages = 0
        scanned_packages = 0
        scanned_files = 0
        found_behaviors = 0
        found_evasions = 0
        
        # 获取包的总数
        for package_name in os.listdir(self.base_dir):
            package_path = os.path.join(self.base_dir, package_name)
            if os.path.isdir(package_path):
                total_packages += 1
        
        # 遍历所有包
        for package_name in os.listdir(self.base_dir):
            package_path = os.path.join(self.base_dir, package_name)
            if not os.path.isdir(package_path):
                continue
            
            scanned_packages += 1
            print(f"\r预扫描进度: [{scanned_packages}/{total_packages}] 包", end="")
            
            # 遍历所有版本
            for version in os.listdir(package_path):
                version_path = os.path.join(package_path, version)
                if not os.path.isdir(version_path):
                    continue
                
                json_path = os.path.join(version_path, "result.json")
                if not os.path.exists(json_path):
                    continue
                
                scanned_files += 1
                
                try:
                    with open(json_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    if "malicious_snippets" not in data:
                        continue
                    
                    for snippet in data["malicious_snippets"]:
                        # 检查是否已经有behavior_formal和evasion_formal
                        if "behavior_formal" in snippet and "evasion_formal" in snippet:
                            # 收集behavior_formal
                            if snippet["behavior_formal"]:
                                if isinstance(snippet["behavior_formal"], list):
                                    for behavior in snippet["behavior_formal"]:
                                        self.known_behaviors.add(behavior)
                                        found_behaviors += 1
                                else:
                                    self.known_behaviors.add(snippet["behavior_formal"])
                                    found_behaviors += 1
                            
                            # 收集evasion_formal
                            if snippet["evasion_formal"]:
                                if isinstance(snippet["evasion_formal"], list):
                                    for evasion in snippet["evasion_formal"]:
                                        self.known_evasions.add(evasion)
                                        found_evasions += 1
                                else:
                                    self.known_evasions.add(snippet["evasion_formal"])
                                    found_evasions += 1
                            
                            # 将已分析的代码添加到缓存
                            if "malicious_code" in snippet:
                                code_hash = self._get_code_hash(snippet["malicious_code"])
                                if code_hash not in self.analyzed_code_cache:
                                    self.analyzed_code_cache[code_hash] = (
                                        snippet["behavior_formal"] if isinstance(snippet["behavior_formal"], list) 
                                        else [snippet["behavior_formal"]],
                                        snippet["evasion_formal"] if isinstance(snippet["evasion_formal"], list)
                                        else [snippet["evasion_formal"]]
                                    )
                
                except Exception as e:
                    print(f"\n预扫描文件时出错 {json_path}: {e}")
        
        print(f"\n预扫描完成! 扫描了 {scanned_files} 个文件")
        print(f"发现 {found_behaviors} 个行为分类, {found_evasions} 个规避技术")
        print(f"已知行为分类: {len(self.known_behaviors)}")
        print(f"已知规避技术: {len(self.known_evasions)}")
        print(f"缓存大小: {len(self.analyzed_code_cache)} 个代码哈希")
        print("")
    
    def _get_code_hash(self, code: str) -> str:
        """
        计算代码的哈希值，用于缓存查找
        
        Args:
            code: 恶意代码
            
        Returns:
            str: 代码的MD5哈希值
        """
        return hashlib.md5(code.encode('utf-8')).hexdigest()
    
    def analyze_all_packages(self):
        """遍历所有包并分析其中的恶意代码片段"""
        for package_name in os.listdir(self.base_dir):
            package_path = os.path.join(self.base_dir, package_name)
            if not os.path.isdir(package_path):
                continue
                
            print(f"分析包: {package_name}")
            for version in os.listdir(package_path):
                version_path = os.path.join(package_path, version)
                if not os.path.isdir(version_path):
                    continue
                    
                json_path = os.path.join(version_path, "result.json")
                if os.path.exists(json_path):
                    self.analyze_package_json(json_path)
        
        # 打印分析统计
        print("\n分析统计:")
        print(f"总代码片段数: {self.total_snippets}")
        print(f"实际分析数: {self.analyzed_snippets}")
        print(f"缓存复用数: {self.cached_snippets}")
        print(f"跳过已分析数: {self.skipped_snippets}")
        print(f"缓存命中率: {self.cached_snippets / (self.analyzed_snippets + self.cached_snippets) * 100:.2f}%" if (self.analyzed_snippets + self.cached_snippets) > 0 else "0%")
    
    def analyze_package_json(self, json_path: str):
        """
        分析单个包的JSON文件
        
        Args:
            json_path: JSON文件的路径
        """
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if "malicious_snippets" not in data:
                print(f"警告: {json_path} 中没有 malicious_snippets 字段")
                return
            
            modified = False
            for snippet in data["malicious_snippets"]:
                self.total_snippets += 1
                
                if "malicious_code" not in snippet or "behavior_summary" not in snippet or "evasion_techniques" not in snippet:
                    continue
                
                # 如果已经分析过，则跳过
                if "behavior_formal" in snippet and "evasion_formal" in snippet:
                    self.skipped_snippets += 1
                    continue
                
                # 检查代码是否已经分析过（缓存中是否有）
                code_hash = self._get_code_hash(snippet["malicious_code"])
                if code_hash in self.analyzed_code_cache:
                    # 从缓存中获取结果
                    behavior_formal, evasion_formal = self.analyzed_code_cache[code_hash]
                    self.cached_snippets += 1
                    print(f"  使用缓存结果 (哈希: {code_hash[:8]}...)")
                else:
                    # 分析代码片段
                    behavior_formal, evasion_formal = self.analyze_snippet(
                        snippet["malicious_code"],
                        snippet["behavior_summary"],
                        snippet["evasion_techniques"]
                    )
                    self.analyzed_snippets += 1
                    
                    # 将结果添加到缓存
                    self.analyzed_code_cache[code_hash] = (behavior_formal, evasion_formal)
                
                # 更新片段
                snippet["behavior_formal"] = behavior_formal
                snippet["evasion_formal"] = evasion_formal
                modified = True
                
                # 更新已知行为和规避技术
                for behavior in behavior_formal:
                    self.known_behaviors.add(behavior)
                for evasion in evasion_formal:
                    self.known_evasions.add(evasion)
            
            # 如果有修改，则保存文件
            if modified:
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                print(f"已更新: {json_path}")
        
        except Exception as e:
            print(f"处理 {json_path} 时出错: {e}")
    
    def analyze_snippet(self, code: str, behavior_summary: str, evasion_techniques: str) -> Tuple[List[str], List[str]]:
        """
        使用LLM分析代码片段，规范化行为和规避技术
        
        Args:
            code: 恶意代码
            behavior_summary: 行为摘要
            evasion_techniques: 规避技术描述
            
        Returns:
            tuple: (behavior_formal, evasion_formal)
        """
        # 构建提示词
        prompt = self._build_prompt(code, behavior_summary, evasion_techniques)
        
        # 调用LLM
        messages = [
            {"role": "system", "content": "You are a security expert specializing in malware analysis, particularly focusing on NPM package malware."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.llm_agent.perform_query(
            messages=messages,
            temperature=0,
            seed=42,
            response_format={"type": "json_object"}
        )
        
        try:
            result = json.loads(response)
            behavior_formal = result.get("behavior_formal", [])
            evasion_formal = result.get("evasion_formal", [])
            
            # 确保behavior_formal和evasion_formal是列表
            if isinstance(behavior_formal, str):
                behavior_formal = [behavior_formal]
            if isinstance(evasion_formal, str):
                evasion_formal = [evasion_formal]
            
            return behavior_formal, evasion_formal
        
        except json.JSONDecodeError:
            print(f"LLM返回的不是有效JSON: {response}")
            return ["unknown"], ["unknown"]
    
    def _build_prompt(self, code: str, behavior_summary: str, evasion_techniques: str) -> str:
        """
        构建提示词
        
        Args:
            code: 恶意代码
            behavior_summary: 行为摘要
            evasion_techniques: 规避技术描述
            
        Returns:
            str: 提示词
        """
        known_behaviors_list = sorted(list(self.known_behaviors))
        known_evasions_list = sorted(list(self.known_evasions))
        
        # 构建已知行为和规避技术的展示
        behaviors_display = ""
        if known_behaviors_list:
            behaviors_display = "Known behavior categories:\n"
            for i, behavior in enumerate(known_behaviors_list):
                behaviors_display += f"- {behavior}\n"
        else:
            behaviors_display = "No existing behavior categories yet, please create new ones.\n"
            
        evasions_display = ""
        if known_evasions_list:
            evasions_display = "Known evasion techniques:\n"
            for i, evasion in enumerate(known_evasions_list):
                evasions_display += f"- {evasion}\n"
        else:
            evasions_display = "No existing evasion techniques yet, please create new ones.\n"
        
        prompt = f"""
Please analyze the following malicious code snippet from an NPM package, its behavior summary, and evasion techniques.

## Malicious Code:
```javascript
{code}
```

## Behavior Summary:
{behavior_summary}

## Evasion Techniques:
{evasion_techniques}

## Important Note:
If the Behavior Summary or Evasion Techniques sections above are empty, please analyze the code directly to determine:
- The malware's behavior and purpose (what it does)
- Any evasion techniques used (how it tries to hide or avoid detection)

Note that not all malicious code uses evasion techniques. If the code doesn't employ any evasion methods, you can return an empty list for evasion_formal.

Your task is to normalize the behavior and evasion techniques into standardized formal categories.

## Behavior Categories
{behaviors_display}
Behavior categories should precisely describe what the malware does (e.g., sensitive_data_collection is collecting system/user data, data_exfiltration is sending that data to external servers).

## Evasion Techniques
{evasions_display}
Evasion techniques should focus on specific methods used to avoid detection or analysis (e.g., base64_encoding, preinstall_hook_abuse, silent_error_handling).

## Examples

### Example 1:
Behavior Summary: "Collects system and user data, exfiltrates via HTTPS POST to remote server."
Evasion Techniques: "Uses standard modules, silent error handling, blends with legitimate network activity."

Response:
```json
{{
  "behavior_formal": ["sensitive_data_collection", "data_exfiltration"],
  "evasion_formal": ["built_in_module_abuse", "silent_error_handling", "network_traffic_blending"]
}}
```

### Example 2:
Behavior Summary: "Executes index.js automatically before install, enabling arbitrary code execution on package install."
Evasion Techniques: "Abuses npm preinstall hook; blends with legitimate scripts in package.json."

Response:
```json
{{
  "behavior_formal": ["arbitrary_command_execution", "persistence_installation"],
  "evasion_formal": ["preinstall_hook_abuse", "legitimate_api_abuse"]
}}
```

### Example 3:
Behavior Summary: "Downloads and executes additional malware components from remote server with base64 encoded URLs."
Evasion Techniques: "Uses base64 encoded strings, checks for sandbox environment, delays execution."

Response:
```json
{{
  "behavior_formal": ["malicious_download", "remote_code_execution"],
  "evasion_formal": ["base64_encoding", "sandbox_detection", "timing_based_evasion"]
}}
```

### Example 4:
Behavior Summary: "Simple keylogger that records keystrokes and saves them locally."
Evasion Techniques: ""

Response:
```json
{{
  "behavior_formal": ["sensitive_data_collection"],
  "evasion_formal": []
}}
```

Respond with a JSON object in this exact format:
{{
  "behavior_formal": ["category1", "category2", ...],
  "evasion_formal": ["technique1", "technique2", ...]
}}

Instructions:
1. For behavior_formal, identify ALL applicable behavior categories (at least one)
2. For evasion_formal, identify ALL applicable evasion techniques (can be empty if none are used)
3. Use concise, snake_case naming for all categories
4. Try to reuse existing categories when appropriate
5. Create new categories only when necessary and ensure they follow the same naming pattern
"""
        return prompt

def main():
    base_dir = "/home2/wenbo/Documents/NPMAnalysis/Codes/code_snipptes/malware_snippets"
    analyzer = MalwareAnalyzer(base_dir)
    analyzer.analyze_all_packages()
    
    print("\n分析完成!")
    print(f"识别到的行为类别 ({len(analyzer.known_behaviors)}):")
    for behavior in sorted(analyzer.known_behaviors):
        print(f"- {behavior}")
        
    print(f"\n识别到的规避技术 ({len(analyzer.known_evasions)}):")
    for evasion in sorted(analyzer.known_evasions):
        print(f"- {evasion}")

if __name__ == "__main__":
    main()