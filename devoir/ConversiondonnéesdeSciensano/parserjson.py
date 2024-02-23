
import json
import re # !
import random



json_data = '{"2020-03-03": {"Anderlecht": "<5", "Watermael-Boitsfort": "N/A"}, "2020-03-08": {"Anderlecht": "2", "Bruxelles": "<5", "Ixelles": "<5", "Jette": "<5", "Uccle": "N/A"}}'

#  charger les données JSON comme dictionnaire
data = json.loads(json_data)

for x, values in data.items():
    # y=nom, cases=nb pour values
    for y, cases in values.items():
        if cases == "<5":
            # Générer un nombre aleatoire entre 0 et 4 inclus
            new_cases = str(random.randint(0, 4))
            # Remplacer la valeur "<5" par le nombre aléatoire
            data[x][y] = new_cases

updated_json_data = json.dumps(data)
print(updated_json_data)