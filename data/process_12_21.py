import pandas as pd    
import json

jsonObj = pd.read_json(path_or_buf='./data/rag_lab_med_engine_responses_12-20.jsonl', lines=True)

jsonL = jsonObj.to_dict(orient='records')

def replace_between(string, start_substring="<<SYS>>", end_substring="<</SYS>>"):
    start_index = string.find(start_substring) - len(start_substring)
    end_index = string.find(end_substring) + len(end_substring)
    
    if start_index != -1 and end_index != -1:
        return string[:start_index + len(start_substring)] + '' + string[end_index:]
    else:
        return string

def process_prompt(prompt):

    # prompt = prompt[prompt.index("<</SYS>>")+9:]
    # prompt = prompt.replace("[/INST]", "\n\n")
    # prompt = prompt.replace("[INST]", "\n\n")

    # while "<<SYS>>" in prompt:
    #     prompt = replace_between(prompt)
        
    prompt = prompt.replace("[/INST]", "\n\n")
    prompt = prompt.replace("[INST]", "\n\n")
    
    return prompt

for i, item in enumerate(jsonL[:]):
    new_item = {}
    new_item['prompt_id'] = item['prompt_id']
    new_item['dataset_id'] = item['dataset_id']
    new_item['instruction'] = item['instruction']
    new_item['human_readable_transcript'] = process_prompt(item['instruction'])
    new_item['responses'] = item['responses']

    print(i)

    with open(f'./data/processed_12_21/{item["prompt_id"]}.json', 'w') as f:
        json.dump(new_item, f, indent=4)


