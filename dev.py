import json

file = "./cloudprac_active.json"
keyword = 'advisor'

with open(file, 'r') as fp:
    bytes = json.load(fp)

ps = [b for b in bytes if keyword in b['question'].lower() or keyword in b['answer'].lower()]

with open(f'./cloudprac_{keyword}_active.json', 'w') as fp:
    json.dump(ps, fp)