#!/usr/bin/env python3
"""
Expert Evaluation Script for Malicious Code Snippet Extraction Validation
Uses multiprocessing with parallel workers for evaluation
Simulates 3 experts to judge whether extracted malicious code snippets are correct
"""

import os
import sys
import json
import random
import time
import logging
import hashlib
from multiprocessing import Pool
from typing import List, Dict, Set, Optional, Tuple
from datetime import datetime

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, PROJECT_ROOT)
from Utils.llm_client import LLMClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Directories and paths
SNIPPETS_DIR = "/home2/wenbo/Documents/NPMAnalysis/Core/Analysis/code_snipptes/malware_snippets"
OUTPUT_DIR = "/home2/wenbo/Documents/NPMAnalysis/Core/Analysis/code_snipptes/evaluation_results"
EVALUATED_FILE = os.path.join(OUTPUT_DIR, "snippet_evaluation_results.json")

# Multiprocessing config
NUM_WORKERS = 10
NUM_SAMPLES = 500


def get_sample_key(package_name: str, version: str, file_path: str, line_number: str) -> str:
    """Generate unique key for a sample"""
    key_str = f"{package_name}_{version}_{file_path}_{line_number}"
    return hashlib.md5(key_str.encode()).hexdigest()


def load_evaluated_samples() -> Set[str]:
    """Load already evaluated sample keys"""
    evaluated_keys = set()

    if not os.path.exists(EVALUATED_FILE):
        logging.info(f"No existing evaluated file found: {EVALUATED_FILE}")
        return evaluated_keys

    try:
        with open(EVALUATED_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)

        results = data.get('results', [])
        for r in results:
            sample_key = r.get('sample_key', '')
            if sample_key:
                evaluated_keys.add(sample_key)

        logging.info(f"Loaded {len(evaluated_keys)} already evaluated samples to skip")

    except Exception as e:
        logging.warning(f"Failed to load evaluated samples: {e}")

    return evaluated_keys


def fix_path(file_path: str) -> str:
    """Fix old paths from different user/machine"""
    # Replace old user paths with current user path
    old_prefixes = ['/home2/mynames/', '/home/mynames/']
    new_prefix = '/home2/wenbo/'

    for old_prefix in old_prefixes:
        if file_path.startswith(old_prefix):
            file_path = new_prefix + file_path[len(old_prefix):]
            break
    return file_path


def read_source_code(file_path: str) -> Optional[str]:
    """Read the complete source code file"""
    try:
        # Fix path if needed
        file_path = fix_path(file_path)

        if not os.path.exists(file_path):
            logging.warning(f"Source file not found: {file_path}")
            return None
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        logging.warning(f"Failed to read source file {file_path}: {e}")
        return None


