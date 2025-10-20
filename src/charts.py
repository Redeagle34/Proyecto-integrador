# Aqui se pondran las funciones de graficacion
from src.statics import average_sleep_by_age

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def heatmap_IMC_vs_sueño(data):
    df = pd.DataFrame(data)
    df_para_relacion = df[['BMI Category', 'Sleep Duration']]
    df_relacion_IMC_sueño = df_para_relacion.groupby('BMI Category')['Sleep Duration'].mean().reset_index()

    pivot = df_relacion_IMC_sueño.set_index("BMI Category")[["Sleep Duration"]]
    sns.heatmap(pivot, cmap="viridis", annot=True)
    return plt.show()

def scatter_IMC_vs_sueño(data):
    df = pd.DataFrame(data)
    df_para_relacion = df[['BMI Category', 'Sleep Duration']]
    df_relacion_IMC_sueño = df_para_relacion.groupby('BMI Category')['Sleep Duration'].mean().reset_index()

    plt.scatter(df_relacion_IMC_sueño['BMI Category'], df_relacion_IMC_sueño['Sleep Duration'])
    plt.plot(df_relacion_IMC_sueño['BMI Category'], df_relacion_IMC_sueño['Sleep Duration'])
    plt.xlabel('BMI Category')
    plt.title('Average Sleep Duration by BMI Category')
    return plt.show()
    

def steps_sleep_chart(data):
    df = pd.DataFrame(data)
    bins = [2000,4000,6000,8000,10000]
    labels = ["2000-4000", "4000-6000", "6000-8000", "8000-10000"]
    df["Daily Steps ranges"] = pd.cut(df["Daily Steps"], bins=bins, labels=labels)
    results = df.groupby("Daily Steps ranges")["Quality of Sleep"].mean().reset_index()
    plt.bar(results["Daily Steps ranges"], results["Quality of Sleep"])

    plt.xlabel("Daily Steps")
    plt.ylabel("Quality of Sleep")
    plt.title("Relation between Daily Steps & Quality of Sleep")
    plt.ylim(0,10)
    plt.show()

def sleep_quality_vs_age(data):
    plt.figure(figsize=(8,5))
    sns.barplot(x="Age group", y="Avg Quality of Sleep", data=average_sleep_by_age(data), palette="viridis")

    plt.title("Promedio de Calidad de Sueño por Grupo de Edad")
    plt.xlabel("Grupo de Edad")
    plt.ylabel("Promedio de Calidad de Sueño")
    plt.ylim(0, 10)  # asumiendo escala de 1 a 10
    plt.show()

def bar_avg_by_group(data, x_col: str, y_col: str):
    data = pd.DataFrame(data)
    avg = data.groupby(x_col)[y_col].mean().reset_index()
    plt.figure(figsize=(10, 6))
    plt.bar(avg[x_col], avg[y_col], color=['pink', 'blue'])
    plt.xlabel(x_col)
    plt.ylabel(f'Average {y_col}')
    plt.title(f'Average {y_col} for each {x_col}')
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.show()

def scatter_IMC_vs_calidad_sueño(data):
    df = pd.DataFrame(data)
    df_para_relacion = df[['BMI Category', 'Quality of Sleep']]
    df_relacion_IMC_calidad = df_para_relacion.groupby('BMI Category')['Quality of Sleep'].mean().reset_index()
    
    df_relacion_IMC_sueño = df.groupby('BMI Category')['Quality of Sleep'].mean().reset_index()

    plt.scatter(df_relacion_IMC_sueño['BMI Category'], df_relacion_IMC_sueño['Quality of Sleep'])
    plt.plot(df_relacion_IMC_sueño['BMI Category'], df_relacion_IMC_sueño['Quality of Sleep'])
    plt.xlabel('BMI Category')
    plt.title('Average Sleep Quality Duration by BMI Category')
    return plt.show()