import pandas as pd

# Chemins des fichiers et paramètres
df_crime = pd.read_excel('filtre\\indicateurs_crime.xlsx')
df_electorale_2017 = pd.read_excel("filtre\\resultats_2017.xlsx")
df_electorale_22 = pd.read_excel("filtre\\resultats_2022.xlsx")
indicateur_resultat = pd.read_excel("filtre\\indicateurs_emploi.xlsx")

df_Vote = df_electorale_2017[['Libellé de la commune', 'Code du département']]
df_Vote['Votes_Nuls_2017'] = df_electorale_2017['Nuls']
df_Vote['Votes_Nuls_2022'] = df_electorale_22['Nuls']
df_Vote['Exprimés_2017'] = df_electorale_2017['Exprimés']
df_Vote['Gauche_2017'] = df_electorale_2017['Total_Gauche']
df_Vote['Milieu_2017'] = df_electorale_2017['Total_Milieu']
df_Vote['Droite_2017'] = df_electorale_2017['Total_Droite']
df_Vote['Exprimés_2022'] = df_electorale_22['Exprimés']
df_Vote['Gauche_2022'] = df_electorale_22['Total_Gauche']
df_Vote['Milieu_2022'] = df_electorale_22['Total_Milieu']
df_Vote['Droite_2022'] = df_electorale_22['Total_Droite']
df_Vote['Gagnants_2017'] = df_electorale_2017['gagnant(e)']
df_Vote['Partie_Gagnante_2017'] = df_electorale_2017['orientation_gagnante']
df_Vote['Partie_Gagnante_2022'] = df_electorale_22['orientation_gagnante']

# Extraction des indicateurs d'emploi pour chaque année
indicateur_emploi_2017 = indicateur_resultat.loc[indicateur_resultat['Année'] == 2017, 'Indicateur'].values[0]
indicateur_emploi_2022 = indicateur_resultat.loc[indicateur_resultat['Année'] == 2022, 'Indicateur'].values[0]

# Ajout des indicateurs d'emploi à df_Vote
df_Vote['Indicateur_Emploi_2017'] = indicateur_emploi_2017
df_Vote['Indicateur_Emploi_2022'] = indicateur_emploi_2022

# Fusion des indicateurs de crime avec les données de vote pour chaque année
crime_2017 = df_crime[df_crime['Année'] == 2017].groupby('Code du département').agg({'tauxpourmille': 'mean'}).reset_index()
crime_2022 = df_crime[df_crime['Année'] == 2022].groupby('Code du département').agg({'tauxpourmille': 'mean'}).reset_index()

df_Vote = df_Vote.merge(crime_2017, how='left', on='Code du département').rename(columns={'tauxpourmille': 'Indicateur_Crime_2017'})
df_Vote = df_Vote.merge(crime_2022, how='left', on='Code du département').rename(columns={'tauxpourmille': 'Indicateur_Crime_2022'})

print(df_Vote.head())
df_Vote.to_excel('final\\fusion_fichier.xlsx')