def collect_all_samples(skip_keys: Set[str] = None) -> List[Dict]:
    """Collect all malicious snippet samples from result.json files"""

    if skip_keys is None:
        skip_keys = set()

    all_samples = []
    skipped_count = 0
    missing_file_count = 0

    for package_name in os.listdir(SNIPPETS_DIR):
        package_dir = os.path.join(SNIPPETS_DIR, package_name)
        if not os.path.isdir(package_dir):
            continue

        for version in os.listdir(package_dir):
            version_dir = os.path.join(package_dir, version)
            if not os.path.isdir(version_dir):
                continue

            result_path = os.path.join(version_dir, "result.json")
            if not os.path.exists(result_path):
                continue

            try:
                with open(result_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                metadata = data.get('metadata', {})
                unzip_dir = metadata.get('unzip_dir', '')
                snippets = data.get('malicious_snippets', [])

                for snippet in snippets:
                    file_path = snippet.get('file', '')
                    line_number = snippet.get('line_number', '')
                    malicious_code = snippet.get('malicious_code', '')
                    detection_type = snippet.get('type', '')
                    behavior_summary = snippet.get('behavior_summary', '')

                    if not malicious_code or not file_path:
                        continue

                    # Generate unique key
                    sample_key = get_sample_key(package_name, version, file_path, line_number)

                    # Skip already evaluated
                    if sample_key in skip_keys:
                        skipped_count += 1
                        continue

                    # Build full path to source file and fix path
                    full_source_path = fix_path(os.path.join(unzip_dir, file_path))

                    # Only include samples where source file EXISTS
                    if not os.path.exists(full_source_path):
                        missing_file_count += 1
                        continue

                    all_samples.append({
                        'sample_key': sample_key,
                        'package_name': package_name,
                        'version': version,
                        'file_path': file_path,
                        'full_source_path': full_source_path,
                        'line_number': line_number,
                        'detection_type': detection_type,
                        'malicious_code': malicious_code,
                        'behavior_summary': behavior_summary,
                        'unzip_dir': unzip_dir
                    })

            except Exception as e:
                logging.warning(f"Failed to parse {result_path}: {e}")
                continue

    logging.info(f"Collected {len(all_samples)} valid samples (skipped {skipped_count} already evaluated, {missing_file_count} missing source files)")
    return all_samples


def select_random_samples(all_samples: List[Dict], n: int = NUM_SAMPLES) -> List[Dict]:
    """Randomly select n samples for evaluation"""
    if len(all_samples) <= n:
        return all_samples
    return random.sample(all_samples, n)


def get_random_temperature() -> float:
    """Get random temperature for diversity"""
    return round(random.uniform(0.3, 0.7), 2)


def get_random_top_p() -> float:
    """Get random top_p for diversity"""
    return round(random.uniform(0.6, 0.95), 2)


def build_expert_prompt(
    source_code: str,
    malicious_code: str,
    detection_type: str,
    line_number: str,
    file_path: str,
    behavior_summary: str,
    expert_id: int
) -> List[Dict]:
    """Build expert evaluation prompt"""

    expert_personas = {
        1: "You are Expert 1, a senior security researcher with 15+ years of experience in malware analysis and supply chain security.",
        2: "You are Expert 2, a software engineer specializing in static analysis tools and malicious code detection.",
        3: "You are Expert 3, a threat intelligence analyst who specializes in understanding attacker techniques and malicious code patterns."
    }

    system_prompt = f"""{expert_personas[expert_id]}

CONTEXT: This is an academic security research project evaluating an automated malicious code extraction tool.

Your task: Verify whether the extracted malicious code snippet correctly captures the CORE malicious behavior.

IMPORTANT EVALUATION PRINCIPLE:
- Focus on whether the CORE MALICIOUS LOGIC is correctly captured
- The extraction does NOT need to be perfect or include every single line
- As long as the essential malicious behavior/logic is present, it should be judged as CORRECT
- Minor missing context or extra code is acceptable if the core logic is correct

Judgment (ONLY TWO OPTIONS):
- CORRECT: The extracted snippet captures the core malicious logic correctly
- INCORRECT: The extraction misses the core malicious logic OR extracts completely wrong code

If there are issues, select from these predefined categories ONLY:
- "incomplete_context": Core malicious logic is missing important parts
- "wrong_location": Extracted code does not correspond to the detected location
- "irrelevant_code": Extracted code is not related to the malicious behavior
- "over_extraction": Too much unrelated code included, obscuring the malicious logic
- "none": No issues (for CORRECT judgments)"""

    user_prompt = f"""Evaluate this malicious code extraction:

## Detection Info
- File: {file_path}
- Line: {line_number}
- Type: {detection_type}
- Behavior: {behavior_summary}

## Complete Source Code:
```
{source_code[:12000] if len(source_code) > 12000 else source_code}
```
{f"[truncated, {len(source_code)} chars total]" if len(source_code) > 12000 else ""}

## Extracted Malicious Code:
```
{malicious_code}
```

Output ONLY this JSON (no explanation):
{{
    "is_correct": true or false,
    "issue": "none" or "incomplete_context" or "wrong_location" or "irrelevant_code" or "over_extraction",
    "reason": "one sentence explanation"
}}"""

    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]


