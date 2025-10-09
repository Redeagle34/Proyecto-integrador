# Aqui se pondran las funciones de reportes
import pandas as pd

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
    