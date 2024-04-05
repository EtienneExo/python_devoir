import pandas as pd

# Charger les données réelles
# URL du fichier CSV
url = 'https://epistat.sciensano.be/Data/COVID19BE_CASES_MUNI.csv'

# Charger les donnees depuis le fichier CSV
data_reelle = pd.read_csv(url)
data_reelle['CASES'] = data_reelle['CASES'].replace({'<5': '3'}).astype(int)

# Préparer un dictionnaire pour les données réelles par date et commune
data_real_dict = data_reelle.groupby(['DATE', 'TX_DESCR_FR'])['CASES'].sum().to_dict()

# Lire les matrices de probabilités à partir du fichier Excel
all_matrices = pd.read_excel('C:/Users/lucie/Desktop/python_devoir/devoir/Test.xlsx', sheet_name=None)

# Initialiser un dictionnaire pour les estimations
estimations = {}

# Calcul des estimations basé sur les matrices de probabilités
for date, matrix in all_matrices.items():
    prev_date = (pd.to_datetime(date) - pd.Timedelta(days=1)).strftime('%Y-%m-%d')
    if prev_date in data_reelle['DATE'].values:
        estimations[date] = {}
        for dest_commune in matrix.columns[1:]:
            estimated_cases = 0
            for index, row in matrix.iterrows():
                depart_commune = row['Unnamed: 0']
                proba_contamination = row[dest_commune]
                real_cases_prev_day = data_real_dict.get((prev_date, depart_commune), 0)
                estimated_cases += proba_contamination * real_cases_prev_day
            estimations[date][dest_commune] = estimated_cases

# Calcul des taux d'erreur
taux_erreurs_abs = []
for date, communes_estimations in estimations.items():
    for commune, estimation in communes_estimations.items():
        real_cases = data_real_dict.get((date, commune), 0)
        if real_cases > 0:
            erreur_absolue = abs(estimation - real_cases)
            taux_erreur_abs = erreur_absolue / real_cases
            taux_erreurs_abs.append(taux_erreur_abs)

# Moyenne des taux d'erreur
moyenne_taux_erreurs_abs = sum(taux_erreurs_abs) / len(taux_erreurs_abs) if taux_erreurs_abs else 0

# Afficher la moyenne des taux d'erreur
print(f"Moyenne des taux d'erreur: {moyenne_taux_erreurs_abs}")
