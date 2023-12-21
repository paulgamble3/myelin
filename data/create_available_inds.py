import json

n = 2320

with open(f'./data/available_inds_12_21.json', 'w') as f:
    json.dump(list(range(n)), f)