import argparse
import json
import os
from collections import defaultdict
from src.utils.functions import read_jsonl, read_json_file, extract_json, parse_json, process_eval_json
import pandas as pd


def process_json(data, category):
    scores = defaultdict(lambda: defaultdict(list))
    if not isinstance(data, dict):
        return scores, False

    for key, score_data in data.items():
        if isinstance(score_data, dict) and 'score' in score_data:
            scores[category][key].append(int(score_data['score']))
        elif isinstance(score_data, dict):
            for sub_key, sub_score_data in score_data.items():
                if isinstance(sub_score_data, int):
                    scores[category][key].append(sub_score_data)
                elif isinstance(sub_score_data, dict) and 'score' in sub_score_data:
                    scores[category][key].append({sub_key: int(sub_score_data['score'])})
        else:
            return scores, False
    return scores, True

def calculate_statistics(scores):
    stats = {}
    dialogue_analysis_total = dialogue_analysis_count = all_total = all_count = 0

    for category, sub_scores in scores.items():
        stats[category] = {}
        category_total = category_count = 0

        for sub_key, values in sub_scores.items():
            if values and isinstance(values[0], dict):
                nested_stats = defaultdict(list)
                total_values = total_count = 0

                for value in values:
                    for nested_key, nested_value in value.items():
                        nested_stats[nested_key].append(nested_value)
                
                for nested_key, nested_values in nested_stats.items():
                    stats[category][sub_key] = {
                        "average": (sum(nested_values) / len(nested_values)) if nested_values else 0,
                        "count": len(nested_values)
                    }
                    total_count += sum(nested_values)
                    total_values += len(nested_values)
                
                stats[category][sub_key]['average'] = total_count / total_values if total_values else 0
                stats[category][sub_key]['count'] = total_count
            else:
                stats[category][sub_key] = {
                    "average": (sum(values) / len(values)) if values else 0,
                    "count": len(values)
                }

            category_total += stats[category][sub_key]['average'] * stats[category][sub_key]['count']
            category_count += stats[category][sub_key]['count']

        stats[category]["Overall"] = {
            "average": category_total / category_count if category_count else 0,
            "count": category_count
        }

        if category in ['goal', 'scene', 'persona', 'utterance']:
            dialogue_analysis_total += category_total
            dialogue_analysis_count += category_count

        all_total += category_total
        all_count += category_count

    stats['analysis'] = {
        'Overall': {
            'average': dialogue_analysis_total / dialogue_analysis_count if dialogue_analysis_count else 0,
            'count': dialogue_analysis_count
        }
    }

    stats['ALL'] = {
        'Overall': {
            'average': all_total / all_count if all_count else 0,
            'count': all_count
        }
    }

    return stats

def process_eval_file(file_path, fail_num, success_num, tag, is_dg):
    scores = defaultdict(lambda: defaultdict(list))
    datas = read_jsonl(file_path)
    # low_uuid_list = en_low_uuids + zh_low_uuids
    for data in datas:
        # if data['uuid'] not in low_uuid_list: continue
        if tag not in data:
            fail_num += 1
            continue

        eval_data = data[tag]
        json_text = extract_json(eval_data)
        eval_data, success = parse_json(json_text)
        if not success:
            eval_data = process_eval_json(eval_data)
        if not eval_data:
            fail_num += 1
            continue

        key = data.get('key') if not is_dg else "generation"
        new_scores, success = process_json(eval_data, key)
        if success:
            success_num += 1
            for category, sub_scores in new_scores.items():
                for sub_key, values in sub_scores.items():
                    scores[category][sub_key].extend(values)
        else:
            fail_num += 1

    return scores, fail_num, success_num

def print_statistics_as_table(statistics):
    flat_data = [
        {
            "Category": category,
            "Sub Key": sub_key,
            "Average": metrics["average"],
            "Count": metrics["count"],
        }
        for category, sub_scores in statistics.items()
        for sub_key, metrics in sub_scores.items()
    ]
    df = pd.DataFrame(flat_data)
    print(df)

def main(args):
    all_scores = defaultdict(lambda: defaultdict(list))
    fail_num, success_num = 0, 0
    file_data = {}

    for root, _, files in os.walk(args.result_path):
        for file in files:
            if file.endswith('.jsonl'):
                file_path = os.path.join(root, file)
                file_data[file] = len(read_jsonl(file_path))
                is_dg = 'cg' in file
                file_scores, fail_num, success_num = process_eval_file(file_path, fail_num, success_num, args.tag, is_dg)
                for category, sub_scores in file_scores.items():
                    for sub_key, values in sub_scores.items():
                        all_scores[category][sub_key].extend(values)

    statistics = calculate_statistics(all_scores)
    print_statistics_as_table(statistics)

    print(json.dumps(file_data, indent=4))
    print(f"failed num: {fail_num}")
    print(f"successful num: {success_num}")

def parse_arguments():
    parser = argparse.ArgumentParser(description='args for step3_result.py')
    parser.add_argument("--result_path", type=str, default="result/eval/qwen2_7b")
    parser.add_argument("--tag", type=str, default="eval")
    args = parser.parse_args()
    print(json.dumps(vars(args), indent=4))
    return args

if __name__ == "__main__":
    args = parse_arguments()
    main(args)
