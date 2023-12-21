import json

n = 1440

with open(f'./data/available_inds_12_21.json', 'w') as f:
    json.dump(list(range(n)), f)