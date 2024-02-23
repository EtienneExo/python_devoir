import json
import numpy as np

# Charger les données JSON
def load_transition_data_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)  # Lit le fichier JSON et convertit en structure de données Python
    return data  # Retourne la structure de données chargée

# Créer un mappage des noms de communes vers des identifiants numériques
#######
## Ajouter une règle pour modifier les "<5" !!
#######
def get_commune_mapping(data):
    communes = set()  # Crée un ensemble vide pour stocker les noms uniques de communes
    for date, daily_data in data.items():  # Itère sur chaque entrée de date dans les données
        for commune in daily_data.keys():  # Itère sur chaque commune présente pour la date donnée
            communes.add(commune)  # Ajoute le nom de la commune à l'ensemble, garantissant l'unicité
    print(communes)
    return {commune: i for i, commune in enumerate(communes)}  # Crée et retourne un dictionnaire avec les communes comme clés et des ID numériques comme valeurs

# Charger les données
transition_data_path = "C:\\Math\\devoir\\1.ConversiondonnéesdeSciensano\\COVID_19BXL.json"
transition_data = load_transition_data_from_json(transition_data_path)  # Appelle la fonction pour charger les données JSON

# Obtenir le mappage des communes vers les ID
commune_mapping = get_commune_mapping(transition_data)  # Appelle la fonction pour obtenir le mappage des communes
num_communes = len(commune_mapping)  # Calcule le nombre de communes uniques

# Initialiser les matrices de transition avec des valeurs aléatoires
transition_matrices = np.random.rand(num_communes, num_communes)  # Crée une matrice avec des valeurs aléatoires pour chaque transition possible entre communes

max_iterations = 100  # Nombre maximal d'itérations pour l'algorithme de traitement
tolerance = 1e-6  # Seuil de tolérance pour vérifier la convergence de l'algorithme

# Boucle d'exemple de traitement
for iteration in range(max_iterations):  # Itère jusqu'à un maximum d'itérations
    # Ici, vous implémenteriez votre algorithme, par exemple, pour mettre à jour `transition_matrices`

    # Vérification de convergence exemple (remplacer par le critère de convergence réel)
    if iteration > 0:  # Vérifie si un critère de convergence est atteint pour arrêter la boucle
        break  # Sort de la boucle si le critère est atteint

# Imprime les matrices de transition
print("Transition matrices:")
for i in range(num_communes):  # Itère sur les lignes de la matrice
    for j in range(num_communes):  # Itère sur les colonnes de la matrice
        #####
        #Ajouter un contrôle pour que la somme soit égale à 1
        ####
        print(f"From {i} to {j}: {transition_matrices[i, j]}")  # Imprime chaque valeur de transition de i vers j