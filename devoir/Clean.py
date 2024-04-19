import pandas as pd
import numpy as np

def download_and_clean_data(url):
    # Télécharger les données
    covid_data = pd.read_csv(url)
    
    # Filtrer les données pour la région de Bruxelles
    brussels_data = covid_data[covid_data['REGION'] == 'Brussels']
    
    # Conserver uniquement les colonnes nécessaires
    brussels_data = brussels_data[['NIS5', 'DATE', 'TX_DESCR_FR', 'CASES']]


    
    # Convertir les dates en type datetime
    brussels_data['DATE'] = pd.to_datetime(brussels_data['DATE'])
    
    # Générer une plage de dates complète du début à la fin
    start_date = brussels_data['DATE'].min()
    end_date = brussels_data['DATE'].max()
    date_range = pd.date_range(start=start_date, end=end_date)
    
    # Créer un DataFrame complet pour toutes les dates et communes
    nis5_unique = brussels_data['NIS5'].unique()
    complete_grid = pd.MultiIndex.from_product([nis5_unique, date_range], names=['NIS5', 'DATE']).to_frame(index=False)
    complete_data = pd.merge(complete_grid, brussels_data, on=['NIS5', 'DATE'], how='left')
    
    # Supprimer les lignes où le nom de la commune est NaN
    complete_data = complete_data.dropna(subset=['TX_DESCR_FR'])

    # Remplir les valeurs manquantes
    complete_data['CASES'] = complete_data['CASES'].fillna('0')
    
    # Convertir '<5' en '2.5' et toutes les valeurs de CASES en float
    complete_data['CASES'] = complete_data['CASES'].replace('<5', '2.5').astype(float)
    
    return complete_data

# URL du fichier de données
data_url = 'https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI.csv'

# Appeler la fonction
cleaned_data = download_and_clean_data(data_url)

# Enregistrer le DataFrame nettoyé en fichier Excel
cleaned_data.to_excel('cleaned_data.xlsx', index=False)

print("Les données ont été sauvegardées avec succès en format Excel sous le nom 'cleaned_data.xlsx'.")