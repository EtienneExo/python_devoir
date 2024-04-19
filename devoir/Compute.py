import numpy as np
import pandas as pd
from scipy import linalg
from sklearn.mixture import GaussianMixture

# Chemin d'accès au fichier Excel avec les données nettoyées
excel_file_path = 'cleaned_data.xlsx'

# Charger les données depuis le fichier Excel
data = pd.read_excel(excel_file_path)



# Définition des proportions initiales pour chaque commune à partir de la répartition réelle de la population
proportions_dict = {
    "Anderlecht": 0.101190902038963,
    "Auderghem": 0.0283790790303975,
    "Berchem-Sainte-Agathe": 0.0206966957793917,
    "Bruxelles": 0.157189422957119,
    "Etterbeek": 0.0398266901926424,
    "Evere": 0.0361072816646102,
    "Forest (Bruxelles-Capitale)": 0.0464986354666141,
    "Ganshoren": 0.0205142220953927,
    "Ixelles": 0.0714806493490834,
    "Jette": 0.0433507634554246,
    "Koekelberg": 0.0181549257846569,
    "Molenbeek-Saint-Jean": 0.0787369927211489,
    "Saint-Gilles": 0.0393484001398697,
    "Saint-Josse-ten-Noode": 0.0215021523052375,
    "Schaerbeek": 0.104382181886874,
    "Uccle": 0.0694018962793857,
    "Watermael-Boitsfort": 0.0203221022254555,
    "Woluwe-Saint-Lambert": 0.048730923662496,
    "Woluwe-Saint-Pierre": 0.0341860829652376
}

# Remplir les noms de commune manquants et trier les données
data['TX_DESCR_FR'] = data['TX_DESCR_FR'].fillna(method='ffill')
data_sorted = data.sort_values(by=['NIS5', 'DATE'])

# Création d'un mappage des noms de commune aux indices numériques
# Liste des communes
communes = [
    'Anderlecht', 'Auderghem', 'Berchem-Sainte-Agathe', 'Bruxelles', 'Etterbeek',
    'Evere', 'Forest (Bruxelles-Capitale)', 'Ganshoren', 'Ixelles', 'Jette', 'Koekelberg',
    'Molenbeek-Saint-Jean', 'Saint-Gilles', 'Saint-Josse-ten-Noode', 'Schaerbeek',
    'Uccle', 'Watermael-Boitsfort', 'Woluwe-Saint-Lambert', 'Woluwe-Saint-Pierre'
]

# Création du dictionnaire commune_to_index
commune_to_index = {commune: index for index, commune in enumerate(communes)}

data_sorted['COMMUNE_INDEX'] = data_sorted['TX_DESCR_FR'].map(commune_to_index)

# Sélectionner les données pour l'algorithme EM
em_data = data_sorted[['COMMUNE_INDEX', 'CASES']].to_numpy()

# Nombre de communes
n_communes = len(commune_to_index)

print(type(commune_to_index))
print(commune_to_index)

def initialize_parameters(commune_to_index, proportions_dict):
    """
    Initialise les paramètres pour l'algorithme EM, y compris les proportions des communes et la matrice de transition.
    
    :param commune_to_index: Dictionnaire associant chaque commune à un indice numérique.
    :param proportions_dict: Dictionnaire des proportions initiales pour chaque commune.
    :return: Dictionnaire contenant les proportions et la matrice de transition initialisées.
    """
    
    # Initialiser les proportions des communes avec les valeurs fournies, ordonnées selon les indices
    initial_proportions = np.array([proportions_dict[commune] for commune in sorted(commune_to_index, key=commune_to_index.get)])
    
    # Initialiser la matrice de transition avec des probabilités uniformes, mais très petites pour chaque transition
    transition_matrix = np.full((n_communes, n_communes), fill_value=1e-4)
    
    # Ajuster les diagonales pour refléter une probabilité plus élevée de rester dans le même état
    np.fill_diagonal(transition_matrix, 1 - transition_matrix.sum(axis=1) + transition_matrix.diagonal())
    
    return {
        'proportions': initial_proportions,
        'transition_matrix': transition_matrix
    }


# Initialisation des paramètres
parameters = initialize_parameters(n_communes, proportions_dict)


