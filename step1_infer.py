import os
from src.utils.functions import load, read_jsonl, parse_json, extract_json, read_json_file
from src.utils.generate import api_generate, LLMPredictor
from src.utils.infer_prompt import *
import json
import argparse
import re
from tqdm import tqdm
import copy

def parse_json_string(json_string):
    patterns = {
        "person": r'"?person"?\s*:\s*"([^"]+)"',
        "content": r'"?content"?\s*:\s*"([^"]+)"'
    }
    dialogue_dict = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, json_string)
        if match:
            value = match.group(1).strip()
            dialogue_dict[key] = value
        else:
            print(f"Failed to extract {key}")
    return dialogue_dict

def build_infer_prompt(type, dialogue_hs, index, dataset_index, input, answer):
    prompt_js = {}
    prompt_js['type'], prompt_js['dialogue_hs'], prompt_js['id'], prompt_js['uuid'] ,prompt_js['answer'], prompt_js['input'] = type, dialogue_hs, index, dataset_index, answer, input
    prompt_js['prompt'] = {'system': "", 'user': input}
    return prompt_js

def data2dainfer_prompt(args, output_path):
    exist_ids = []
    if os.path.exists(output_path):
        exist_datas = read_jsonl(output_path)
        with open(output_path, 'w', encoding='utf-8') as fw:
            for exist_data in exist_datas:
                if exist_data[args.tag]:
                    key = exist_data['uuid'] + str(exist_data['id'])
                    exist_ids.append(key)
                    fw.write(json.dumps(exist_data, ensure_ascii=False) + '\n')   


    datas = read_json_file(args.bench_path)
    prompts = []
    for num, data in enumerate(datas):
        if (data['dataset_id'] + str(num)) in exist_ids:
            continue
        input = data['instruction']
        prompts.append(build_infer_prompt(data['type'], data['dialogue_hs'], num, data['dataset_id'], input, data['answer']))
    return prompts

def is_complete(item, ref_ls):
    return item['uuid'] in ref_ls

def data2dginfer_prompt(output_path, datas, args, dialogue_hs, turn, ref_ls):
    prompts = []
    if os.path.exists(output_path):
        dg_fail_delete(output_path, args.tag)
        exist_ids = []
        exist_datas = read_jsonl(output_path)
        for exist_data in exist_datas:
            key = exist_data['uuid']
            exist_ids.append(key)  
        ref_ls += exist_ids

    for num, item in tqdm(enumerate(datas), total=len(datas), desc="Processing Inference"):
        if is_complete(item, ref_ls):
            continue
    
        prompt_js = {}   
        person_map = {
            item['person1']['name'].lower(): {
                "goal": item['goal'][0],
                "background": item['person1']['background']
            },
            item['person2']['name'].lower(): {
                "goal": item['goal'][1],
                "background": item['person2']['background']
            }
        }
        dialogue_history = dialogue_hs[num][-1] if dialogue_hs[num] else ""
        prompt = dg_test_en_input if args.en else dg_test_zh_input
        p1_name = item['person1']['name'].lower() if turn % 2 == 1 else item['person2']['name'].lower()
        p2_name = item['person2']['name'].lower() if turn % 2 == 1 else item['person1']['name'].lower()
        p1_goal = person_map[p1_name]['goal']
        p1_bg = person_map[p1_name]['background']
        familiarity = int(re.search(r'\d', str(item['combine']['familiarity'])).group())
        p2_bg = "unknown" if familiarity < 4 else person_map[p2_name]['background']
        if not args.en:
            p2_bg = "未知" if familiarity < 4 else p2_bg

        try:
            item['combine']['familiarity'] =  Familiar_map[str(familiarity)][1] if args.en else Familiar_map[str(familiarity)][0]     
        except:
            item['combine']['familiarity'] = item['combine']['familiarity']
        input_prompt = prompt.format(
            dialogue=item, dialogue_history=dialogue_history, 
            p1_name=p1_name, p1_goal=p1_goal, p1_bg=p1_bg, 
            p2_name=p2_name, p2_bg=p2_bg, turn=turn
        )
        
        prompt_js['uuid'] = item['uuid']
        prompt_js['id'] = num
        prompt_js['history'] = dialogue_history
        prompt_js['prompt'] = {'system': "", 'user': input_prompt}
        prompts.append(prompt_js)
    return prompts

def dg_fail_delete(output_path, tag):
    datas = read_jsonl(output_path)
    with open(output_path, 'w', encoding='utf-8') as fw:
        for item in datas:
            if "*ENDING*" in item[tag]:
                fw.write(json.dumps(item, ensure_ascii=False) + '\n')
            else:
                json_text = extract_json(item[tag])
                result, success = parse_json(json_text)
                try:
                    if not success:
                        result = re.sub(r'//.*', '', result).replace('“', '"').replace('”', '"')
                        result = parse_json_string(result)
                    result['person']
                    result['content']
                    fw.write(json.dumps(item, ensure_ascii=False) + '\n')
                except Exception as e:
                    print(e)

        