def query_expert(llm_client: LLMClient, messages: List[Dict],
                 temperature: float, top_p: float, max_retries: int = 3) -> Optional[Dict]:
    """Query single expert with retry logic"""

    for attempt in range(max_retries):
        try:
            response = llm_client.perform_query(
                messages,
                temperature=temperature,
                top_p=top_p,
                max_tokens=2000
            )

            # Parse JSON response
            if isinstance(response, str):
                # Try to extract JSON from response
                import re
                json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group(1))
                else:
                    result = json.loads(response)
                return result
            return response

        except json.JSONDecodeError as e:
            logging.warning(f"JSON parse failed (attempt {attempt+1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(2)
        except Exception as e:
            logging.warning(f"LLM query failed (attempt {attempt+1}): {e}")
            if attempt < max_retries - 1:
                time.sleep(5 * (attempt + 1))

    return None


def evaluate_single_sample(args) -> Dict:
    """Evaluate a single sample with 3 experts (worker function for multiprocessing)"""

    sample, sample_idx, total_samples = args

    logging.info(f"[{sample_idx+1}/{total_samples}] Evaluating {sample['package_name']}/{sample['version']} - {sample['file_path']}:{sample['line_number']}")

    # Read source code
    source_code = read_source_code(sample['full_source_path'])
    if not source_code:
        return {
            'sample_key': sample['sample_key'],
            'sample_info': sample,
            'error': f"Cannot read source file: {sample['full_source_path']}",
            'expert_results': [],
            'final_judgment': {'judgment': None, 'error': 'Source file not found'}
        }

    # Create LLM client for this worker
    try:
        llm_client = LLMClient()
    except Exception as e:
        return {
            'sample_key': sample['sample_key'],
            'sample_info': sample,
            'error': f"Failed to create LLM client: {e}",
            'expert_results': [],
            'final_judgment': {'judgment': None, 'error': 'LLM client error'}
        }

    expert_results = []

    for expert_id in [1, 2, 3]:
        temperature = get_random_temperature()
        top_p = get_random_top_p()

        messages = build_expert_prompt(
            source_code=source_code,
            malicious_code=sample['malicious_code'],
            detection_type=sample['detection_type'],
            line_number=sample['line_number'],
            file_path=sample['file_path'],
            behavior_summary=sample['behavior_summary'],
            expert_id=expert_id
        )

        result = query_expert(llm_client, messages, temperature, top_p)

        if result:
            expert_results.append({
                'expert_id': expert_id,
                'is_correct': result.get('is_correct', False),
                'issue': result.get('issue', 'none'),
                'reason': result.get('reason', '')
            })
        else:
            expert_results.append({
                'expert_id': expert_id,
                'error': 'Failed to get response'
            })

        time.sleep(0.5)  # Rate limiting

    # Aggregate results
    final_judgment = aggregate_expert_results(expert_results)

    return {
        'sample_key': sample['sample_key'],
        'sample_info': {
            'package_name': sample['package_name'],
            'version': sample['version'],
            'file_path': sample['file_path'],
            'line_number': sample['line_number'],
            'detection_type': sample['detection_type'],
            'malicious_code': sample['malicious_code'][:500] + "..." if len(sample['malicious_code']) > 500 else sample['malicious_code'],
            'behavior_summary': sample['behavior_summary']
        },
        'expert_results': expert_results,
        'final_judgment': final_judgment
    }


def aggregate_expert_results(expert_results: List[Dict]) -> Dict:
    """Aggregate results from 3 experts using majority voting"""

    valid_results = [r for r in expert_results if 'is_correct' in r and 'error' not in r]

    if not valid_results:
        return {
            'is_correct': None,
            'error': 'No valid expert responses'
        }

    # Count votes
    correct_votes = sum(1 for r in valid_results if r.get('is_correct', False))
    incorrect_votes = len(valid_results) - correct_votes

    # Majority vote
    is_correct = correct_votes > incorrect_votes

    # Collect issues (from incorrect votes)
    issue_counts = {}
    reasons = []
    for r in valid_results:
        issue = r.get('issue', 'none')
        if issue and issue != 'none':
            issue_counts[issue] = issue_counts.get(issue, 0) + 1
        if r.get('reason'):
            reasons.append(f"Expert{r['expert_id']}: {r['reason']}")

    # Primary issue is the most common one
    primary_issue = max(issue_counts, key=issue_counts.get) if issue_counts else 'none'

    return {
        'is_correct': is_correct,
        'correct_votes': correct_votes,
        'incorrect_votes': incorrect_votes,
        'consensus': correct_votes == len(valid_results) or incorrect_votes == len(valid_results),
        'primary_issue': primary_issue,
        'issue_counts': issue_counts,
        'reasons': reasons
    }


def calculate_fleiss_kappa(results: List[Dict]) -> float:
    """Calculate Fleiss' Kappa for inter-rater reliability (binary: correct/incorrect)"""

    votes = []
    for r in results:
        if 'expert_results' not in r:
            continue
        expert_votes = []
        for er in r['expert_results']:
            if 'is_correct' in er and 'error' not in er:
                expert_votes.append(1 if er['is_correct'] else 0)
        if len(expert_votes) == 3:
            votes.append(expert_votes)

    if not votes:
        return 0.0

    n = len(votes)  # number of subjects
    k = 3  # number of raters
    categories = 2  # CORRECT (1), INCORRECT (0)

    # Build count matrix [incorrect_count, correct_count]
    n_matrix = []
    for vote in votes:
        correct_count = sum(vote)
        incorrect_count = k - correct_count
        n_matrix.append([incorrect_count, correct_count])

    # Calculate P_i for each subject
    P_i = []
    for row in n_matrix:
        p = (sum(x * x for x in row) - k) / (k * (k - 1))
        P_i.append(p)

    P_bar = sum(P_i) / n

    # Calculate p_j for each category
    p_j = []
    for j in range(categories):
        total = sum(row[j] for row in n_matrix)
        p_j.append(total / (n * k))

    P_e = sum(p * p for p in p_j)

    if P_e == 1:
        return 1.0

    kappa = (P_bar - P_e) / (1 - P_e)
    return round(kappa, 4)


def calculate_statistics(results: List[Dict]) -> Dict:
    """Calculate comprehensive statistics"""

    total = len(results)
    valid_results = [r for r in results if 'final_judgment' in r and r['final_judgment'].get('is_correct') is not None]

    if not valid_results:
        return {'error': 'No valid results'}

    # Count judgments
    correct_count = sum(1 for r in valid_results if r['final_judgment']['is_correct'])
    incorrect_count = len(valid_results) - correct_count

    # Consensus rate
    consensus_count = sum(1 for r in valid_results if r['final_judgment'].get('consensus', False))

    # Fleiss' Kappa
    kappa = calculate_fleiss_kappa(results)

    # Issue statistics
    issue_stats = {
        'incomplete_context': 0,
        'wrong_location': 0,
        'irrelevant_code': 0,
        'over_extraction': 0
    }
    for r in valid_results:
        if not r['final_judgment']['is_correct']:
            issue = r['final_judgment'].get('primary_issue', 'none')
            if issue in issue_stats:
                issue_stats[issue] += 1

    # By detection type
    by_type = {}
    for r in valid_results:
        det_type = r['sample_info'].get('detection_type', 'unknown')
        if det_type not in by_type:
            by_type[det_type] = {'total': 0, 'correct': 0, 'incorrect': 0}
        by_type[det_type]['total'] += 1
        if r['final_judgment']['is_correct']:
            by_type[det_type]['correct'] += 1
        else:
            by_type[det_type]['incorrect'] += 1

    for det_type in by_type:
        t = by_type[det_type]['total']
        by_type[det_type]['accuracy'] = round(by_type[det_type]['correct'] / t, 3) if t > 0 else 0

    return {
        'total_evaluated': len(valid_results),
        'total_errors': total - len(valid_results),
        'correct_count': correct_count,
        'incorrect_count': incorrect_count,
        'accuracy': round(correct_count / len(valid_results), 3),
        'consensus_rate': round(consensus_count / len(valid_results), 3),
        'fleiss_kappa': kappa,
        'issue_statistics': issue_stats,
        'by_detection_type': by_type
    }


def print_summary(results: List[Dict]):
    """Print evaluation summary"""

    stats = calculate_statistics(results)

    print("\n" + "=" * 70)
    print("Malicious Code Snippet Extraction Evaluation Summary")
    print("=" * 70)

    if 'error' in stats:
        print(f"Error: {stats['error']}")
        return

    print(f"Total samples evaluated: {stats['total_evaluated']}")
    print(f"Evaluation errors: {stats['total_errors']}")
    print("-" * 70)
    print(f"CORRECT:   {stats['correct_count']:4d} ({stats['accuracy']*100:.1f}%)")
    print(f"INCORRECT: {stats['incorrect_count']:4d} ({(1-stats['accuracy'])*100:.1f}%)")
    print("-" * 70)
    print(f"Accuracy: {stats['accuracy']*100:.1f}%")
    print(f"Consensus Rate: {stats['consensus_rate']*100:.1f}%")
    print(f"Fleiss' Kappa: {stats['fleiss_kappa']:.4f}")

    print("\nIssue Statistics (for INCORRECT samples):")
    issue_stats = stats.get('issue_statistics', {})
    for issue, count in sorted(issue_stats.items(), key=lambda x: -x[1]):
        if count > 0:
            print(f"  {issue}: {count}")

    print("\nBy Detection Type:")
    for det_type, type_stats in sorted(stats['by_detection_type'].items(), key=lambda x: -x[1]['total']):
        print(f"  {det_type}: {type_stats['correct']}/{type_stats['total']} ({type_stats['accuracy']*100:.1f}%)")

    print("=" * 70)


def save_results(results: List[Dict], output_file: str):
    """Save evaluation results to JSON file"""

    stats = calculate_statistics(results)

    output_data = {
        'metadata': {
            'total_samples': len(results),
            'evaluation_time': datetime.now().isoformat(),
            'num_workers': NUM_WORKERS,
            'statistics': stats
        },
        'results': results
    }

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    logging.info(f"Results saved to: {output_file}")


def run_evaluation(num_samples: int = NUM_SAMPLES,
                   output_file: str = None,
                   num_workers: int = NUM_WORKERS,
                   skip_evaluated: bool = True):
    """Run the complete evaluation with multiprocessing"""

    logging.info(f"Starting evaluation with {num_workers} workers")

    # Load already evaluated samples
    skip_keys = set()
    if skip_evaluated:
        skip_keys = load_evaluated_samples()

    # Collect all samples
    all_samples = collect_all_samples(skip_keys)

    if not all_samples:
        logging.error("No valid samples found")
        return None

    # Random selection
    selected_samples = select_random_samples(all_samples, num_samples)
    logging.info(f"Selected {len(selected_samples)} samples for evaluation")

    # Log detection type distribution
    type_counts = {}
    for s in selected_samples:
        t = s['detection_type']
        type_counts[t] = type_counts.get(t, 0) + 1
    logging.info(f"Detection type distribution: {type_counts}")

    # Prepare worker arguments
    total = len(selected_samples)
    worker_args = [(sample, idx, total) for idx, sample in enumerate(selected_samples)]

    # Run parallel evaluation
    logging.info(f"Starting parallel evaluation with {num_workers} processes...")
    start_time = time.time()

    with Pool(processes=num_workers) as pool:
        results = pool.map(evaluate_single_sample, worker_args)

    elapsed = time.time() - start_time
    logging.info(f"Evaluation completed in {elapsed:.1f} seconds")

    # Save results
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join(OUTPUT_DIR, f"snippet_evaluation_{timestamp}.json")

    save_results(results, output_file)
    print_summary(results)

    return results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Expert Evaluation for Malicious Code Snippet Extraction')
    parser.add_argument('--num-samples', type=int, default=NUM_SAMPLES,
                        help=f'Number of samples to evaluate (default: {NUM_SAMPLES})')
    parser.add_argument('--output', type=str, default=None,
                        help='Output file path')
    parser.add_argument('--workers', type=int, default=NUM_WORKERS,
                        help=f'Number of parallel workers (default: {NUM_WORKERS})')
    parser.add_argument('--no-skip', action='store_true',
                        help='Do not skip already evaluated samples')

    args = parser.parse_args()

    run_evaluation(
        num_samples=args.num_samples,
        output_file=args.output,
        num_workers=args.workers,
        skip_evaluated=not args.no_skip
    )
