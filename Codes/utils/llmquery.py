# @File     : llm_agent.py
# @Project  : BinMalware
# @Author   : honywen
# @version  : python 3.8
# @Description：Simplified LLM Agent class for multi-platform LLM access

import os
import json
import time
import logging
import requests
import tiktoken
import openai
import numpy as np
import faiss
from openai import AzureOpenAI
from typing import List, Dict, Tuple, Union, Optional

class LLMAgent:
    
    def __init__(self):
        """
        Initialize the LLM agent with configuration for various backends
        """
        # Set up project directories
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "Configs", "config.json")
        
        # Load configuration
        self.config = self._load_config()
        self.query_type = self.config.get('query_type', 'azure')
        
        # Initialize clients based on query type
        self._init_clients()
        
        # General settings
        self.max_attempts = 5
        self.max_token_length = 16000
        self.dimension = 3072  # Embedding dimension for text-embedding-3-large model
        self.embedding_model = "text-embedding-3-large"
    
    
    def _load_config(self) -> Dict:
        """Load configuration from JSON file"""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', errors='ignore') as file:
                    return json.load(file)
            except Exception as e:
                logging.error(f"Error loading config from {self.config_path}: {e}")
                return {}
        else:
            logging.warning(f"Config file not found at {self.config_path}, using empty config")
            return {}
    
    def _init_clients(self):
        """Initialize the appropriate clients based on the query type"""
        # Initialize embedding client (always using Azure in this implementation)
        if 'azure_api_key' in self.config:
            self.embedding_client = AzureOpenAI(
                api_key=self.config["azure_api_key"],
                api_version=self.config["azure_api_version"],
                azure_endpoint=self.config["azure_api_base"]
            )
        
        # Initialize the appropriate client based on query type
        if self.query_type == 'azure':
            self.client = AzureOpenAI(
                api_key=self.config["azure_api_key"],
                api_version=self.config["azure_api_version"],
                azure_endpoint=self.config["azure_api_base"]
            )
        elif self.query_type == 'openai':
            self.openai_model = self.config.get('openai_api_model', 'gpt-4o')
            openai.api_key = self.config['openai_api_key']
        elif self.query_type == 'ollama':
            self.ollama_model = self.config.get('ollama_model', 'llama3')
            self.host = os.getenv('OLLAMA_HOST', 'host.docker.internal')
        elif self.query_type == 'xinference':
            self.xinference_model = self.config.get('xinference_model', 'llama3')
            openai.api_base = self.config['xinference_api_base']
            openai.api_key = self.config.get('xinference_api_key', 'dummy-key')
    
    def count_tokens(self, content: str, model: str = "gpt-3.5-turbo-16k-0613") -> int:
        """Count the number of tokens in the given content for the specified model"""
        content = str(content)
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            logging.warning(f"Model {model} not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")
        
        return len(encoding.encode(content))
    
    def token_slice(self, content: str, token_limit: int = 14000) -> List[str]:
        """Split content into chunks that respect token limits"""
        encoding = tiktoken.encoding_for_model("gpt-3.5-turbo-16k-0613")
        content_tokens = encoding.encode(content)
        
        segments = []
        current_segment = []
        current_length = 0
        
        for token in content_tokens:
            if current_length + 1 > token_limit:
                segments.append(encoding.decode(current_segment))
                current_segment = [token]
                current_length = 1
            else:
                current_segment.append(token)
                current_length += 1
                
        if current_segment:
            segments.append(encoding.decode(current_segment))
            
        return segments
    
    def perform_query(self, 
                     messages: List[Dict[str, str]], 
                     max_tokens: int = 16000,
                     temperature: float = 0,
                     top_p: float = 0.3,
                     frequency_penalty: float = 0,
                     presence_penalty: float = 0,
                     response_format: Optional[Dict] = None,
                     seed: int = 42) -> str:
        """
        Unified query interface for all LLM backends
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            max_tokens: Maximum number of tokens in the response
            temperature: Sampling temperature (0-1)
            top_p: Nucleus sampling parameter
            frequency_penalty: Penalty for token frequency
            presence_penalty: Penalty for token presence
            response_format: Specify response format (e.g. {"type": "json_object"})
            seed: Random seed for reproducibility
            
        Returns:
            Response text from the LLM
        """
        # Set defaults for response format if needed
        response_format = response_format or ({"type": "json_object"} if self.query_type == 'azure' else None)
        
        # Call the appropriate backend
        if self.query_type == "azure":
            return self._azure_query(messages, max_tokens, temperature, top_p, 
                                   frequency_penalty, presence_penalty, response_format, seed)
        elif self.query_type == "ollama":
            return self._ollama_query(messages, max_tokens, temperature, top_p, 
                                    frequency_penalty, presence_penalty, response_format, seed)
        elif self.query_type == "openai":
            return self._openai_query(messages, max_tokens, temperature, top_p, 
                                    frequency_penalty, presence_penalty, response_format, seed)
        elif self.query_type == "xinference":
            return self._xinference_query(messages, max_tokens, temperature, top_p, 
                                        frequency_penalty, presence_penalty, response_format, seed)
        else:
            raise ValueError(f"Unknown query type: {self.query_type}")
    
    def _azure_query(self, messages, max_tokens, temperature, top_p, frequency_penalty, presence_penalty, response_format, seed):
        """Execute query using Azure OpenAI"""
        wait_time = 10
        attempt = 0
        
        while attempt < self.max_attempts:
            try:
                completion = self.client.chat.completions.create(
                    model="gpt-4o",  # or use self.config.get("azure_model", "gpt-4o")
                    messages=messages,
                    temperature=temperature,
                    response_format=response_format,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                    stop=None,
                    seed=seed,
                    stream=False
                )
                return completion.choices[0].message.content
            except Exception as e:
                logging.warning(f"Attempt {attempt + 1}: An error occurred: {e}")
                attempt += 1
                time.sleep(wait_time)
                wait_time += 5  # Increase wait time after each failure
        
        return ""  # Return empty string if all attempts fail
    
    def _openai_query(self, messages, max_tokens, temperature, top_p, frequency_penalty, presence_penalty, response_format, seed):
        """Execute query using OpenAI API"""
        wait_time = 10
        attempt = 0
        
        while attempt < self.max_attempts:
            try:
                # Use the legacy API if using older OpenAI version
                response = openai.ChatCompletion.create(
                    model=self.openai_model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                    stop=None
                )
                return response.choices[0].message['content']
            except Exception as e:
                logging.warning(f"Attempt {attempt + 1}: An error occurred: {e}")
                attempt += 1
                time.sleep(wait_time)
                wait_time += 5
        
        return ""
    
    def _ollama_query(self, messages, max_tokens, temperature, top_p, frequency_penalty, presence_penalty, response_format, seed):
        """Execute query using Ollama local API"""
        wait_time = 10
        attempt = 0
        url = f"http://{self.host}:11434/api/chat"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.ollama_model,
            "stream": False,
            "format": "json" if response_format else None,
            "messages": messages,
            "options": {
                "temperature": temperature,
                "seed": seed,
                "num_ctx": 65536
            },
        }
        
        while attempt < self.max_attempts:
            try:
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                return response.json()['message']['content']
            except Exception as e:
                logging.warning(f"Attempt {attempt + 1}: An error occurred: {e}")
                attempt += 1
                time.sleep(wait_time)
                wait_time += 5
        
        return ""
    
    def _xinference_query(self, messages, max_tokens, temperature, top_p, frequency_penalty, presence_penalty, response_format, seed):
        """Execute query using Xinference API"""
        wait_time = 10
        attempt = 0
        
        while attempt < self.max_attempts:
            try:
                response = openai.ChatCompletion.create(
                    model=self.xinference_model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                    frequency_penalty=frequency_penalty,
                    presence_penalty=presence_penalty,
                    stop=None
                )
                return response.choices[0].message['content']
            except Exception as e:
                logging.warning(f"Attempt {attempt + 1}: An error occurred: {e}")
                attempt += 1
                time.sleep(wait_time)
                wait_time += 5
        
        return ""

# # 示例使用方法
# if __name__ == "__main__":
    
#     # 创建代理实例
#     agent = LLMAgent()
    
#     # 准备消息
#     messages = [
#         {"role": "system", "content": "你是一个有用的助手。"},
#         {"role": "user", "content": "请简要介绍一下Python语言。输出成json"}
#     ]
    
#     # 执行查询
#     response = agent.perform_query(messages)
#     print(response)