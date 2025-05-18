import json

file = './cloudprac_active.json'

with open(file, 'w') as f:
    l = json.load(f)

print(l)