def dg_output_process(output_path, tag, dialogue_hs, turn, fail_ls, finish_ls):
    datas = read_jsonl(output_path)
    for item in datas:
        dialog_history = dialogue_hs[item['id']]
        if "*ENDING*" in item[tag]:
            finish_ls.append(item['uuid'])
            if not dialog_history:
                dialogue_hs[item['id']].append(item[tag])
        else:
            json_text = extract_json(item[tag])
            result, success = parse_json(json_text)
            try:
                if success:
                    utterance = f"Turn #{turn}\n{result['person']}: {result['content']}\n"
                else:
                    result = re.sub(r'//.*', '', result).replace('“', '"').replace('”', '"')
                    result = parse_json_string(result)
                    utterance = f"Turn #{turn}\n{result['person']}: {result['content']}\n"
            except Exception as e:
                print(e)
                utterance = item[tag]
                fail_ls.append(item['uuid'])

            if dialog_history:
                dialogue_hs[item['id']].append(dialog_history[-1] + utterance)
            else:
                dialogue_hs[item['id']].append(utterance)

    print(f'fail_turn: {len(fail_ls)}')
    print(f'finish_turn: {len(finish_ls)}')
    print('*'*100)

    return dialogue_hs, fail_ls, finish_ls


def dg_result_process(dialogue_hs, datas, output_path):
    with open(output_path, 'w', encoding='utf-8') as fw:
        for i, dialogue in enumerate(dialogue_hs):
            if dialogue: 
                final_dialogues = {
                    'uuid': datas[i]['uuid'],
                    'id': i,
                    'time': datas[i]['combine']['time'],
                    'location': datas[i]['combine']['location'],
                    'talkway': datas[i]['combine']['talkway'],
                    'person1': datas[i]['person1']['name'],
                    'person2': datas[i]['person2']['name'],
                    "person1_bg": datas[i]['person1']['background'],
                    "person2_bg": datas[i]['person2']['background'],
                    'topic': datas[i]['topic'],
                    'relationship': datas[i]['combine']['relationship'],
                    'familiarity': datas[i]['combine']['familiarity'],
                    'goal1': datas[i]['goal'][0],
                    'goal2': datas[i]['goal'][1],
                    'dialogue': dialogue[-1]
                }
                fw.write(json.dumps(final_dialogues, ensure_ascii=False) + '\n') 

def main(args):
    config = load(open(args.config_path, 'r'))
    print(json.dumps(config, indent=4))
    output_dir = os.path.join(args.output_path, args.data)
    output_path = os.path.join(output_dir, args.output_file)
    os.makedirs(output_dir, exist_ok=True)
    if not args.dg:
        config['run_args']['temperature'] = args.temperature 
        ### dialogue analysis inference
        prompts = data2dainfer_prompt(args, output_path)               
        if prompts: print(prompts[-1]['prompt'])
        if prompts: 
            if args.api:
                api_generate(prompts, config, output_path, args.process_num, args.port, args.tag)
            else:
                llm = LLMPredictor(config)
                llm.prefix_batch_infer(prompts, config, output_path, args.batch_size, args.tag)
    else:
        # dialogue generation inference
        config['run_args']['temperature'] = args.temperature 
        max_try = args.max_try
        llm = LLMPredictor(config) if not args.api else None
        datas = read_jsonl(args.bench_path)
        dialogue_hs = [[] for _ in datas]
        fail_ls, finish_ls = [], []
        final_output_path = output_path
        for turn in range(1, 22):
            print("Dialog Turn: ", turn)
            output_path = os.path.join(output_dir, f"{args.output_file[:-5].strip('.')}_{turn}.jsonl")
            
            for try_num in range(max_try):
                prompts = data2dginfer_prompt(output_path, copy.deepcopy(datas), args, dialogue_hs, turn, fail_ls + finish_ls)
                if prompts: 
                    print("Try num: ", try_num+1)
                    print(prompts[-1]['prompt'])
                    if args.api:
                        api_generate(prompts, config, output_path, args.process_num, args.port, args.tag)
                    else:
                        llm.prefix_batch_infer(prompts, config, output_path, args.batch_size, args.tag)
                else: break
            dialogue_hs, fail_ls, finish_ls = dg_output_process(output_path, args.tag, dialogue_hs, turn, fail_ls, finish_ls)   
            if (len(fail_ls) + len(finish_ls)) == len(datas):
                break 
        dg_result_process(dialogue_hs, datas, final_output_path)

def parse_arguments():
    parser = argparse.ArgumentParser(description='args for step1_infer.py')
    parser.add_argument("--bench_path", type=str, default="data/generation/DIALOG/1109_500_test_zh_final.jsonl")
    parser.add_argument("--config_path", type=str, default="config/qwen2_7b.yaml")
    parser.add_argument("--data", type=str, default="output/1109qwen2_7b")
    parser.add_argument("--output_path", type=str, default="result")
    parser.add_argument("--output_file", type=str, default="cg_zh_infer.jsonl")
    parser.add_argument("--process_num", type=int, default=50)             
    parser.add_argument("--tag", type=str, default="INFER")
    parser.add_argument("--port", type=str, default="8000")
    parser.add_argument("--batch_size", type=int, default=4096)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--max_try", type=int, default=5)
    parser.add_argument("--api", action="store_true", help="Use API")
    parser.add_argument("--dg", action="store_true", help="Dialogue Generation")
    parser.add_argument("--en", action="store_true", help="Use English") 
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_arguments()
    # args.api = True
    # args.dg = True
    print(json.dumps(vars(args), indent=4))
    main(args)
