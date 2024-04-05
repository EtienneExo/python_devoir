import devoir5
import numpy as np
from datetime import datetime

# Assurez-vous d'avoir exécuté votre devoir5.py pour charger et traiter vos données réelles
# Cela inclut la création de daily_case_matrices et daily_transition_matrices, que nous utiliserons ici.

# Utilisez devoir5.data_dict qui a déjà été créé pour avoir les données réelles.
real_case_matrices = {date: cases for date, cases in devoir5.data_dict.items()}

# # Utilisez devoir5.data_dict qui a déjà été créé pour avoir les données réelles.
# real_case_matrices = {date.strftime('%Y-%m-%d'): cases for date, cases in devoir5.data_dict.items()}

# # Création des dictionnaires de cas réels pour chaque jour, sans conversion en tableau numpy
# real_case_matrices = {date: cases for date, cases in devoir5.data_dict.items()}

# # Exemple de conversion des clés datetime.date en chaînes de caractères pour l'accès :
# formatted_real_case_matrices = {date.strftime('%Y-%m-%d'): cases for date, cases in real_case_matrices.items()}

# # Ensuite, lorsque vous appelez prevoir_cases_suivant, utilisez le dictionnaire avec les dates formatées :
# predicted_cases = devoir5.prevoir_cases_suivant(formatted_real_case_matrices, devoir5.daily_transition_matrices)

# Puis, en appelant prevoir_cases_suivant, assurez-vous que les formats correspondent.
predicted_cases = devoir5.prevoir_cases_suivant(real_case_matrices, devoir5.daily_transition_matrices)


# # Prédiction des cas pour chaque jour en utilisant les matrices de transition de devoir5.py
# predicted_cases = devoir5.prevoir_cases_suivant(real_case_matrices, devoir5.daily_transition_matrices)

# Définir une fonction pour calculer les erreurs dans test.py si non défini dans devoir5.py
def calculer_erreurs(predictions, real_data):
    mae = 0
    mse = 0
    n = len(predictions)

    for date, predicted_cases in predictions.items():
        if date in real_data:
            real_cases = real_data[date]
            errors = predicted_cases - real_cases
            mae += np.abs(errors).mean()
            mse += np.mean(errors ** 2)

    mae /= n
    mse /= n

    return mae, mse

# Calculer les erreurs entre les prédictions et les données réelles
mae, mse = calculer_erreurs(predicted_cases, real_case_matrices)

# Afficher les résultats des erreurs
print("Erreur Absolue Moyenne (MAE):", mae)
print("Erreur Quadratique Moyenne (MSE):", mse)