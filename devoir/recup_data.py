import pandas as pd
from datetime import datetime

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

# Filtrer les données pour les municipalités spécifiées
filtered_municipalities = data[data['TX_DESCR_FR'].isin(municipalities) | data['TX_DESCR_NL'].isin(municipalities)]

# Convertir les dates en type datetime pour le filtrage
filtered_municipalities['DATE'] = pd.to_datetime(filtered_municipalities['DATE'])

# Définir la plage de dates
start_date = datetime(2020, 9, 1)
end_date = datetime(2020, 12, 31)

# Filtrer les données pour la plage de dates spécifiée
final_filtered_data = filtered_municipalities[(filtered_municipalities['DATE'] >= start_date) & (filtered_municipalities['DATE'] <= end_date)]

# Afficher les résultats
print(final_filtered_data)