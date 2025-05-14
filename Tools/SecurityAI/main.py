import argparse
import json
from pathlib import Path
from datetime import datetime
from socketai import SocketAI


def print_banner():
    """打印程序横幅"""
    print("="*50)
    print("SocketAI - NPM包恶意代码检测系统")
    print("基于论文: Leveraging Large Language Models to Detect npm Malicious Packages")
    print("="*50)


def print_file_report(report: dict):
    """打印单个文件报告的摘要"""
    print(f"\n文件: {report.get('file_path', 'unknown')}")
    print(f"目的: {report.get('purpose', 'N/A')}")
    print(f"恶意评分: {report.get('malware', 0):.2f}")
    print(f"安全风险: {report.get('securityRisk', 0):.2f}")
    print(f"混淆程度: {report.get('obfuscated', 0):.2f}")
    print(f"置信度: {report.get('confidence', 0):.2f}")
    print(f"是否恶意: {'是' if report.get('is_malicious', False) else '否'}")
    
    if report.get('anomalies'):
        print(f"异常: {report.get('anomalies')}")
    
    if report.get('conclusion'):
        print(f"结论: {report.get('conclusion')}")


def print_package_summary(result: dict):
    """打印包分析的摘要"""
    summary = result.get('summary', {})
    print(f"\n分析摘要:")
    print(f"总文件数: {summary.get('total_files', 0)}")
    print(f"已分析文件: {summary.get('analyzed_files', 0)}")
    print(f"恶意文件数: {summary.get('malicious_files', 0)}")
    print(f"包状态: {'恶意' if result.get('is_malicious', False) else '正常'}")
    
    if result.get('malicious_files'):
        print(f"\n发现的恶意文件:")
        for mf in result['malicious_files']:
            print(f"  - {mf['file']} (恶意评分: {mf['malware_score']:.2f})")
            print(f"    结论: {mf['conclusion']}")


def save_report(result: dict, output_path: str):
    """保存报告到文件"""
    # 添加元数据
    result['metadata'] = {
        'analysis_date': datetime.now().isoformat(),
        'socketai_version': '1.0.0',
        'model_used': result.get('model', 'unknown')
    }
    
    # 保存JSON报告
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n报告已保存到: {output_path}")
    
    # 如果检测到恶意代码，额外保存一个警告文件
    if result.get('is_malicious'):
        warning_path = output_path.replace('.json', '_WARNING.txt')
        with open(warning_path, 'w', encoding='utf-8') as f:
            f.write("⚠️ 警告：检测到恶意代码！\n\n")
            f.write(f"包路径: {result.get('package_dir', result.get('file_path'))}\n")
            f.write(f"分析时间: {result['metadata']['analysis_date']}\n\n")
            
            if 'malicious_files' in result:
                f.write("恶意文件列表:\n")
                for mf in result['malicious_files']:
                    f.write(f"- {mf['file']}\n")
                    f.write(f"  恶意评分: {mf['malware_score']:.2f}\n")
                    f.write(f"  结论: {mf['conclusion']}\n\n")
        
        print(f"⚠️  警告文件已保存到: {warning_path}")


def main():
    parser = argparse.ArgumentParser(
        description='SocketAI - NPM包恶意代码检测系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  分析单个文件:
    python main.py /path/to/file.js
    python main.py /path/to/file.js --mini
    
  分析整个包:
    python main.py /path/to/package/
    python main.py /path/to/package/ --mini --output report.json
        """
    )
    
    parser.add_argument('input', help='要分析的文件或目录路径')
    parser.add_argument('--mini', action='store_true', 
                       help=f'使用更强的模型 {SocketAI().config.STRONG_MODEL}（默认使用 {SocketAI().config.STANDARD_MODEL}）')
    parser.add_argument('--output', default=None, 
                       help='输出报告文件路径（默认: input_report_时间戳.json）')
    parser.add_argument('--verbose', action='store_true', 
                       help='显示详细输出')
    
    args = parser.parse_args()
    
    print_banner()
    
    # 创建SocketAI实例
    socketai = SocketAI()
    
    # 判断输入是文件还是目录
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"错误: {input_path} 不存在")
        return 1
    
    # 生成默认输出文件名
    if args.output is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = input_path.stem if input_path.is_file() else input_path.name
        args.output = f"{base_name}_report_{timestamp}.json"
    
    try:
        if input_path.is_file():
            # 分析单个文件
            result = socketai.analyze_file(str(input_path), use_strong_model=args.mini)
            
            # 打印报告摘要
            print_file_report(result)
            
        elif input_path.is_dir():
            # 分析整个包
            result = socketai.analyze_package(str(input_path), use_strong_model=args.mini)
            
            # 打印包摘要
            print_package_summary(result)
            
            # 如果设置了详细输出，打印每个文件的报告
            if args.verbose:
                for file_report in result.get('files', []):
                    if 'error' not in file_report:
                        print_file_report(file_report)
        else:
            print(f"错误: {input_path} 不是有效的文件或目录")
            return 1
        
        # 保存报告
        save_report(result, args.output)
        
        # 返回状态码（如果检测到恶意代码返回1）
        return 1 if result.get('is_malicious', False) else 0
        
    except KeyboardInterrupt:
        print("\n\n分析被用户中断")
        return 1
    except Exception as e:
        print(f"\n错误: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())