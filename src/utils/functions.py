import functools
import os
from typing import Any, Dict
import json
import yaml
import random
from tqdm import tqdm
import uuid
import re


# ===========================================================================
# code for universal functions
# ===========================================================================
class ExtLoaderMeta(type):
    def __new__(metacls: Any, __name__: str, __bases__: Any, __dict__: Dict) -> Any:
        """Add include constructer to class."""

        # register the include constructor on the class
        cls = super().__new__(metacls, __name__, __bases__, __dict__)
        cls.add_constructor("!include", cls.construct_include)

        return cls


class ExtLoader(yaml.Loader, metaclass=ExtLoaderMeta):
    """YAML Loader with `!include` constructor."""

    def __init__(self, stream: Any) -> None:
        """Initialise Loader."""

        try:
            self._root = os.path.split(stream.name)[0]
        except AttributeError:
            self._root = os.path.curdir

        super().__init__(stream)

    def construct_include(self, node: Any) -> str:
        """Include file referenced at node."""

        filename = os.path.abspath(
            os.path.join(self._root, str(self.construct_scalar(node)))
        )
        extension = os.path.splitext(filename)[1].lstrip(".")

        with open(filename, "r") as f:
            if extension in ("yaml", "yml"):
                return yaml.load(f, ExtLoader)
            else:
                return "".join(f.readlines())


# Set MyLoader as default.
load = functools.partial(yaml.load, Loader=ExtLoader)

