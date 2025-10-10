# Aqui se pondran las funciones de reportes
import pandas as pd
from pandas import DataFrame

def sleep_vs_age_report(data):
    bins = [20,29,39,49,100]
    labels = ["20-29", "30-39", "40-49", "50+"]  

    # agrupar datos
    data["Age group"] = pd.cut(data['Age'], bins=bins, labels=labels, right=True)

    # promedios
    promedios = data.groupby("Age group",observed=False)["Quality of Sleep"].mean()

    tabla = promedios.reset_index().rename(columns={"Quality of Sleep": "Avg Quality of Sleep"})
    promedios = data.groupby("Age group",observed=False)["Quality of Sleep"].mean()
    # Calcular conteos
    conteos = data["Age group"].value_counts().sort_index()

    # Crear el reporte
    print("=== Reporte: Calidad de sueño por grupo de edad ===\n")
    for grupo, promedio in promedios.items():
        cantidad = conteos[grupo]
        print(f"- Grupo {grupo}: promedio = {promedio:.2f} (n={cantidad})")

    # Observaciones automáticas (opcional)
    mejor = promedios.idxmax()
    peor = promedios.idxmin()

    print(f"\nEl grupo con mejor calidad de sueño es {mejor}, "
        f"mientras que el grupo con peor calidad de sueño es {peor}.")
    
def create_bins_and_display(data: DataFrame, column: str, n: int):
    """
    Create bins for a numerical column and display the bin ranges.

    Parameters:
        data (DataFrame): The dataset containing the column.
        column (str): The name of the column to bin.
        n (int): The number of bins to create.
    """
    # Get unique values and sort them
    unique_values = sorted(data[column].unique())
    
    # Divide unique values into n equal bins
    bins = pd.cut(unique_values, bins=n, retbins=True, labels=False)[1]

    # Display the bins
    print("=== Bins for column '{}' ===".format(column))
    for i in range(len(bins) - 1):
        print(f"Bin {i + 1}: {bins[i]:.2f} to {bins[i + 1]:.2f}")
    return bins


def sleep_vs_physical_activity_report(data):

    bins = create_bins_and_display(data, 'Physical Activity Level', n=4)

    # Create labels for the bins
    labels = []
    for i in range(len(bins) - 1):
        labels.append(f"{bins[i]:.2f}-{bins[i+1]:.2f}")

    # Group data by bins
    data["Physical Activity Level grouped"] = pd.cut(
        data['Physical Activity Level'],
        bins=bins,
        labels=labels,
        include_lowest=True,
        right=True
    )

    # Calculate means
    promedios = data.groupby("Physical Activity Level grouped", observed=False)["Quality of Sleep"].mean()

    tabla = promedios.reset_index().rename(columns={"Quality of Sleep": "Avg Quality of Sleep"})
    # Calculate counts
    conteos = data["Physical Activity Level grouped"].value_counts().sort_index()

    # Create the report
    print("=== Reporte: Calidad de sueño por cantidad de ejercicio ===\n")
    for grupo, promedio in promedios.items():
        cantidad = conteos[grupo]
        print(f"- Grupo {grupo}: promedio = {promedio:.2f} (n={cantidad})")

    # Automatic observations (optional)
    mejor = promedios.idxmax()
    peor = promedios.idxmin()

    print(f"\nEl grupo con mejor calidad de sueño es {mejor}, "
          f"mientras que el grupo con peor calidad de sueño es {peor}.")

    