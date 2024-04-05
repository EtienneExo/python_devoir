from collections import defaultdict
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

# URL du fichier CSV
url = 'https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI.csv'

# Charger les données depuis le fichier CSV
data = pd.read_csv(url)

# Convertir les cas "<5" en 3 pour avoir un entier
data['CASES'] = data['CASES'].replace('<5', '3').astype(int)

# Liste des municipalités à filtrer
municipalities = [
    'Anderlecht', 'Auderghem', 'Berchem-Sainte-Agathe', 'Bruxelles', 'Etterbeek',
    'Evere', 'Forest (Bruxelles-Capitale)', 'Ganshoren', 'Ixelles', 'Jette',
    'Koekelberg', 'Molenbeek-Saint-Jean', 'Saint-Gilles', 'Saint-Josse-ten-Noode',
    'Schaerbeek', 'Uccle', 'Watermael-Boitsfort', 'Woluwe-Saint-Lambert', 'Woluwe-Saint-Pierre'
]

# Filtre les données pour ne garder que les municipalités spécifiées
filtered_data = data[data['TX_DESCR_FR'].isin(municipalities)]

# Calcul de la variation quotidienne des cas par commune
def calculate_daily_variation(data):
    data['DATE'] = pd.to_datetime(data['DATE'])
    data.sort_values(by=['TX_DESCR_FR', 'DATE'], inplace=True)
    data['CASES_PREV_DAY'] = data.groupby('TX_DESCR_FR')['CASES'].shift(1)
    data['VARIATION'] = (data['CASES'] - data['CASES_PREV_DAY']) / data['CASES_PREV_DAY']
    data['VARIATION'].fillna(0, inplace=True)
    variation_by_commune_date = data.pivot(index='DATE', columns='TX_DESCR_FR', values='VARIATION')
    return variation_by_commune_date.fillna(0)

# Ajustement des matrices de transition en fonction de la variation quotidienne des cas
def adjust_transition_matrices(daily_transition_matrices, daily_variation):
    adjusted_matrices = {}
    for date, matrix in daily_transition_matrices.items():
        if date in daily_variation.index:
            variations = daily_variation.loc[date].to_numpy()
            adjusted_matrix = np.array(matrix) * (1 + np.tile(variations, (len(matrix), 1)))
            adjusted_matrices[date] = adjusted_matrix
    return adjusted_matrices

# Exemple d'implémentation du calcul des matrices de transition et des cas réels par jour (à adapter)
daily_transition_matrices = {}  # À définir: calcul ou chargement des matrices de transition quotidiennes
initial_cases = np.array([10, 5, 3, ...])  # Exemple: nombre initial de cas par commune (à ajuster)

# Calcul de la variation quotidienne des cas
daily_variation = calculate_daily_variation(filtered_data)

# Ajustement des matrices de transition
adjusted_matrices = adjust_transition_matrices(daily_transition_matrices, daily_variation)

# Calcul des prédictions ajustées (cette fonction doit être définie selon la structure de vos données)
def calculate_adjusted_predictions(adjusted_matrices, initial_cases):
    predicted_cases = defaultdict(dict)
    current_cases = initial_cases
    for date, adjusted_matrix in sorted(adjusted_matrices.items()):
        current_cases = np.dot(adjusted_matrix, current_cases)
        for i, commune in enumerate(municipalities):
            predicted_cases[date][commune] = current_cases[i]
    return predicted_cases

# Calcul des prédictions ajustées
adjusted_predictions = calculate_adjusted_predictions(adjusted_matrices, initial_cases)

# Afficher ou enregistrer les résultats ajustés
# Définir le chemin du fichier de sortie
# Définir le chemin du fichier de sortie
output_file_path = 'Test.xlsx'

# Utiliser ExcelWriter de pandas pour écrire dans un fichier Excel
with pd.ExcelWriter(output_file_path) as writer:
    for date, predictions in adjusted_predictions.items():
        # Convertir les prédictions du jour en DataFrame
        predictions_df = pd.DataFrame(predictions, index=[date])
        predictions_df.index.name = "Date"
        # Transposer le DataFrame pour avoir les communes de départ en lignes
        predictions_df = predictions_df.T
        # Écrire le DataFrame dans un onglet nommé d'après la date
        predictions_df.to_excel(writer, sheet_name=str(date))
        
print(f"Les résultats ajustés ont été enregistrés dans le fichier '{output_file_path}'.")