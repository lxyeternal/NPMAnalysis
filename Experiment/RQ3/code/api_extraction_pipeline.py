#!/usr/bin/env python3
"""
RQ3: API Extraction Pipeline
Extracts API calls from malware snippets
"""

import os
import json
import logging
from pathlib import Path
from collections import defaultdict
from tqdm import tqdm

import tree_sitter_javascript as tsjs
from tree_sitter import Language, Parser

INPUT_DIR = Path("/home2/wenbo/Documents/NPMAnalysis/Core/Analysis/code_snipptes/malware_snippets")
OUTPUT_DIR = Path("/home2/wenbo/Documents/NPMAnalysis/Experiment/RQ3/statistic/api_extraction")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_CATEGORIES = {
    'execution': {
        'child_process': ['exec', 'execSync', 'execFile', 'execFileSync', 'spawn', 'spawnSync', 'fork'],
        'vm': ['runInContext', 'runInNewContext', 'runInThisContext', 'createContext', 'createScript', 'Script', 'compileFunction'],
        '_global': ['eval', 'Function', 'setTimeout', 'setInterval', 'setImmediate'],
        'module': ['require', '_load', '_compile', 'createRequire'],
        'worker_threads': ['Worker'],
        'cluster': ['fork'],
    },
    'network': {
        'http': ['request', 'get', 'post', 'createServer', 'Server', 'Agent'],
        'https': ['request', 'get', 'post', 'createServer', 'Server', 'Agent'],
        'net': ['connect', 'createConnection', 'createServer', 'Socket', 'Server'],
        'dgram': ['createSocket', 'send', 'bind'],
        'dns': ['lookup', 'resolve', 'resolve4', 'resolve6', 'resolveMx', 'resolveTxt', 'resolveNs', 'getServers', 'setServers'],
        'tls': ['connect', 'createServer', 'createSecureContext', 'TLSSocket'],
        '_global': ['fetch', 'XMLHttpRequest', 'WebSocket', 'axios', 'got', 'superagent', 'needle', 'request'],
    },
    'filesystem': {
        'fs': [
            'readFile', 'readFileSync', 'readdir', 'readdirSync', 'read', 'readSync', 'createReadStream', 'readlink', 'readlinkSync',
            'writeFile', 'writeFileSync', 'appendFile', 'appendFileSync', 'write', 'writeSync', 'createWriteStream',
            'unlink', 'unlinkSync', 'rename', 'renameSync', 'copyFile', 'copyFileSync', 'truncate', 'truncateSync',
            'chmod', 'chmodSync', 'chown', 'chownSync', 'rm', 'rmSync', 'mkdir', 'mkdirSync', 'rmdir', 'rmdirSync',
            'stat', 'statSync', 'lstat', 'lstatSync', 'exists', 'existsSync', 'access', 'accessSync',
            'realpath', 'realpathSync', 'link', 'linkSync', 'symlink', 'symlinkSync', 'watch', 'watchFile',
            'open', 'openSync', 'opendir', 'opendirSync',
        ],
        'path': ['join', 'resolve', 'basename', 'dirname', 'extname', 'normalize', 'parse'],
    },
    'process_info': {
        'process': [
            'env', 'argv', 'argv0', 'execArgv', 'execPath', 'cwd', 'chdir', 'exit', 'kill',
            'pid', 'ppid', 'platform', 'arch', 'stdin', 'stdout', 'stderr', 'memoryUsage', 'cpuUsage', 'uptime',
        ],
    },
    'crypto': {
        'crypto': [
            'createHash', 'createHmac', 'getHashes', 'hash',
            'createCipher', 'createCipheriv', 'createDecipher', 'createDecipheriv',
            'publicEncrypt', 'privateEncrypt', 'publicDecrypt', 'privateDecrypt',
            'createSign', 'createVerify', 'sign', 'verify',
            'randomBytes', 'randomFill', 'randomFillSync', 'randomInt', 'randomUUID',
            'pbkdf2', 'pbkdf2Sync', 'scrypt', 'scryptSync',
            'generateKeyPair', 'generateKeyPairSync', 'createDiffieHellman', 'createECDH',
        ],
    },
    'encoding': {
        'Buffer': ['from', 'alloc', 'allocUnsafe', 'concat', 'toString', 'isBuffer'],
        'querystring': ['parse', 'stringify', 'encode', 'decode', 'escape', 'unescape'],
        'JSON': ['parse', 'stringify'],
        'url': ['parse', 'format', 'resolve', 'URL', 'URLSearchParams'],
        'zlib': ['gzip', 'gunzip', 'deflate', 'inflate', 'createGzip', 'createGunzip', 'brotliCompress', 'brotliDecompress'],
        '_global': ['btoa', 'atob', 'encodeURIComponent', 'decodeURIComponent', 'encodeURI', 'decodeURI', 'TextEncoder', 'TextDecoder'],
    },
    'system_info': {
        'os': ['hostname', 'homedir', 'userInfo', 'platform', 'arch', 'release', 'type', 'cpus',
               'networkInterfaces', 'tmpdir', 'totalmem', 'freemem', 'uptime', 'loadavg'],
    },
}


def create_parser():
    return Parser(Language(tsjs.language()))


