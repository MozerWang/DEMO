import json
from tqdm import tqdm
import multiprocessing
import requests
import numpy as np
from functools import partial
from decimal import Decimal
from openai import OpenAI
import numpy as np
import time

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, bytes):
            try:
                return str(obj, encoding='utf-8')
            except:
                return str(obj, encoding='gbk')
        elif isinstance(obj, Decimal):
            return float(obj)
        # print(obj, type(obj))
        return json.JSONEncoder.default(self, obj)


def get_api_results(prompt_input, config, port):
    prompt = prompt_input['prompt']
    model = config['args']['api_name']
    messages = [{"role": "system", "content": prompt['system']}] if prompt.get('system') else []
    messages.append({"role": "user", "content": prompt['user']})
    
    if config['type'] == 'Azure':
        # Azure API
        headers = {"Content-Type": "application/json",
                "Authorization": config['args']['api_key']}
        raw_info = {
            "model": model,
            "messages": messages,
            "n": 1}
        raw_info.update(config['run_args'])
        try:
            callback = requests.post(config['args']['api_url'], data=json.dumps(raw_info, cls=MyEncoder), headers=headers,
                                    timeout=(60, 60))
            result = callback.json()
            # todo: customize the result
            return result['data']['response']['choices'][0]['message']['content']
        except Exception as e:
            print(e)
            return []
    
    elif config['type'] == 'OpenAI':
        # Set OpenAI's API key and API base to use vLLM's API server.
        client = OpenAI(
            api_key=config['args']['api_key'],
            base_url=config['args']['api_url'].format(port=port),
        )
        try:
            chat_response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=config['run_args']['temperature'],
                timeout=600,
                logprobs=True
            )
            # return chat_response.choices[0].message.model_dump()['content']
            return chat_response.choices[0]
        except Exception as e:
            print(e)
            return []
    
    elif config['type'] == 'dashscope':
        import dashscope
        from dashscope import Generation
        from http import HTTPStatus
        model_name = config['args']['api_name']
        dashscope.api_key = config['args']['api_key']
        dashscope.base_http_api_url = config['args']['api_url']

        try:
            response = Generation.call(
                model_name,
                messages=messages,
                result_format='message',  # set the result to be "message"  format.
            )
            return response.output.choices[0]['message']['content']
        except Exception as e:
            print(e)
            return []
    
    elif config['type'] == 'claude':
        headers = {"Content-Type": "application/json",
                "Authorization": config['args']['api_key']}
        raw_info = {
            "model": model,
            "messages": messages}
        raw_info.update(config['run_args'])
        try:
            callback = requests.post(config['args']['api_url'], data=json.dumps(raw_info, cls=MyEncoder), headers=headers,
                                    timeout=(60, 60))
            result = callback.json()
            # print(result)
            return result['content'][0]['text']
        except Exception as e:
            print(e)
            return []

def fetch_api_result(prompt_input, config, port, max_retries=5):
    """Attempt to get a valid result from the API, with a maximum number of retries."""
    for _ in range(max_retries):
        result = get_api_results(prompt_input, config, port)
        if config['type'] == 'OpenAI' and result.message.content:
            return result
        if result: 
            return result
    return None


def api(prompt, output_path, config, port, tag):
    response_content = fetch_api_result(prompt, config, port)
    result = prompt.copy()

    if config['type'] == 'OpenAI':
        result['logprobs'] = response_content.logprobs.model_dump()['content'] or ""
        result[tag] = response_content.message.content or ""
        if result['logprobs']:
            logprobs = [token.logprob for token in response_content.logprobs.content]
            result['perplexity'] = np.exp(-np.mean(logprobs))
    else:
        result[tag] = response_content or ""
    
    with open(output_path, 'a', encoding='utf-8') as fw:
        fw.write(json.dumps(result, ensure_ascii=False) + '\n')


def api_generate(prompts, config, output_path, process_num, port, tag):
    func = partial(api, output_path=output_path, config=config, port=port, tag=tag)
    with multiprocessing.Pool(processes=process_num) as pool:
        for _ in tqdm(pool.imap(func, prompts), total=len(prompts)):
            pass

####prefix_batch_inference
class LLMPredictor:
    def __init__(self, config: dict):
        # Create an LLM instance with the provided configuration.
        from vllm import LLM
        from transformers import AutoTokenizer
        self.llm = LLM(
            model=config['ckpt'],
            tensor_parallel_size=config['tensor_parallel_size'],
            enable_prefix_caching=config['enable_prefix_caching'],
            gpu_memory_utilization=config['gpu_memory_utilization'],
            # max_num_batched_tokens=config['max_num_batched_tokens'],
            max_num_seqs=config['max_num_seqs'],
            enable_lora=config['lora']
        )
        self.tokenizer = tokenizer = AutoTokenizer.from_pretrained(config['ckpt'])
    
    def batch_process(self, prompts: list[dict], batch_size: int) -> list[tuple]:
        # Split prompts into batches.
        batches = []
        for i in tqdm(range(0, len(prompts), batch_size), total=int((len(prompts)/batch_size))+1, desc="Processing batch"):
            current_batch = prompts[i:i + batch_size]
            formatted_batch = []
            for item in current_batch:
                messages = [{"role": "system", "content": item['prompt']['system']}] if item['prompt'].get('system') else []
                messages.append({"role": "user", "content": item['prompt']['user']})
                formatted_batch.append(self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True))
            batches.append((current_batch, formatted_batch))
        return batches

    def prefix_batch_infer(self, prompts: list[dict], config: dict, output_path: str, batch_size: int, tag: str):
        from vllm import SamplingParams
        # Process the prompts in batches and write results to the output.
        batches = self.batch_process(prompts, batch_size)
        sampling_params = SamplingParams(max_tokens=config['max_tokens'], temperature=config['run_args']['temperature'])
        if config['lora']:
            from vllm.lora.request import LoRARequest
            lora_name = config['lora_name']
            lora_path = config['lora_path']
            print(f'use lora {lora_name}, {lora_path}')
        # Warmup so that the shared prompt's KV cache is computed.
        if config['enable_prefix_caching']:
            if config['lora']:
                self.llm.generate(batches[0][1][0], sampling_params, lora_request=LoRARequest(lora_name, 1, lora_path))
            else:
                self.llm.generate(batches[0][1][0], sampling_params)                
        for batch, batch_inputs in tqdm(batches, total=len(batches), desc="Batch inference"):
            print(batch_inputs[0])
            if config['lora']:
                outputs = self.llm.generate(batch_inputs, sampling_params, lora_request=LoRARequest(lora_name, 1, lora_path))
            else:
                outputs = self.llm.generate(batch_inputs, sampling_params)
            with open(output_path, 'a', encoding='utf-8') as fw:
                for idx, output in enumerate(outputs):
                    result = batch[idx]
                    result.pop('prompt')
                    result[tag] = output.outputs[0].text or ""
                    try:
                        fw.write(json.dumps(result, ensure_ascii=False) + '\n')
                    except Exception as e:
                        print(e)