from collections import defaultdict
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# URL du fichier CSV
url = 'https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI.csv'

# Charger les donnees depuis le fichier CSV
data = pd.read_csv(url)

# Liste des municipalites a filtrer
municipalities = [
    'Anderlecht', 'Auderghem', 'Berchem-Sainte-Agathe', 'Bruxelles', 'Etterbeek',
    'Evere', 'Forest (Bruxelles-Capitale)', 'Ganshoren', 'Ixelles', 'Jette', 'Koekelberg',
    'Molenbeek-Saint-Jean', 'Saint-Gilles', 'Saint-Josse-ten-Noode', 'Schaerbeek',
    'Uccle', 'Watermael-Boitsfort', 'Woluwe-Saint-Lambert', 'Woluwe-Saint-Pierre'
]

# Convertir les dates en type datetime pour le filtrage
data['DATE'] = pd.to_datetime(data['DATE'])

# Definir la plage de dates
start_date = datetime(2020, 9, 1)
end_date = datetime(2020, 12, 31)

# Initialiser le dictionnaire de donnees
data_dict = defaultdict(lambda: {municipality: 0 for municipality in municipalities})

# Filtrer et remplir le dictionnaire
for index, row in data.iterrows():
    if start_date <= row['DATE'] <= end_date and row['TX_DESCR_FR'] in municipalities:
        # Convertir '<5' en 3
        cases = 3 if row['CASES'] == '<5' else int(row['CASES'])
        data_dict[row['DATE'].date()][row['TX_DESCR_FR']] = cases

# Convertir defaultdict en dict pour une meilleure lisibilite/extensibilite
transition_data = {str(date): cases for date, cases in data_dict.items()}

# Creer un mappage des noms de communes vers des identifiants numeriques
def get_commune_mapping(data):
    communes = set()  # Cree un ensemble vide pour stocker les noms uniques de communes
    for date, daily_data in data.items():  # Itere sur chaque entree de date dans les donnees
        for commune in daily_data.keys():  # Itere sur chaque commune presente pour la date donnee
            communes.add(commune)  # Ajoute le nom de la commune a l'ensemble, garantissant l'unicite
    return {commune: i for i, commune in enumerate(communes)}  # Cree et retourne un dictionnaire avec les communes comme cles et des ID numeriques comme valeurs

# Obtention du mappage des communes vers les ID a partir du dictionnaire de donnees
commune_mapping = get_commune_mapping(transition_data)
num_communes = len(commune_mapping)

prior_probabilities = np.full(num_communes, 1 / num_communes)
max_iterations = 100  # Nombre maximal d'iterations pour l'algorithme de traitement
tolerance = 1e-24  # Seuil de tolerance pour verifier la convergence de l'algorithme

#Formule pour Espérance
# Ajuster la fonction d'étape E pour une meilleure mise à jour basée sur les cas réels
def etape_E(transition_matrix_for_day, daily_data, commune_mapping, num_communes):
    # Initialisation de la matrice des transitions estimées
    estimated_transitions = np.zeros((num_communes, num_communes))
    
    if daily_data:  # Vérifie que les données quotidiennes ne sont pas vides
        daily_data_for_day = next(iter(daily_data.values()))  # Obtient les données du jour concerné

        for i in range(num_communes):
            commune_from = list(commune_mapping.keys())[list(commune_mapping.values()).index(i)]
            cases_from = daily_data_for_day.get(commune_from, 0) + 1  # Ajout d'une constante pour éviter la division par zéro

            for j in range(num_communes):
                commune_to = list(commune_mapping.keys())[list(commune_mapping.values()).index(j)]
                cases_to = daily_data_for_day.get(commune_to, 0) + 1  # De même, ajout d'une constante

                # Si le nombre de cas est le même pour les communes de départ et d'arrivée,
                # considérez cela comme un indicateur de taux de contamination interne élevé ou de stase.
                if cases_from == cases_to:
                    estimated_transitions[i, j] = cases_from
                else:
                    # Sinon, utilisez la différence absolue des cas comme auparavant
                    difference_cases = abs(cases_to - cases_from)
                    estimated_transitions[i, j] = difference_cases

        # Normalisation pour que chaque ligne somme à 1
        for i in range(num_communes):
            row_sum = np.sum(estimated_transitions[i])
            if row_sum > 0:  # Pour éviter la division par zéro dans la normalisation
                estimated_transitions[i] /= row_sum

    return estimated_transitions
    

