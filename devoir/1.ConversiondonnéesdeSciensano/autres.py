import json

file = open("COVID19BE_CASES_MUNI.json", 'r', encoding='utf8').read()
file = json.loads(file)

print(file[210000])