import json

n = 3784

with open(f'./data/available_inds_12_12.json', 'w') as f:
    json.dump(list(range(n)), f)