#Formule pour la maximisation
def etape_M(estimated_transitions, num_communes):
    new_transition_matrices = np.copy(estimated_transitions)
    
    for i in range(num_communes):
        row_sum = np.sum(new_transition_matrices[i])
        if row_sum > 0:
            new_transition_matrices[i] /= row_sum
        else:
            # Gérer le cas où la somme est zéro en attribuant des probabilités égales
            # Cela pourrait arriver si estimated_transitions est incorrecte; ajustez selon le besoin
            new_transition_matrices[i] = np.ones(num_communes) / num_communes
    
    return new_transition_matrices

# Conversion des dates en type datetime pour le filtrage
data['DATE'] = pd.to_datetime(data['DATE'])

# Définition de la plage de dates
start_date = datetime(2020, 9, 1)
end_date = datetime(2020, 12, 31)

# Création d'un dictionnaire pour stocker les matrices de transition quotidiennes
daily_transition_matrices = {}

# Itérer sur chaque jour dans la plage de dates spécifiée
for single_date in pd.date_range(start_date, end_date):
    # Formatage de la date pour utilisation comme clé
    date_key = single_date.strftime('%Y-%m-%d')

    # Vérifier si des données existent pour cette date
    if date_key in transition_data:
        # Initialisation de la matrice de transition pour le jour actuel
        transition_matrix_for_day = np.full((num_communes, num_communes), 1 / num_communes)

        # Appliquer l'Algorithme EM pour ce jour spécifique
        for iteration in range(max_iterations):
            estimated_transitions = etape_E(transition_matrix_for_day, {date_key: transition_data[date_key]}, commune_mapping, num_communes)
            new_transition_matrix = etape_M(estimated_transitions, num_communes)
            
            # Vérifier la convergence
            delta = np.linalg.norm(new_transition_matrix - transition_matrix_for_day)
            if delta < tolerance:
                print(delta-tolerance)
                print(f'Convergence atteinte après {iteration + 1} itérations pour la date {date_key}.')
                break
            transition_matrix_for_day = new_transition_matrix

        # Stocker la matrice ajustée pour le jour courant dans le dictionnaire
        daily_transition_matrices[date_key] = transition_matrix_for_day
    else:
        print(f'Pas de données pour la date {date_key}, sautée.')

# print("Résultats des Matrices de Transition Quotidiennes:")
# for date, matrix in daily_transition_matrices.items():
#     print(f"\nDate: {date}")
#     print("Matrice de transition:")
#     for row in matrix:
# #         # Imprime chaque ligne de la matrice de transition, formatée pour une meilleure lisibilité
#         print(' '.join(['{:.4f}'.format(val) for val in row]))

# # Creer un graphe dirige
# G = nx.DiGraph()

# # Ajouter des noeuds au graphe
# for commune in commune_mapping:
#     G.add_node(commune)

# # Ajouter des aretes dirigees ponderees au graphe
# for i, from_commune in enumerate(commune_mapping):
#     for j, to_commune in enumerate(commune_mapping):
#         weight = round(transition_matrices[i, j], 3)
#         if weight > 0:  # Ajouter une arete seulement si le poids est non nul
#             G.add_edge(from_commune, to_commune, weight=weight)

# # Dessiner le graphe
# pos = nx.spring_layout(G)  # positions pour tous les noeuds
# nx.draw(G, pos, with_labels=True)
# edge_labels = nx.get_edge_attributes(G, 'weight')
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# # Afficher le graphe
# plt.show()

with pd.ExcelWriter('Test.xlsx', engine='openpyxl') as writer:
    # Parcourir le dictionnaire de matrices de transition quotidiennes
    for date, matrix in daily_transition_matrices.items():
        # Convertir la matrice numpy en DataFrame de pandas pour l'exportation
        df = pd.DataFrame(matrix)
        # Nommer les colonnes et les index selon les noms des municipalités pour plus de clarté
        df.columns = list(commune_mapping.keys())
        df.index = list(commune_mapping.keys())
        # Écrire le DataFrame dans un nouvel onglet du fichier Excel, avec le nom de l'onglet égal à la date
        df.to_excel(writer, sheet_name=date)

print("Les matrices de transition ont été enregistrées dans le fichier Excel 'Test.xlsx'")

def prevoir_cases_suivant(daily_case_matrices, daily_transition_matrices):
    predicted_cases = {}
    sorted_dates = sorted(daily_case_matrices.keys())
    
    for i, date in enumerate(sorted_dates[:-1]):  # Pas de prédiction pour le dernier jour car nous n'avons pas de matrice de transition
        current_cases = np.array(list(daily_case_matrices[date].values()))
        next_date = sorted_dates[i + 1]
        transition_matrix = daily_transition_matrices[date]
        predicted_cases[next_date] = np.dot(transition_matrix, current_cases)
        
    return predicted_cases