def extract_apis_from_code(code_str, parser):
    if not code_str or not code_str.strip():
        return {}

    try:
        code_bytes = code_str.encode('utf-8', errors='ignore')
        tree = parser.parse(code_bytes)
    except Exception:
        return {}

    strings = set()
    def collect_strings(node):
        if node.type == 'string':
            text = code_bytes[node.start_byte:node.end_byte].decode(errors='ignore')
            strings.add(text.strip("'\""))
        for child in node.children:
            collect_strings(child)
    collect_strings(tree.root_node)

    calls = []
    def collect_calls(node):
        if node.type == 'call_expression':
            func = node.child_by_field_name('function')
            if func:
                calls.append(code_bytes[func.start_byte:func.end_byte].decode(errors='ignore'))
        for child in node.children:
            collect_calls(child)
    collect_calls(tree.root_node)

    members = []
    def collect_members(node):
        if node.type == 'member_expression':
            members.append(code_bytes[node.start_byte:node.end_byte].decode(errors='ignore'))
        for child in node.children:
            collect_members(child)
    collect_members(tree.root_node)

    found_apis = defaultdict(set)

    for s in strings:
        for category, modules in API_CATEGORIES.items():
            for module, apis in modules.items():
                if s == module and module != '_global':
                    found_apis[category].add(f"[module] {module}")
                for api in apis:
                    if s == api:
                        found_apis[category].add(f"{module}.{api}" if module != '_global' else api)

    for call in calls:
        for category, modules in API_CATEGORIES.items():
            for module, apis in modules.items():
                for api in apis:
                    if f"{module}.{api}" in call or (module == '_global' and api in call):
                        found_apis[category].add(f"{module}.{api}" if module != '_global' else api)

    for member in members:
        for category, modules in API_CATEGORIES.items():
            for module, apis in modules.items():
                for api in apis:
                    if f"{module}.{api}" in member:
                        found_apis[category].add(f"{module}.{api}" if module != '_global' else api)

    return {k: sorted(list(v)) for k, v in found_apis.items() if v}


def process_single_file(input_path: Path) -> dict:
    parser = create_parser()

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        logger.error(f"Failed to read {input_path}: {e}")
        return None

    metadata = data.get('metadata', {})
    snippets = data.get('malicious_snippets', [])

    if not snippets:
        return None

    result = {
        'metadata': {
            'package_name': metadata.get('package_name', ''),
            'version': metadata.get('version', ''),
            'snippet_count': len(snippets),
        },
        'snippets': []
    }

    all_apis_by_category = defaultdict(set)

    for idx, snippet in enumerate(snippets):
        code = snippet.get('malicious_code', '')
        apis = extract_apis_from_code(code, parser)

        result['snippets'].append({
            'index': idx,
            'file': snippet.get('file', ''),
            'hash': snippet.get('hash_value', ''),
            'apis': apis,
            'api_count': sum(len(v) for v in apis.values())
        })

        for category, api_list in apis.items():
            all_apis_by_category[category].update(api_list)

    result['summary'] = {
        'total_apis': sum(len(v) for v in all_apis_by_category.values()),
        'apis_by_category': {k: sorted(list(v)) for k, v in all_apis_by_category.items()},
        'category_counts': {k: len(v) for k, v in all_apis_by_category.items()}
    }

    return result


def get_relative_path(input_path: Path) -> Path:
    parts = input_path.parts
    try:
        idx = parts.index('malware_snippets')
        return Path(*parts[idx+1:-1])
    except ValueError:
        return Path(input_path.parent.name)


def main():
    logger.info("=" * 60)
    logger.info("API Extraction Pipeline")
    logger.info("=" * 60)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    logger.info(f"Scanning {INPUT_DIR}...")
    input_files = list(INPUT_DIR.rglob("result.json"))
    logger.info(f"Found {len(input_files)} result.json files")

    stats = {
        'total_files': len(input_files),
        'processed': 0,
        'failed': 0,
        'total_snippets': 0,
        'total_apis': 0,
        'category_totals': defaultdict(int)
    }

    for input_path in tqdm(input_files, desc="Processing"):
        try:
            result = process_single_file(input_path)

            if result is None:
                stats['failed'] += 1
                continue

            rel_path = get_relative_path(input_path)
            output_path = OUTPUT_DIR / rel_path / "apis.json"
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            stats['processed'] += 1
            stats['total_snippets'] += result['metadata']['snippet_count']
            stats['total_apis'] += result['summary']['total_apis']
            for cat, count in result['summary']['category_counts'].items():
                stats['category_totals'][cat] += count

        except Exception as e:
            logger.error(f"Error processing {input_path}: {e}")
            stats['failed'] += 1

    logger.info("\n" + "=" * 60)
    logger.info("Pipeline Complete!")
    logger.info("=" * 60)
    logger.info(f"Total files:     {stats['total_files']}")
    logger.info(f"Processed:       {stats['processed']}")
    logger.info(f"Failed:          {stats['failed']}")
    logger.info(f"Total snippets:  {stats['total_snippets']}")
    logger.info(f"Total APIs:      {stats['total_apis']}")
    logger.info("\nAPIs by category:")
    for cat, count in sorted(stats['category_totals'].items(), key=lambda x: -x[1]):
        logger.info(f"  {cat}: {count}")

    summary_path = OUTPUT_DIR / "extraction_summary.json"
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump({
            'total_files': stats['total_files'],
            'processed': stats['processed'],
            'failed': stats['failed'],
            'total_snippets': stats['total_snippets'],
            'total_apis': stats['total_apis'],
            'category_totals': dict(stats['category_totals'])
        }, f, indent=2)
    logger.info(f"\nSummary saved to: {summary_path}")


if __name__ == "__main__":
    main()
