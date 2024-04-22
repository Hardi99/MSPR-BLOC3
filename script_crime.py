import pandas as pd

def charger_donnees_criminelles(annees, code_departement):
    filepath = 'base\\donnee-dep-data.gouv-2023-geographie2023-produit-le2024-03-07.csv'
    df = pd.read_csv(filepath, delimiter=';', quotechar='"')
    # Correction des formats de données numériques
    df['tauxpourmille'] = pd.to_numeric(df['tauxpourmille'].str.replace(',', '.'), errors='coerce')
    df['Année'] = df['Année'].apply(lambda x: 2000 + x if x < 100 else x)  # Convertir 17 en 2017, 22 en 2022
    df_filtered = df[(df['Année'].isin(annees)) & (df['Code du département'] == code_departement)]
    return df_filtered

# Définir les années d'intérêt et le code département pour Hauts-de-Seine
annees_interet = [2017, 2022]
code_departement_HDS = '92'

# Utilisation des fonctions
df_crime_92 = charger_donnees_criminelles(annees_interet, code_departement_HDS)

# Afficher les données filtrées pour vérifier
print(df_crime_92[['Année', 'Code du département', 'classe', 'faits', 'POP', 'tauxpourmille']])
df_crime_92.to_excel('filtre\\indicateurs_crime.xlsx')
