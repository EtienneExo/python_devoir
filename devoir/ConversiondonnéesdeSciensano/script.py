"""
1. Conversion données de Sciensano

Bien regarder quel fichier prendre sur le site de sciensano
https://epistat.wiv-isp.be/covid/

2022.
"""

# Import (si ne fonctionne pas, executer le fichier 'requirement.bat' en racine (mode admin ?)
import json
import random
from colorama import *

init(autoreset=True)
import datetime

import collections


def makehash():  # Pour les dict a plusieurs niveaux
    return collections.defaultdict(makehash)


# -----------------------------------#
# Récupération données sur Sciensano #
# -----------------------------------#

print("=====================================================")
print(Fore.YELLOW + "1. Conversion données de Sciensano")
print("=====================================================")

# DateTime pour enregistrer le temps que le fichier va mettre
tempsDepart = datetime.datetime.now()

# Ouverture du fichier
try:
    file = open("COVID19BE_CASES_MUNI.json", "r", encoding='utf8').read()
except:
    print(Fore.RED + "Erreur :")
    print("Impossible de trouver le fichier : " + Fore.CYAN + "COVID19BE_CASES_MUNI.json")
    input()
    quit()

print("Fichier : " + Fore.CYAN + "COVID19BE_CASES_MUNI.json" + Fore.RESET + " trouvé.")
print()

# Conversion du fichier
data = json.loads(file)
print("Fichier converti")

print("Il y a " + Fore.YELLOW + str(len(data)) + Fore.RESET + " entrées.")
print('')

"""
Data (fichier JSON) est constitué comme suit:
C'est une list qui contient des dictionnaires.
Dans ces dictionnaires on sait accèder aux valeurs grace à ces clés :

NIS5
DATE
TX_DESCR_NL
TX_DESCR_FR
TX_ADM_DSTR_DESCR_NL
TX_ADM_DSTR_DESCR_FR
PROVINCE
REGION
CASES

"""
"""
Anderlecht, Auderghem, Berchem-Sainte-Agathe, Bruxelles, Etterbeek, Evere, Forest, Ganshoren, Ixelles, Jette, 
Koekelberg, Molenbeek-Saint-Jean, Saint-Gilles, Saint-Josse-ten-Noode, Schaerbeek, Uccle, Watermael-Boitsfort, 
Woluwe-Saint-Lambert, Woluwe-Saint-Pierre.
"""

print("Creation du json pour les 19 communes de Bruxelles suivantes : "
      + Fore.MAGENTA
      + "Anderlecht, Auderghem, Berchem-Sainte-Agathe, Bruxelles, Etterbeek, Evere, Forest, Ganshoren, Ixelles, Jette,"
        " Koekelberg, Molenbeek-Saint-Jean, Saint-Gilles, Saint-Josse-ten-Noode, Schaerbeek, Uccle, "
        "Watermael-Boitsfort, Woluwe-Saint-Lambert, Woluwe-Saint-Pierre.")

