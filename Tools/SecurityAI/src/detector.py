import json
import logging
from pathlib import Path
import openai
import time
from typing import List, Dict, Any

class SocketAIDetector:
    def __init__(self, config):
        self.config = config
        self.openai_client = openai.OpenAI(api_key=config.OPENAI_API_KEY)
        
        # 加载提示词
        self.prompts = self._load_prompts()
        
    def _load_prompts(self):
        """加载所有提示词"""
        prompts = {}
        prompt_dir = Path("prompts")
        
        # 加载系统提示词
        system_prompts_dir = prompt_dir / "system_prompts"
        prompts["initial_report"] = self._read_prompt_file(system_prompts_dir / "initial_report.txt")
        prompts["critical_review"] = self._read_prompt_file(system_prompts_dir / "critical_review.txt")
        prompts["final_report"] = self._read_prompt_file(system_prompts_dir / "final_report.txt")
        
        # 加载用户提示词
        user_prompts_dir = prompt_dir / "user_prompts"
        prompts["code_analysis"] = self._read_prompt_file(user_prompts_dir / "code_analysis.txt")
        
        return prompts
    
    def _read_prompt_file(self, file_path):
        """读取提示词文件"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except Exception as e:
            logging.error(f"Error reading prompt file {file_path}: {str(e)}")
            return ""
    
    def analyze_file(self, file_path):
        """分析单个JavaScript文件"""
        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as f:
                code_content = f.read()
            
            # 如果文件太大，截断或跳过
            if len(code_content) > self.config.MAX_FILE_SIZE:
                logging.warning(f"File {file_path} exceeds maximum size, truncating")
                code_content = code_content[:self.config.MAX_FILE_SIZE]
            
            # 步骤1: 生成初始报告
            initial_reports = self._generate_initial_reports(code_content)
            
            if not initial_reports:
                return None
            
            # 步骤2: 关键审查
            critical_reports = self._generate_critical_reports(code_content, initial_reports)
            
            # 步骤3: 生成最终报告
            final_report = self._generate_final_report(code_content, critical_reports)
            
            return {
                "file_path": str(file_path),
                "initial_reports": initial_reports,
                "critical_reports": critical_reports,
                "final_report": final_report
            }
            
        except Exception as e:
            logging.error(f"Error analyzing file {file_path}: {str(e)}")
            return None
    
    def _generate_initial_reports(self, code_content):
        """步骤1: 生成初始报告"""
        reports = []
        model = self.config.GPT_MODEL
        num_reports = self.config.GPT3_REPORTS if "gpt-3" in model else self.config.GPT4_REPORTS
        
        for i in range(num_reports):
            try:
                response = self._call_openai(
                    system_prompt=self.prompts["initial_report"],
                    user_prompt=f"{code_content}\n\n{self.prompts['code_analysis']}",
                    temperature=1.0,
                    top_p=0.9
                )
                
                # 解析JSON响应
                report = self._parse_json_response(response)
                if report:
                    reports.append(report)
                    
            except Exception as e:
                logging.error(f"Error generating initial report {i+1}: {str(e)}")
                continue
        
        return reports
    
    def _generate_critical_reports(self, code_content, initial_reports):
        """步骤2: 生成关键审查报告"""
        reports = []
        model = self.config.GPT_MODEL
        num_reports = self.config.GPT3_REPORTS if "gpt-3" in model else self.config.GPT4_REPORTS
        
        # 准备初始报告的文本表示
        reports_text = json.dumps(initial_reports, indent=2)
        
        for i in range(num_reports):
            try:
                user_prompt = f"Code:\n{code_content}\n\nReports to review:\n{reports_text}"
                
                response = self._call_openai(
                    system_prompt=self.prompts["critical_review"],
                    user_prompt=user_prompt,
                    temperature=0.75,
                    top_p=0.6
                )
                
                report = self._parse_json_response(response)
                if report:
                    reports.append(report)
                    
            except Exception as e:
                logging.error(f"Error generating critical report {i+1}: {str(e)}")
                continue
        
        return reports
    
    def _generate_final_report(self, code_content, critical_reports):
        """步骤3: 生成最终报告"""
        try:
            # 准备关键报告的文本表示
            reports_text = json.dumps(critical_reports, indent=2)
            
            # 结合初始报告提示和最终报告提示
            system_prompt = f"{self.prompts['final_report']}\n\n{self.prompts['initial_report']}"
            user_prompt = f"Code:\n{code_content}\n\nCritical reports:\n{reports_text}"
            
            response = self._call_openai(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=0.5,
                top_p=0.5
            )
            
            final_report = self._parse_json_response(response)
            return final_report
            
        except Exception as e:
            logging.error(f"Error generating final report: {str(e)}")
            return None
    
    def _call_openai(self, system_prompt, user_prompt, temperature, top_p):
        """调用OpenAI API"""
        try:
            response = self.openai_client.chat.completions.create(
                model=self.config.GPT_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                top_p=top_p,
                response_format={"type": "json_object"}  # 强制JSON响应
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logging.error(f"OpenAI API call failed: {str(e)}")
            # 实现重试逻辑
            time.sleep(5)
            raise
    
    def _parse_json_response(self, response_text):
        """解析JSON响应"""
        try:
            # 清理响应文本
            response_text = response_text.strip()
            
            # 尝试解析JSON
            return json.loads(response_text)
            
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse JSON response: {str(e)}")
            logging.debug(f"Response text: {response_text}")
            
            # 尝试修复常见的JSON错误
            try:
                # 移除可能的前后文本
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                if start_idx != -1 and end_idx > start_idx:
                    json_text = response_text[start_idx:end_idx]
                    return json.loads(json_text)
            except:
                pass
            
            return None