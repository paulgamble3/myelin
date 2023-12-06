import pandas as pd
import ast
import json

raw_fn = './data/raw_data_debo_12-6.csv'

raw_df = pd.read_csv(raw_fn)

print(raw_df.head())


def process_conv(conversation):
    #conv_str = ""

    turns = []
    for turn in conversation:

        if turn['role'] == 'user':
            #conv_str += "Patient: " + turn['content'] + "\n\n"
            turns.append("Patient: " + turn['content'])

        if turn['role'] == 'assistant':
            #conv_str += "Nurse: " + turn['content'] + "\n\n"
            turns.append("Nurse: " + turn['content'])

    conv_str = "\n\n".join(turns[-8:])
    return conv_str
        

for i, row in raw_df.iterrows():
    # if i > 3:
    #     break
    conv = row['conversations']
    #conv = process_conv(conv)
    conv = ast.literal_eval(conv)

    conv_str = process_conv(conv)
    gpt4_str = row['gpt-4']
    our_model_str = row['original_model_response']

    item = {
        "prompt_id": i,
        "prompt": conv_str,
        "responses": {
            "gpt4": gpt4_str,
            "our_model": our_model_str
        }
        
    }
    
    with open(f'./data/processed/{i}.json', 'w') as f:
        json.dump(item, f, indent=4)