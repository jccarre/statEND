from pandas import read_csv as pdRead_csv

from matplotlib import pyplot as plt

def generer_image(fichier, columns):
    df = pdRead_csv(fichier, sep=";")
    legendes = []
    for c in columns:
        legendes.append(c)

    plt.rcParams["figure.figsize"] = [10, 10]
    plt.rcParams["figure.autolayout"] = True

    df.plot(x="année", y=columns, grid=True)
    plt.tight_layout()
    plt.legend(legendes, bbox_to_anchor=(0.5, 1.2), loc='upper center')

    fichier_sans_extension = fichier.split(".")[0]
    plt.savefig(fichier_sans_extension + ".png")