def read_jsonl(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return [json.loads(line) for line in file]

def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def read_txt_lines(file_path):
    # 使用 with 语句打开文件，以确保文件在操作后关闭
    with open(file_path, 'r', encoding='utf-8') as file:
        # 使用列表推导式读取每一行并去除前后空白字符
        lines = [line.strip() for line in file]
    return lines

def random_choice(lst):
    return random.choice(lst) if lst else None

def extract_json(text):
    result = text.split("```json")[-1].split("```")[0]
    if result: return result
    else: return text 

def parse_json(text):
    """Try to parse text as JSON. Return parsed_json and whether it was successful."""
    try:
        return json.loads(text), True
    except json.JSONDecodeError:
        start_index = text.find("{")
        end_index = text.rfind("}")
        if start_index != -1 and end_index != -1:
            try:
                return json.loads(text[start_index:end_index + 1]), True
            except json.JSONDecodeError:
                return text[start_index:end_index + 1], False
        return text, False

# ===========================================================================
# code for step1 building goal and scenario prompts
# ===========================================================================


# ===========================================================================
# code for step2 building persona prompts
# ===========================================================================

# ===========================================================================
# code for step3 json data extraction
# ===========================================================================
def element_check(item, tag):
    if tag == 'G&S':
        gs = item[tag]
        return {
            'goal': [gs['goal']['person'][0]['goal1'], gs['goal']['person'][1]['goal2']],
            'goal_type': gs['type'],
            'time': gs['context']['time'],
            'location': gs['context']['location'],
            'topic': gs['context']['topic'],
            'atmosphere': gs['context']['atmosphere'],
            'domain': gs['domain']
        }
    elif tag == 'background':
        person = item
        background = item[tag]
        return {
            'name': person['name'],
            'gender': person['gender_identity'],
            'age': person['age'],
            'social_skill': person['social_skill'],
            'big_five': person['big_five'],
            'moral': person['moral'],
            'moral_value': person['moral_value'],
            'value': person['value'],
            'decision_style': person['decision_style'],
            'action': person['action'],
            'inspiring_prompt': person['inspiring_prompt'],
            'background': background['background'],
            'hobby': background['persona']['hobby'],
            'education': background['persona']['education'],
            'occupation': background['persona']['occupation'],
            'culture': background['persona']['culture'],
            'relationship': background['persona']['relationship'],
            'speaking_style': background['persona']['speaking_style']
        }
    elif tag == 'combine':
        combine = item[tag]
        if (isinstance(combine['result'], str) and combine['result'].lower() == 'true') or combine['result'] is True:
            return {
                'result' : combine['result'],
                'relationship': combine['relationship'],
                'familiarity': combine['familiarity'],
                'talkway': combine['talkway']
            }
        else:
            raise ValueError("Result is false or not found.")
    
    elif tag == 'dialogue':
        dialogue = item[tag]
        return {
            'dialogue': dialogue['dialogue'],
            'workflow': dialogue['workflow'],
            'summary': dialogue['summary'],
            'goal_completion': dialogue['goal_completion'],
        }
    
    elif tag == 'cycle_g':
        dialogue = item
        return {
            'person': dialogue['person'],
            'content': dialogue['content']
        }
    
    elif tag == 'cycle_psg_a':
        analysis = item
        return {
            "persona":{
                "participant1":{
                    "name": analysis['persona']['participant1']['name'],
                    "gender": analysis['persona']['participant1']['gender'],
                    "age": analysis['persona']['participant1']['age'],
                    "big_five": analysis['persona']['participant1']['big_five'],
                    "education": analysis['persona']['participant1']['education'],
                    "occupation": analysis['persona']['participant1']['occupation'],
                    "culture": analysis['persona']['participant1']['culture'],
                    "speaking_style": analysis['persona']['participant1']['speaking_style'],
                    "hobby": analysis['persona']['participant1']['hobby']                              
                },
                "participant2":{
                    "name": analysis['persona']['participant2']['name'],
                    "gender": analysis['persona']['participant2']['gender'],
                    "age": analysis['persona']['participant2']['age'],
                    "big_five": analysis['persona']['participant2']['big_five'],
                    "education": analysis['persona']['participant2']['education'],
                    "occupation": analysis['persona']['participant2']['occupation'],
                    "culture": analysis['persona']['participant2']['culture'],
                    "speaking_style": analysis['persona']['participant2']['speaking_style'],
                    "hobby": analysis['persona']['participant2']['hobby'] 
                }
            }}
    
    elif tag == 'cycle_u_a':
        analysis = item
        return {
            "dialogue": [{
                'person': dialogue['person'],
                'content': dialogue['content'],
                'intent': dialogue['intent'],
                'sentiment': dialogue['sentiment'],
                'emotion': dialogue['emotion'],
                'stance': dialogue['stance'],
                'strategy': dialogue['strategy']
            } for dialogue in analysis['dialogue']]
        }
    
    elif tag == 'score':
        return {
            "reason": item['reason'],
            "score": int(item['score'])
        } 
        

def process_json_file(input_data, output_path, tag, dataset):
    success_num = 0
    fail_num = 0
    with open(input_data, 'r', encoding='utf-8', errors='ignore') as fr, open(output_path, 'a', encoding='utf-8') as fw:
        for line in tqdm(fr):
            try:
                js = json.loads(line)
                text = js.get(tag, '')
                json_text = extract_json(text)
                result, success = parse_json(json_text)

                if success:
                    try:
                        js[tag] = result
                        element_check(js, tag)
                        if tag not in ['dialogue', 'infer']:
                            js['uuid'] = str(uuid.uuid1())
                            js['dataset'] = dataset
                        fw.write(json.dumps(js, ensure_ascii=False) + '\n')
                        success_num += 1
                    except:
                        fail_num += 1
                    
                else:
                    fail_num += 1
            except:
                continue
    total = success_num + fail_num
    print(f'Total: {total}')
    print(f'Success: {success_num}, Ratio: {success_num / total:.2f}')
    print(f'Fail: {fail_num}, Ratio: {fail_num / total:.2f}')

# Function to process evaluation JSON string and extract scores using regex
def process_eval_json(json_string):
    pattern = r'"([\w\s]+)":\s*{\s*"reason":\s*(?:<([^>]+)>|"([^"]+)"),\s*"score":\s*(<?\d+>?)\s*}'
    matches = re.findall(pattern, json_string, re.DOTALL)
    result = {}
    for category, reason1, reason2, score in matches:
        reason = reason1 or reason2
        score = score.strip('<>')
        result[category.strip()] = {
            "reason": reason.strip(),
            "score": int(score)
        }
    return result

# ===========================================================================
# code for step4 combine and define goal, scenario and persona prompts
# ===========================================================================

# ===========================================================================
# code for step5 building dialog generation prompts
# ===========================================================================

# ===========================================================================
# code for step6 transforming data to format
# ===========================================================================


# ===========================================================================
# code for inference
# ===========================================================================
  
# ===========================================================================
# code for evaluation
# ===========================================================================

# ===========================================================================
# code for result statistics
# ===========================================================================