import json
import numpy as np

# Load JSON data
# Charger les données JSON
def load_transition_data_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file) 
    return data

# Assuming you want to map commune names to numeric IDs for matrix operations
# Créer un mappage des noms de communes vers des identifiants numériques
def get_commune_mapping(data):
    communes = set()
    for date, daily_data in data.items():
        for commune in daily_data.keys():
            communes.add(commune)
    return {commune: i for i, commune in enumerate(communes)}

# Load data
#transition_data_path = "C:\Math\devoir\1.ConversiondonnéesdeSciensano\COVID_19BXL.json"
transition_data_path = "C:\\Math\\devoir\\1.ConversiondonnéesdeSciensano\\COVID_19BXL.json"
transition_data = load_transition_data_from_json(transition_data_path)

# Get mapping of communes to IDs
commune_mapping = get_commune_mapping(transition_data)
num_communes = len(commune_mapping)

# Initialize transition matrices with random values
transition_matrices = np.random.rand(num_communes, num_communes)

max_iterations = 100
tolerance = 1e-6

# Example processing loop (adapt as needed for your actual use case)
# This is a placeholder for where you would implement your EM algorithm or other processing
for iteration in range(max_iterations):
    # Placeholder for algorithm implementation
    # Update transition_matrices based on your algorithm's requirements

    # Example convergence check (replace with actual convergence criteria)
    if iteration > 0:  # Assuming you have some actual convergence check
        break

# Print transition matrices
print("Transition matrices:")
for i in range(num_communes):
    for j in range(num_communes):
        print(f"From {i} to {j}: {transition_matrices[i, j]}")
