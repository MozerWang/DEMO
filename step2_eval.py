import os
from src.utils.functions import load, read_jsonl, process_eval_json
from src.utils.generate import api_generate, LLMPredictor
from src.utils.eval_prompt import *
import json
import argparse
import uuid
import random

def build_da_prompt(item, num_dict):
    prompts = []
    
    def create_prompt(key, instruction, prediction, answer):
        prompt_template = {
            'persona': eval_persona,
            'goal': eval_goal,
            'scene': eval_scene,
            'utterance': eval_utterance
        }.get(key)
        if key == 'persona':
            instruction = instruction.split("\n```json")[0]
            input_prompt = prompt_template.format(instruction=instruction, prediction=prediction, answer=answer)
        else:
            input_prompt = prompt_template.format(prediction=prediction, answer=answer)    
        
        return {
            'id': item['id'],
            'uuid': item['uuid'],
            'prompt': {'system': "", 'user': input_prompt},
            'answer': answer,
            'prediction': prediction,
            'key': key
        }

    prompts.append(create_prompt(item['type'], item['prompt']['user'], item['INFER'], item['answer']))
    num_dict[item['type']] += 1
    return prompts, num_dict


def fail_discover(prompts, output_path, tag, is_dg):
    existing_datas = read_jsonl(output_path)
    finish_ls = []
    finish_datas = []
    random.shuffle(existing_datas)
    for existing_data in existing_datas:
        unique_index = str(existing_data.get('uuid')) + str(existing_data.get('id'))
        
        if existing_data[tag] and process_eval_json(existing_data[tag]) and (unique_index not in finish_ls):
            finish_datas.append(existing_data)
            finish_ls.append(unique_index)

    with open(output_path, 'w', encoding='utf-8') as fw:
        for item in finish_datas:
            fw.write(json.dumps(item, ensure_ascii=False) + '\n')

    infer_prompts = []
    for item in prompts:
        unique_index = str(item.get('uuid')) + str(item.get('id'))
        if unique_index not in finish_ls:
            infer_prompts.append(item)
        else:
            continue
    return infer_prompts

def data2daeval_prompt(args):
    datas = read_jsonl(args.result_path)
    prompts = []
    num_dict = {"persona":0,"scene":0,"goal":0,"utterance":0}
    for item in datas:
        temp_prompts, num_dict= build_da_prompt(item, num_dict)
        prompts.extend(temp_prompts)
    print(json.dumps(num_dict, indent=4))
    return prompts

def data2dgeval_prompt(args):
    datas = read_jsonl(args.result_path)
    prompts = []
    for item in datas:
        prompt = eval_dg
        prompt_js = item.copy()
        try:
            item['familiarity'] = Familiar_map[str(item['familiarity'])][1] if args.en else Familiar_map[str(item['familiarity'])][0]
        except:
            item['familiarity'] = item['familiarity']    
        prompt_js['prompt'] = {'system': "", 'user': eval_dg.format(result=item)}
        prompts.append(prompt_js)
    return prompts

def main(args):
    output_dir = os.path.join(args.output_path, args.data)
    output_path = os.path.join(output_dir, args.output_file)
    os.makedirs(output_dir, exist_ok=True)
    config = load(open(args.config_path, 'r'))
    print(json.dumps(config, indent=4))

    prompts = data2dgeval_prompt(args) if args.dg else data2daeval_prompt(args)
    prompts = fail_discover(prompts, output_path, args.tag, args.dg) if os.path.exists(output_path) else prompts           
    if prompts: 
        print(prompts[-1]['prompt'])
        api_generate(prompts, config, output_path, args.process_num, args.port, args.tag)
    print('Finish!!')

def parse_arguments():
    parser = argparse.ArgumentParser(description='args for step2_eval.py')
    parser.add_argument("--result_path", type=str, default="final_result/output/1104qwen2_7b_self/ca_en_infer_extract.jsonl")
    parser.add_argument("--config_path", type=str, default="config/gpt_4o.yaml")
    parser.add_argument("--data", type=str, default="eval/1104qwen2_7b_self")
    parser.add_argument("--output_path", type=str, default="result")
    parser.add_argument("--output_file", type=str, default="ca_en_eval.jsonl")
    parser.add_argument("--process_num", type=int, default=1)             
    parser.add_argument("--tag", type=str, default="eval")
    parser.add_argument("--port", type=str, default="8000")
    parser.add_argument("--batch_size", type=int, default=2048)
    parser.add_argument("--dg", action="store_true", help="Dialogue generation")
    parser.add_argument("--en", action="store_true", help="Use English")  
    args = parser.parse_args()
    print(json.dumps(vars(args), indent=4))
    return args

if __name__ == "__main__":
    args = parse_arguments()
    args.en = True
    main(args)
