import pandas as pd

# Charger le fichier Excel
df = pd.read_excel("base\\resultat20221.xlsx")

# Supprimer les colonnes inutiles, en gardant celles nécessaires pour le résultat final
columns_to_drop = ["Libellé du département", "Votants", "% Vot/Ins", "Libellé de la circonscription",
                    "Code du b.vote", "N°Panneau", "N°Panneau.1", "N°Panneau.2", "N°Panneau.3",
                    "N°Panneau.4", "N°Panneau.5", "N°Panneau.6", "N°Panneau.7", "N°Panneau.8",
                    "% Blancs/Ins", "% Blancs/Vot", "% Nuls/Ins", "% Nuls/Vot", "% Exp/Ins", "% Exp/Vot",
                    "% Abs/Ins", "d", "N°Panneau.9",]
df.drop(columns=columns_to_drop, errors='ignore', inplace=True)

new_columns = []
for col in df.columns:
    if col in ['Nom', 'Prénom', 'Voix', '% Voix/Ins', "% Voix/Exp"] and '.' not in col:
        new_columns.append(col + '.0')
    else:
        new_columns.append(col)
df.columns = new_columns

# Filtrer pour le département 92 (si nécessaire)
df = df[df['Code du département'] == 92]

# Supposons que 'df' est votre DataFrame et que 'orientations' est déjà défini
colonnes_voix = [col for col in df.columns if 'Voix' in col]

# Mapping des orientations politiques
orientations_politiques = {
    "ARTHAUD": "Gauche", "HIDALGO": "Gauche", "JADOT": "Gauche", 
    "LASSALLE": "Gauche", "MÉLENCHON": "Gauche", "POUTOU": "Gauche", 
    "ROUSSEL": "Gauche", "DUPONT-AIGNAN": "Droite", "LE PEN": "Droite",
    "PÉCRESSE": "Droite", "ZEMMOUR": "Droite", "MACRON": "Milieu"
}

# Supposons que les colonnes Voix et Nom sont formatées comme Voix.i et Nom.i où i est un index de candidat
num_candidats = 12  # Semble être 12 candidats basés sur les colonnes Nom.0 à Nom.11

# Fonction pour calculer les voix de gauche pour une ligne
def calculer_voix_gauche(row):
    total_gauche = 0
    for i in range(num_candidats):
        nom_candidat = row[f'Nom.{i}']
        if orientations_politiques.get(nom_candidat.split()[-1], '') == 'Gauche':
            total_gauche += row[f'Voix.{i}']
    return total_gauche

# Fonction pour calculer les voix de gauche pour une ligne
def calculer_voix_droite(row):
    total_droite = 0
    for i in range(num_candidats):
        nom_candidat = row[f'Nom.{i}']
        if orientations_politiques.get(nom_candidat.split()[-1], '') == 'Droite':
            total_droite += row[f'Voix.{i}']
    return total_droite

# Fonction pour calculer les voix de gauche pour une ligne
def calculer_voix_milieu(row):
    total_milieu = 0
    for i in range(num_candidats):
        nom_candidat = row[f'Nom.{i}']
        if orientations_politiques.get(nom_candidat.split()[-1], '') == 'Milieu':
            total_milieu += row[f'Voix.{i}']
    return total_milieu

# Appliquer cette fonction à chaque ligne du DataFrame et créer une nouvelle colonne
df['Total_Gauche'] = df.apply(calculer_voix_gauche, axis=1)
df['Total_Droite'] = df.apply(calculer_voix_droite, axis=1)
df['Total_Milieu'] = df.apply(calculer_voix_milieu, axis=1)

index_gagnant = df[colonnes_voix].idxmax(axis=1)
df['gagnant(e)'] = index_gagnant.apply(lambda x: df['Nom' + x.split('Voix')[1]].iloc[0])
df['orientation_gagnante'] = df['gagnant(e)'].apply(lambda x: orientations_politiques.get(x.split(' ')[-1], "Inconnue"))

# Sélectionner uniquement les colonnes nécessaires pour le résultat final
df_final = df[['Code du département', 'Code de la commune', 'Libellé de la commune', 'Inscrits', "Exprimés", "Blancs", "Nuls", 'gagnant(e)', 'orientation_gagnante', 'Total_Gauche', 'Total_Droite', 'Total_Milieu']]

# Sauvegarde du fichier Excel
print(df_final)
df_final.to_excel('filtre\\resultats_2022.xlsx', index=False)
