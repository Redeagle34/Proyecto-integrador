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

def gender_vs_stress_level(data):
    """
    Generate a report on the relationship between gender and stress level.
    
    Parameters:
        data (DataFrame): The dataset containing 'Gender' and 'Stress Level' columns.
    """
    # Group data by gender and calculate average stress level
    promedios = data.groupby("Gender")["Stress Level"].mean()
    
    # Calculate counts
    conteos = data["Gender"].value_counts().sort_index()
    
    # Create the report
    print("=== Reporte: Nivel de estrés por género ===\n")
    for genero, promedio in promedios.items():
        cantidad = conteos[genero]
        print(f"- Género {genero}: promedio = {promedio:.2f} (n={cantidad})")
    
    # Automatic observations
    mayor_estres = promedios.idxmax()
    menor_estres = promedios.idxmin()
    
    print(f"\nEl género con mayor nivel de estrés es {mayor_estres}, "
          f"mientras que el género con menor nivel de estrés es {menor_estres}.")

def BMI_vs_sleep_duration(data):
    """
    Reporte sobre la relación entre IMC y duración del sueño.
    
    Parameters:
        data (DataFrame): Dataset con columnas 'BMI Category' y 'Sleep Duration'
    """
    # Agrupar datos por categoría de IMC y calcular estadísticas de duración de sueño
    promedios = data.groupby("BMI Category")["Sleep Duration"].mean()
    desviaciones = data.groupby("BMI Category")["Sleep Duration"].std()
    
    # Calcular conteos
    conteos = data["BMI Category"].value_counts().sort_index()
    
    # Crear el reporte
    print("=" * 70)
    print("REPORTE: DURACIÓN DEL SUEÑO POR CATEGORÍA DE IMC")
    print("=" * 70)
    print()
    
    print(f"Total de registros analizados: {len(data)}")
    print(f"Categorías de IMC: {', '.join(sorted(data['BMI Category'].unique()))}")
    print()
    
    print("ESTADÍSTICAS POR CATEGORÍA DE IMC:")
    print("-" * 70)
    for categoria in sorted(promedios.index):
        promedio = promedios[categoria]
        std = desviaciones[categoria]
        cantidad = conteos[categoria]
        print(f"  • {categoria:20s}: {promedio:.2f} horas (±{std:.2f}) - {cantidad} personas")
    
    print()
    
    # Observaciones automáticas
    mayor_duracion = promedios.idxmax()
    menor_duracion = promedios.idxmin()
    diferencia = promedios[mayor_duracion] - promedios[menor_duracion]
    
    print("HALLAZGOS:")
    print("-" * 70)
    print(f"Categoría con MAYOR duración de sueño: {mayor_duracion}")
    print(f"Promedio: {promedios[mayor_duracion]:.2f} horas")
    print()
    print(f"Categoría con MENOR duración de sueño: {menor_duracion}")
    print(f"Promedio: {promedios[menor_duracion]:.2f} horas")
    print()
    print(f"Diferencia entre categorías: {diferencia:.2f} horas")
    print()
    print("CONCLUSIÓN:")
    print(f"   Las personas con IMC '{mayor_duracion}' duermen en promedio")
    print(f"   {diferencia:.2f} horas más que las personas con IMC '{menor_duracion}'.")
    print()
    print("=" * 70)


def BMI_vs_sleep_quality(data):
    """
    Reporte sobre la relación entre IMC y calidad del sueño.
    
    Parameters:
        data (DataFrame): Dataset con columnas 'BMI Category' y 'Quality of Sleep'
    """
    # Agrupar datos por categoría de IMC y calcular estadísticas de calidad de sueño
    promedios = data.groupby("BMI Category")["Quality of Sleep"].mean()
    desviaciones = data.groupby("BMI Category")["Quality of Sleep"].std()
    
    # Calcular conteos
    conteos = data["BMI Category"].value_counts().sort_index()
    
    # Crear el reporte
    print("=" * 70)
    print("REPORTE: CALIDAD DEL SUEÑO POR CATEGORÍA DE IMC")
    print("=" * 70)
    print()
    
    print(f"Total de registros analizados: {len(data)}")
    print(f"Categorías de IMC: {', '.join(sorted(data['BMI Category'].unique()))}")
    print()
    
    print("ESTADÍSTICAS POR CATEGORÍA DE IMC:")
    print("-" * 70)
    for categoria in sorted(promedios.index):
        promedio = promedios[categoria]
        std = desviaciones[categoria]
        cantidad = conteos[categoria]
        print(f"  • {categoria:20s}: {promedio:.2f}/10 (±{std:.2f}) - {cantidad} personas")
    
    print()
    
    # Observaciones automáticas
    mayor_calidad = promedios.idxmax()
    menor_calidad = promedios.idxmin()
    diferencia = promedios[mayor_calidad] - promedios[menor_calidad]
    
    print("HALLAZGOS:")
    print("-" * 70)
    print(f"Categoría con MAYOR calidad de sueño: {mayor_calidad}")
    print(f"Calidad promedio: {promedios[mayor_calidad]:.2f}/10")
    print()
    print(f"Categoría con MENOR calidad de sueño: {menor_calidad}")
    print(f"Calidad promedio: {promedios[menor_calidad]:.2f}/10")
    print()
    print(f"Diferencia entre categorías: {diferencia:.2f} puntos")
    print()
    print("CONCLUSIÓN:")
    print(f"Las personas con IMC '{mayor_calidad}' reportan una calidad de sueño")
    print(f"{diferencia:.2f} puntos superior a las personas con IMC '{menor_calidad}'.")
    print()
    print("=" * 70)