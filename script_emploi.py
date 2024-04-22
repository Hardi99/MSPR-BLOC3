import pandas as pd

def fusionner_dataframe(df_2017, df_2022):
    df_2017['Année'] = 2017
    df_2022['Année'] = 2022

    # Flatten the multi-level columns
    df_2017.columns = [' '.join(col).strip() for col in df_2017.columns.values]
    df_2022.columns = [' '.join(col).strip() for col in df_2022.columns.values]
    return pd.concat([df_2017, df_2022], ignore_index=True)

def traiter_donnees_annuelles(file_path, year):
    df = pd.read_excel(file_path, str(year), skiprows=3, header=[0, 1], nrows=96)
    print(df)

    subset_columns = [('Départements', 'Unnamed: 0_level_1'),
                      ('Départements', 'Unnamed: 1_level_1'),
                      ('Ensemble', '20 à 39 ans'),
                      ('Ensemble', '40 à 59 ans')]
    df = df[subset_columns]
    df_filtered = df[df[('Départements', 'Unnamed: 0_level_1')] == '92'].copy()
    df_filtered['Total_Actif'] = df_filtered[('Ensemble', '20 à 39 ans')] + df_filtered[('Ensemble', '40 à 59 ans')]
    df_filtered['Année'] = year
    return df_filtered

def calculeActifParDep92():
    file_path = 'base\\estim-pop-dep-sexe-gca-1975-2023.xls'
    df2017 = traiter_donnees_annuelles(file_path, 2017)
    df2022 = traiter_donnees_annuelles(file_path, 2022)
    return fusionner_dataframe(df2017, df2022)

def calculeMoyenneDemandeurParAnParDep():
    file_path = 'base\\Demandeur_Emploie.csv'
    data = pd.read_csv(file_path, skiprows=3, delimiter=';', nrows=330)
    
    # Extraire l'année des données de 'Mois' qui sont probablement sous la forme "Janvier 2017"
    data['Année'] = data['Mois'].str.extract('(\d{4})').astype(int)  # Utilise une expression régulière pour isoler l'année
    
    # Conversion des données numériques pour 'Hauts-de-Seine 92' en enlevant les espaces
    data['Hauts-de-Seine 92'] = data['Hauts-de-Seine 92'].str.replace(' ', '').astype(int)
    
    # Grouper les données par 'Année' et calculer la moyenne pour 'Hauts-de-Seine 92'
    data = data.groupby('Année')['Hauts-de-Seine 92'].mean().reset_index()
    
    return data

def calculerIndicateurHautsDeSeine92(df_actifs, df_emplois):
    # Fusionner les données d'actifs et d'emploi sur l'année
    df_actifs.rename(columns={'Départements Unnamed: 0_level_1': 'Code du département'}, inplace=True)
    print(df_actifs)
    df_merged = pd.merge(df_actifs, df_emplois, on='Année', how='inner')

    # Calculer l'indicateur comme le pourcentage de demandeurs d'emploi par rapport aux actifs
    df_merged['Indicateur'] = (df_merged['Hauts-de-Seine 92'] / df_merged['Total_Actif']) * 100

    # Sélectionner uniquement les colonnes pertinentes pour l'output
    resultat = df_merged[['Code du département', 'Année', 'Indicateur']]

    return resultat

df1 = calculeActifParDep92()
df2 = calculeMoyenneDemandeurParAnParDep()
print(df1)
print(df2)

# Exemple d'utilisation de la fonction
df_actifs = calculeActifParDep92()
df_emplois = calculeMoyenneDemandeurParAnParDep()
indicateur_resultat = calculerIndicateurHautsDeSeine92(df_actifs, df_emplois)
print(indicateur_resultat)
