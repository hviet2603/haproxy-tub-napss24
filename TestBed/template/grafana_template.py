import json
import copy
import re

grafana_db_template = 'grafana_individual_cache.json'
with open(grafana_db_template, 'r') as file:
    data = json.load(file)

original_targets = data['dashboard']['panels'][0]['targets']
duplicated_targets = []

for target in original_targets:
    for i in range(1, 21):
        new_target = copy.deepcopy(target)
        if 'expr' in new_target:
            new_target['expr'] = re.sub(r'cache_\d+', f'cache_{i}', new_target['expr'])
        if 'legendFormat' in new_target:
            new_target['legendFormat'] = re.sub(r'\d+', str(i), new_target['legendFormat'])
        if 'refId' in new_target:
            new_target['refId'] = re.sub(r'_\d+', f'_{i}', new_target['refId'])
        if 'expression' in new_target:
            new_target['expression'] = re.sub(r'_\d+', f'_{i}', new_target['expression'])
        duplicated_targets.append(new_target)

data['dashboard']['panels'][0]['targets'] = duplicated_targets

with open('templates/grafana_individual_cache.json', 'w') as file:
    json.dump(data, file, indent=4)