"""
On crée un dictionnaire (nested dict a plusieurs niveaux) dont la clé est la date, car c'est l'élement commun entre chaque noeuds.
"""
dicoMatrix = makehash()
for item in data:

    if item.get("TX_DESCR_FR") == "Anderlecht":
        dicoMatrix[item.get('DATE')]['Anderlecht'] = item.get('CASES')

    if item.get("TX_DESCR_FR") == "Auderghem":
        dicoMatrix[item.get('DATE')]['Auderghem'] = item.get('CASES')

    if item.get("TX_DESCR_FR") == "Berchem-Sainte-Agathe":
        dicoMatrix[item.get('DATE')]['Berchem-Sainte-Agathe'] = item.get('CASES')

    if item.get("TX_DESCR_FR") == "Bruxelles":
        dicoMatrix[item.get('DATE')]['Bruxelles'] = item.get('CASES')

    if item.get("TX_DESCR_FR") == "Etterbeek":
        dicoMatrix[item.get('DATE')]['Etterbeek'] = item.get('CASES')

    if item.get("TX_DESCR_FR") == "Evere":
        dicoMatrix[item.get('DATE')]['Evere'] = item.get('CASES')

    if item.get("TX_DESCR_FR") == "Forest":
        dicoMatrix[item.get('DATE')]['Forest'] = item.get('CASES')

    if item.get("TX_DESCR_FR") == "Ganshoren":
        dicoMatrix[item.get('DATE')]['Ganshoren'] = item.get('CASES')

    if item.get("TX_DESCR_FR") == "Ixelles":
        dicoMatrix[item.get('DATE')]['Ixelles'] = item.get('CASES')

    if item.get("TX_DESCR_FR") == "Jette":
        dicoMatrix[item.get('DATE')]['Jette'] = item.get('CASES')

    if item.get("TX_DESCR_FR") == "Koekelberg":
        dicoMatrix[item.get('DATE')]['Koekelberg'] = item.get('CASES')

    if item.get("TX_DESCR_FR") == "Molenbeek-Saint-Jean":
        dicoMatrix[item.get('DATE')]['Molenbeek-Saint-Jean'] = item.get('CASES')

    if item.get("TX_DESCR_FR") == "Saint-Gilles":
        dicoMatrix[item.get('DATE')]['Saint-Gilles'] = item.get('CASES')

    if item.get("TX_DESCR_FR") == "Saint-Josse-ten-Noode":
        dicoMatrix[item.get('DATE')]['Saint-Josse-ten-Noode'] = item.get('CASES')

    if item.get("TX_DESCR_FR") == "Schaerbeek":
        dicoMatrix[item.get('DATE')]['Schaerbeek'] = item.get('CASES')

    if item.get("TX_DESCR_FR") == "Uccle":
        dicoMatrix[item.get('DATE')]['Uccle'] = item.get('CASES')

    if item.get("TX_DESCR_FR") == "Watermael-Boitsfort":
        dicoMatrix[item.get('DATE')]['Watermael-Boitsfort'] = item.get('CASES')

    if item.get("TX_DESCR_FR") == "Woluwe-Saint-Lambert":
        dicoMatrix[item.get('DATE')]['Woluwe-Saint-Lambert'] = item.get('CASES')

    if item.get("TX_DESCR_FR") == "Woluwe-Saint-Pierre":
        dicoMatrix[item.get('DATE')]['Woluwe-Saint-Pierre'] = item.get('CASES')

print()
print("Enregistrement du fichier : " + Fore.CYAN + "'COVID_5BXL.JSON'")

try:
    file = open('COVID_19BXL.json', 'w', encoding='utf8')
    file.write(json.dumps(dicoMatrix))
    file.close()
except:
    print(Fore.RED + "Erreur :")
    print(Fore.RED + "Impossible d'enregistrer le fichier...")
    input()
    quit()

print("Fichier enregistré !")

tempsFin = datetime.datetime.now()
tempsTotal = tempsFin - tempsDepart
print("Effectué en " + Fore.YELLOW + str(tempsTotal) + Fore.RESET + " millisecondes.")

# ------------------------------#
# Parser JSON pour les CASES <5 #
# ------------------------------#

print()
print("début du parser JSON")

try:
    file = open("../1. Conversion données de Sciensano/COVID_19BXL.json", "r", encoding='utf8').read()
except:
    print(Fore.RED + "Erreur :")
    print("Impossible de trouver le fichier : " + Fore.CYAN + "COVID19BE_CASES_MUNI.json")
    input()
    quit()

print("Fichier : " + Fore.CYAN + "COVID19BE_CASES_MUNI.json" + Fore.RESET + " trouvé.")
print()

data = json.loads(file)

for x, values in data.items():
    for y, cases in values.items():
        if cases == "<5":
            new_cases = str(random.randint(0, 4))
            data[x][y] = new_cases

updated_json_data = json.dumps(data)

try:
    file = open('../1. Conversion données de Sciensano/COVID_19BXL.json', 'w', encoding='utf8')
    file.write(json.dumps(data))
    file.close()
except:
    print(Fore.RED + "Erreur :")
    print(Fore.RED + "Impossible d'enregistrer le fichier...")
    input()
    quit()

print("Fichier enregistré !")

tempsFin = datetime.datetime.now()
tempsTotal = tempsFin - tempsDepart
print("Effectué en " + Fore.YELLOW + str(tempsTotal) + Fore.RESET + " millisecondes.")
print()

print("Fin Parser JSON")
