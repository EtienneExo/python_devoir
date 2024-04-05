from collections import defaultdict
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# URL du fichier CSV
url = 'https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI.csv'

# Charger les données depuis le fichier CSV
data = pd.read_csv(url)

# Liste des municipalités à filtrer
municipalities = [
    'Anderlecht', 'Auderghem', 'Berchem-Sainte-Agathe', 'Bruxelles', 'Etterbeek',
    'Evere', 'Forest', 'Ganshoren', 'Ixelles', 'Jette', 'Koekelberg',
    'Molenbeek-Saint-Jean', 'Saint-Gilles', 'Saint-Josse-ten-Noode', 'Schaerbeek',
    'Uccle', 'Watermael-Boitsfort', 'Woluwe-Saint-Lambert', 'Woluwe-Saint-Pierre'
]

# Convertir les dates en type datetime pour le filtrage
data['DATE'] = pd.to_datetime(data['DATE'])

# Définir la plage de dates
start_date = datetime(2020, 9, 1)
end_date = datetime(2020, 12, 31)

# Initialiser le dictionnaire de données
data_dict = defaultdict(lambda: {municipality: 0 for municipality in municipalities})

# Filtrer et remplir le dictionnaire
for index, row in data.iterrows():
    if start_date <= row['DATE'] <= end_date and row['TX_DESCR_FR'] in municipalities:
        # Convertir '<5' en 3
        cases = 3 if row['CASES'] == '<5' else int(row['CASES'])
        data_dict[row['DATE'].date()][row['TX_DESCR_FR']] = cases

# Convertir defaultdict en dict pour une meilleure lisibilité/extensibilité
transition_data = {str(date): cases for date, cases in data_dict.items()}

# Créer un mappage des noms de communes vers des identifiants numériques
def get_commune_mapping(data):
    communes = set()  # Crée un ensemble vide pour stocker les noms uniques de communes
    for date, daily_data in data.items():  # Itère sur chaque entrée de date dans les données
        for commune in daily_data.keys():  # Itère sur chaque commune présente pour la date donnée
            communes.add(commune)  # Ajoute le nom de la commune à l'ensemble, garantissant l'unicité
    print(communes)
    return {commune: i for i, commune in enumerate(communes)}  # Crée et retourne un dictionnaire avec les communes comme clés et des ID numériques comme valeurs

# Obtention du mappage des communes vers les ID à partir du dictionnaire de données
commune_mapping = get_commune_mapping(transition_data)
num_communes = len(commune_mapping)

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

# Transformer la matrice de transition en matrice probabiliste
for i in range(num_communes):
    row_sum = np.sum(transition_matrices[i])
    if row_sum > 0:  # Pour éviter la division par zéro
        transition_matrices[i] /= row_sum


# Imprime les matrices de transition
print("Transition matrices:")
for i in range(num_communes):  # Itère sur les lignes de la matrice
    for j in range(num_communes):  # Itère sur les colonnes de la matrice
        #####
        #Ajouter un contrôle pour que la somme soit égale à 1
        ####
        print(f"From {i} to {j}: {transition_matrices[i, j]}")  # Imprime chaque valeur de transition de i vers j


# Créer un graphe dirigé
G = nx.DiGraph()

# Ajouter des nœuds au graphe
for commune in commune_mapping:
    G.add_node(commune)

# Ajouter des arêtes dirigées pondérées au graphe
for i, from_commune in enumerate(commune_mapping):
    for j, to_commune in enumerate(commune_mapping):
        weight = round(transition_matrices[i, j], 3)
        if weight > 0:  # Ajouter une arête seulement si le poids est non nul
            G.add_edge(from_commune, to_commune, weight=weight)

# Dessiner le graphe
pos = nx.spring_layout(G)  # positions pour tous les nœuds
nx.draw(G, pos, with_labels=True)
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Afficher le graphe
plt.show()
