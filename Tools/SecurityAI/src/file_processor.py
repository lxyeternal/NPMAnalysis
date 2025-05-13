import os
from pathlib import Path
import logging

class FileProcessor:
    def __init__(self, config):
        self.config = config
        self.supported_extensions = ['.js', '.mjs', '.cjs']
        
    def scan_packages(self, dataset_path):
        """扫描数据集目录中的所有包"""
        package_dirs = []
        
        try:
            dataset_path = Path(dataset_path)
            
            # 遍历目录结构：包名 - 版本
            for package_name_dir in dataset_path.iterdir():
                if package_name_dir.is_dir():
                    for version_dir in package_name_dir.iterdir():
                        if version_dir.is_dir():
                            # 组合包名和版本作为完整的包标识
                            full_package_name = f"{package_name_dir.name}-{version_dir.name}"
                            package_dirs.append(version_dir)
                            
            logging.info(f"Found {len(package_dirs)} packages in {dataset_path}")
            return package_dirs
            
        except Exception as e:
            logging.error(f"Error scanning packages in {dataset_path}: {str(e)}")
            return []
    
    def find_js_files(self, package_dir):
        """在包目录中查找所有JavaScript文件"""
        js_files = []
        
        try:
            for root, dirs, files in os.walk(package_dir):
                # 跳过特定目录
                if 'node_modules' in dirs:
                    dirs.remove('node_modules')
                if '.git' in dirs:
                    dirs.remove('.git')
                
                for file in files:
                    file_path = Path(root) / file
                    
                    # 检查文件扩展名
                    if file_path.suffix.lower() in self.supported_extensions:
                        js_files.append(file_path)
                    
                    # 特殊处理package.json
                    elif file == 'package.json':
                        js_files.append(file_path)
            
            logging.debug(f"Found {len(js_files)} JavaScript files in {package_dir}")
            return js_files
            
        except Exception as e:
            logging.error(f"Error finding JS files in {package_dir}: {str(e)}")
            return []
    
    def read_file_content(self, file_path):
        """读取文件内容"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 如果文件太大，返回截断的内容
            if len(content) > self.config.MAX_FILE_SIZE:
                logging.warning(f"File {file_path} exceeds max size, truncating")
                return content[:self.config.MAX_FILE_SIZE]
            
            return content
            
        except Exception as e:
            logging.error(f"Error reading file {file_path}: {str(e)}")
            return None