def e_step(data, parameters):
    """
    Étape E de l'algorithme EM.
    Calcule les responsabilités en fonction des paramètres actuels.

    :param data: Données observées, array numpy des cas.
    :param parameters: Dictionnaire contenant 'proportions' et 'transition_matrix'.
    :return: Un array de responsabilités.
    """
    # Extraction des paramètres
    proportions = parameters['proportions']
    transition_matrix = parameters['transition_matrix']

    # Calcul des probabilités pour chaque point de données
    responsibilities = np.dot(data, transition_matrix) * proportions
    responsibilities = responsibilities / responsibilities.sum(axis=1, keepdims=True)

    return responsibilities

def m_step(data, responsibilities):
    """
    Étape M de l'algorithme EM.
    Met à jour les paramètres pour maximiser la log-vraisemblance en fonction des responsabilités calculées.

    :param data: Données observées.
    :param responsibilities: Responsabilités de l'étape E.
    :return: Dictionnaire contenant les paramètres mis à jour.
    """
    # Nombre de communes
    n_communes = data.shape[1]

    # Mise à jour des proportions
    proportions = responsibilities.mean(axis=0)

    # Mise à jour de la matrice de transition
    transition_matrix = np.zeros((n_communes, n_communes))
    for i in range(n_communes):
        for j in range(n_communes):
            transition_matrix[i, j] = (responsibilities[:, i] * data[:, j]).sum() / responsibilities[:, i].sum()

    return {
        'proportions': proportions,
        'transition_matrix': transition_matrix
    }

def compute_log_likelihood(data, parameters):
    """
    Calcule la log-vraisemblance des données avec les paramètres donnés.
    
    :param data: Données observées.
    :param parameters: Paramètres actuels de l'algorithme EM, contenant les 'proportions' et la 'transition_matrix'.
    :return: Valeur de la log-vraisemblance.
    """
    proportions = parameters['proportions']
    transition_matrix = parameters['transition_matrix']
    
    # Calculer la matrice de probabilité pour chaque observation en utilisant la matrice de transition
    probability_matrix = np.dot(data, transition_matrix)
    
    # Calculer la log-vraisemblance
    log_likelihood = np.sum(np.log(np.dot(probability_matrix, proportions)))

    return log_likelihood

def em_algorithm(data, init_params, start_date, end_date, max_iter=100, tol=1e-6):
    """
    Exécute l'algorithme EM et sauvegarde les matrices de transition par nuit.
    
    :param data: Données observées.
    :param init_params: Paramètres initiaux.
    :param start_date: Date de début de l'analyse.
    :param end_date: Date de fin de l'analyse.
    :param max_iter: Nombre maximum d'itérations.
    :param tol: Tolérance pour la convergence.
    :return: Paramètres finaux et historique de la log-vraisemblance.
    """
    # Filtrer les données pour l'intervalle spécifié
    data['DATE'] = pd.to_datetime(data['DATE'])
    filtered_data = data[(data['DATE'] >= pd.to_datetime(start_date)) & (data['DATE'] <= pd.to_datetime(end_date))]

    parameters = init_params
    log_likelihood_history = []
    transition_matrices = {}

    for day in pd.date_range(start=start_date, end=end_date):
        daily_data = filtered_data[filtered_data['DATE'] == day]
        if daily_data.empty:
            continue
        
        responsibilities = e_step(daily_data, parameters)
        parameters = m_step(daily_data, responsibilities)
        log_likelihood = compute_log_likelihood(daily_data, parameters)
        log_likelihood_history.append(log_likelihood)
        
        # Enregistrement de la matrice de transition pour le jour actuel
        transition_matrices[day.strftime('%Y-%m-%d')] = parameters['transition_matrix']

    # Sauvegarde des matrices de transition dans un fichier Excel
    with pd.ExcelWriter('transition_matrix.xlsx') as writer:
        for date, matrix in transition_matrices.items():
            pd.DataFrame(matrix).to_excel(writer, sheet_name=date)
    
    return parameters, log_likelihood_history

# Exécution de l'algorithme EM avec les dates spécifiées
start_date = '2022-01-01'  # Exemple de date de début
end_date = '2022-01-10'    # Exemple de date de fin
final_params, log_likelihood = em_algorithm(data, init_params, start_date, end_date)