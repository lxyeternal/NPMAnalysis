#!/usr/bin/env python3
import os
import json
from pathlib import Path

def find_package_dir(start_path, max_depth=5):
    """
    递归查找package目录
    返回: (package_dir_path, relative_path) 或 (None, None)
    """
    def _recursive_find(current_path, depth=0):
        if depth > max_depth:
            return None, None
            
        # 检查当前目录下是否有package目录
        package_dir = current_path / "package"
        if package_dir.exists() and package_dir.is_dir():
            relative_path = str(package_dir.relative_to(start_path))
            return package_dir, relative_path
        
        # 递归查找子目录
        for item in current_path.iterdir():
            if item.is_dir():
                found_dir, found_relative = _recursive_find(item, depth + 1)
                if found_dir:
                    return found_dir, found_relative
        
        return None, None
    
    return _recursive_find(start_path)

def analyze_npm_structure(base_paths):
    """
    分析NPM数据集的目录结构
    预期结构: 包名/版本/[可能多层]/package/package.json
    """
    results = {
        'summary': {},
        'issues': {
            'missing_package_dir': [],
            'missing_package_json': [],
            'unexpected_structure': [],
            'deep_package_dirs': []  # 记录package目录不在第三层的情况
        }
    }
    
    for base_path in base_paths:
        print(f"\n正在分析: {base_path}")
        path_obj = Path(base_path)
        
        if not path_obj.exists():
            print(f"路径不存在: {base_path}")
            continue
            
        dataset_name = path_obj.name
        results['summary'][dataset_name] = {
            'total_packages': 0,
            'valid_structure': 0,
            'missing_package_dir': 0,
            'missing_package_json': 0,
            'unexpected_structure': 0,
            'deep_package_dirs': 0  # package目录不在直接第三层的数量
        }
        
        # 遍历包名目录
        for package_name_dir in path_obj.iterdir():
            if not package_name_dir.is_dir():
                continue
                
            print(f"  检查包: {package_name_dir.name}")
            
            # 遍历版本目录
            for version_dir in package_name_dir.iterdir():
                if not version_dir.is_dir():
                    continue
                    
                results['summary'][dataset_name]['total_packages'] += 1
                package_path = f"{package_name_dir.name}/{version_dir.name}"
                full_path = str(version_dir)
                
                # 递归查找package目录
                package_dir, package_relative_path = find_package_dir(version_dir)
                
                if not package_dir:
                    results['summary'][dataset_name]['missing_package_dir'] += 1
                    results['issues']['missing_package_dir'].append(
                        f"{dataset_name}: {package_path} - 找不到package目录 - {full_path}"
                    )
                    continue
                
                # 检查package目录是否在第三层，如果不是，记录为深层目录
                if package_relative_path != "package":
                    results['summary'][dataset_name]['deep_package_dirs'] += 1
                    results['issues']['deep_package_dirs'].append(
                        f"{dataset_name}: {package_path} - package目录在深层: {package_relative_path} - {full_path}"
                    )
                
                # 检查package.json文件
                package_json = package_dir / "package.json"
                if not package_json.exists():
                    results['summary'][dataset_name]['missing_package_json'] += 1
                    results['issues']['missing_package_json'].append(
                        f"{dataset_name}: {package_path} - package目录下缺少package.json - {package_relative_path} - {full_path}"
                    )
                    continue
                
                if not package_json.is_file():
                    results['summary'][dataset_name]['unexpected_structure'] += 1
                    results['issues']['unexpected_structure'].append(
                        f"{dataset_name}: {package_path} - package.json不是文件 - {package_relative_path} - {full_path}"
                    )
                    continue
                
                # 结构完整
                results['summary'][dataset_name]['valid_structure'] += 1
    
    return results

def print_analysis_results(results):
    """打印分析结果"""
    print("\n" + "="*60)
    print("NPM数据集结构分析报告")
    print("="*60)
    
    # 打印总结
    for dataset_name, summary in results['summary'].items():
        print(f"\n【{dataset_name}】")
        print(f"  总包数量: {summary['total_packages']}")
        print(f"  结构完整: {summary['valid_structure']} ({summary['valid_structure']/max(summary['total_packages'], 1)*100:.1f}%)")
        print(f"  缺少package目录: {summary['missing_package_dir']}")
        print(f"  缺少package.json: {summary['missing_package_json']}")
        print(f"  其他结构异常: {summary['unexpected_structure']}")
    
    # 只打印缺少package目录和package.json的问题
    problem_types = ['missing_package_dir', 'missing_package_json']
    has_problems = any(results['issues'][ptype] for ptype in problem_types)
    
    if has_problems:
        print(f"\n{'='*60}")
        print("问题详情")
        print("="*60)
        
        for issue_type in problem_types:
            issues = results['issues'][issue_type]
            if issues:
                type_name = {
                    'missing_package_dir': '缺少package目录',
                    'missing_package_json': '缺少package.json'
                }[issue_type]
                print(f"\n【{type_name}】")
                for issue in issues:
                    print(f"  - {issue}")
    else:
        print(f"\n✅ 所有包都符合预期结构！")

def save_results_to_file(results, output_file="npm_structure_analysis.json"):
    """保存结果到文件"""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n结果已保存到: {output_file}")

if __name__ == "__main__":
    # 设置要分析的路径
    base_paths = [
        "/home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_benign",
        "/home2/wenbo/Documents/NPMAnalysis/Dataset/unzip_malware"
    ]
    
    # 执行分析
    results = analyze_npm_structure(base_paths)
    
    # 打印结果
    print_analysis_results(results)
    
    # 保存结果
    save_results_to_file(results)
    
    # 额外的快速检查功能
    print(f"\n{'='*60}")
    print("快速检查示例")
    print("="*60)
    
    # 显示前几个包的结构作为示例
    for base_path in base_paths:
        path_obj = Path(base_path)
        if path_obj.exists():
            print(f"\n{path_obj.name} 前3个包的结构:")
            count = 0
            for package_name_dir in path_obj.iterdir():
                if not package_name_dir.is_dir() or count >= 3:
                    continue
                count += 1
                print(f"  {package_name_dir.name}/")
                for version_dir in package_name_dir.iterdir():
                    if version_dir.is_dir():
                        print(f"    {version_dir.name}/")
                        for item in version_dir.iterdir():
                            if item.is_dir():
                                print(f"      {item.name}/")
                                if item.name == "package":
                                    for sub_item in item.iterdir():
                                        print(f"        {sub_item.name}")
                        break  # 只看第一个版本