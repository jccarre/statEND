import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import os.path

# Chargement des données
secteurs_file = 'les secteurs Province Sud Est.csv'
df_secteurs = pd.read_csv(secteurs_file, sep=';')
secteursDoublon = df_secteurs['Secteur'].duplicated()
if any(secteursDoublon):
    messagebox.showwarning("Attention", "Secteurs en doublon dans le fichier '" + secteurs_file + "'")

years = ["2021", "2020"]  # Add more years if needed
results_by_year = []
for year in years:
    file_name = year + '.csv'
    df = pd.read_csv(os.path.join("Foyers",  file_name))
    df_merged = pd.merge(df, df_secteurs, on='Secteur')
    columns_to_keep = ["Identifiant", "Nom de l'équipe", "Secteur", "Date de naissance LUI", "Date de naissance ELLE",
                       "Province", "Région"]
    df_merged = df_merged.loc[:, columns_to_keep]
    df_merged['Year'] = year
    results_by_year.append(df_merged)
final_result = pd.concat(results_by_year)

# Fonction pour générer le graphe
def generate_graph():
    selected_secteurs = [secteur_var.get() for secteur_var in secteur_vars if secteur_var.get()]
    selected_regions = [region_var.get() for region_var in region_vars if region_var.get()]
    selected_provinces = [province_var.get() for province_var in province_vars if province_var.get()]
    selected_grandeur = grandeur_var.get()

    filtered_data = final_result[final_result['Secteur'].isin(selected_secteurs) &
                              final_result['Région'].isin(selected_regions) &
                              final_result['Province'].isin(selected_provinces)]

    grouped_data = filtered_data.groupby(['Secteur', 'Région', 'Province', 'Year'])['Identifiant'].count().reset_index()
    averaged_data = grouped_data.groupby(['Secteur', 'Région', 'Province', 'Year'])['Identifiant'].mean().reset_index()

    plt.figure(figsize=(10, 6))

    for sector, data in averaged_data.groupby('Secteur'):
        plt.plot(data['Year'], data['Identifiant'], marker='o', label=sector)

    plt.xlabel('Year')
    plt.ylabel(selected_grandeur)
    plt.legend()
    plt.title(f'{selected_grandeur} for each Sector over Time')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig('graph.png', dpi=300)
    plt.show()

# Création de l'interface graphique en tkinter
root = Tk()
root.title('Graph Generator')

# Zones pour les checkboxes
secteur_pane = PanedWindow(root, orient=VERTICAL)
secteur_pane.pack(fill=BOTH, expand=True)

region_pane = PanedWindow(root, orient=VERTICAL)
region_pane.pack(fill=BOTH, expand=True)

province_pane = PanedWindow(root, orient=VERTICAL)
province_pane.pack(fill=BOTH, expand=True)

# Checkbox pour les secteurs
secteur_vars = []
for sector in df_merged['Secteur'].unique():
    var = BooleanVar()
    Checkbutton(secteur_pane, text=sector, variable=var).pack(anchor=W)
    secteur_vars.append(var)

# Checkbox pour les régions
region_vars = []
for region in df_merged['Région'].unique():
    var = BooleanVar()
    Checkbutton(region_pane, text=region, variable=var).pack(anchor=W)
    region_vars.append(var)

# Checkbox pour les provinces
province_vars = []
for province in df_merged['Province'].unique():
    var = BooleanVar()
    Checkbutton(province_pane, text=province, variable=var).pack(anchor=W)
    province_vars.append(var)

# Menu déroulant pour choisir la grandeur
grandeurs = ['Nombre moyen de foyers par équipe', 'Autre grandeur 1', 'Autre grandeur 2']
grandeur_var = StringVar()
grandeur_var.set(grandeurs[0])
grandeur_dropdown = OptionMenu(root, grandeur_var, *grandeurs)
grandeur_dropdown.pack()

# Bouton pour générer le graphe
generate_button = Button(root, text='Générer graphe', command=generate_graph)
generate_button.pack()

root.mainloop()
