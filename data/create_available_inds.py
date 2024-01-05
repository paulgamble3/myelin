import json

n = 485

with open(f'./data/available_inds_1_5.json', 'w') as f:
    json.dump(list(range(n)), f)