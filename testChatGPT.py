import os.path

import pandas as pd
import matplotlib.pyplot as plt
from tkinter import messagebox
from log import logCSV, create_file_and_folder


# Step 1: Load "les secteurs Province Sud Est.csv"
secteurs_file = 'les secteurs Province Sud Est.csv'
df_secteurs = pd.read_csv(secteurs_file, sep=';')
secteursDoublon = df_secteurs['Secteur'].duplicated()
if any(secteursDoublon):
    messagebox.showwarning("Attention", "Secteurs en doublon dans le fichier '" + secteurs_file + "'")
# Initialize an empty list to store the results for each year
results_by_year = []

# Step 2: Process each CSV file for each year
years = ["2021", "2020"]  # Add more years if needed

create_file_and_folder("temp", "nb_moyen_foyer_par_equipe.csv")

for year in years:
    # Load the CSV file for the current year
    file_name = year + '.csv'
    df = pd.read_csv(os.path.join("Foyers",  file_name))

    # Merge with "les secteurs Province Sud Est.csv" based on the 'Secteur' column
    df_merged = pd.merge(df, df_secteurs, on='Secteur')

    # Convertir les chaînes de caractères représentant les dates en dates. Attention : il faut au préalable avoir supprimé toutes les cellules vides.
    # df_merged['Date de naissance LUI'] = pd.to_datetime(df_merged['Date de naissance LUI'], format="%d/%m/%y")
    # df_merged['Date de naissance ELLE'] = pd.to_datetime(df_merged['Date de naissance ELLE'], format="%d/%m/%y")

    # On supprime toutes les colonnes inutiles
    columns_to_keep = ["Identifiant", "Nom de l'équipe", "Secteur", "Date de naissance LUI", "Date de naissance ELLE", "Province", "Région"]
    df_merged = df_merged.loc[:, columns_to_keep]
    # Step 3: Calculate the average number of "Foyer" per "Equipe" for each sector, region, and province
    results = df_merged.groupby(['Secteur', 'Région', 'Province', "Nom de l'équipe"])[["Identifiant"]].count()
    results.rename(columns={'Identifiant': 'Nombre de foyers par équipe'}, inplace=True)
    results.reset_index(inplace=True)
    average_foyers_par_secteur = results.groupby(['Secteur', 'Région', 'Province'])["Nombre de foyers par équipe"].mean()
    average_foyers_par_secteur = average_foyers_par_secteur.reset_index()
    average_foyers_par_region = average_foyers_par_secteur.groupby(['Région', 'Province'])["Nombre de foyers par équipe"].mean()
    average_foyers_par_region = average_foyers_par_region.reset_index()
    average_foyers_par_province = average_foyers_par_secteur.groupby(['Province'])["Nombre de foyers par équipe"].mean()
    average_foyers_par_province = average_foyers_par_province.reset_index()
    dictionnaire_pour_CSV = {"year" : year}
    for sector, data in average_foyers_par_secteur.groupby('Secteur'):
        dictionnaire_pour_CSV[sector] = data['Nombre de foyers par équipe'].mean()
    for region, data in average_foyers_par_region.groupby('Région'):
        dictionnaire_pour_CSV[region] = data['Nombre de foyers par équipe'].mean()
    for province, data in average_foyers_par_region.groupby('Province'):
        dictionnaire_pour_CSV[province] = data['Nombre de foyers par équipe'].mean()
    logCSV(dictionnaire_pour_CSV, nom_fichier=os.path.join("temp", "nb_moyen_foyer_par_equipe.csv"))

# Concatenate the results for all years into a single DataFrame
final_result = pd.concat(results_by_year)

# Step 4: Create the plot
plt.figure(figsize=(12, 8))
for sector, data in final_result.groupby('Secteur'):
    for region, region_data in data.groupby('Région'):
        plt.plot(region_data['Year'], region_data['Average Foyer per Equipe'], marker='o', label=f'{sector} - {region}')

plt.xlabel('Year')
plt.ylabel('Average Foyer per Equipe')
plt.legend()
plt.title('Average Foyer per Equipe for each Sector and Region by Year')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('average_foyers_per_equipe.png', dpi=300)
plt.show()
