# Aqui se llamaran a todas las funciones del proyecto
from src.charts import heatmap_IMC_vs_sueño, scatter_IMC_vs_sueño, steps_sleep_chart,sleep_quality_vs_age
from src.reports import sleep_vs_age_report

# imports
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# cargar el dataset
def menu():
    ## aqui cambiar para llamar a la funcion que hizo JP que carga el csv
    data = pd.read_csv("resources/data/Sleep_health_and_lifestyle_dataset.csv")

    user = input('elige una opcion (heatmap|scatter|age|report): ')
    match user:
        case 'heatmap':
            heatmap_IMC_vs_sueño(data)
        case 'scatter':
            scatter_IMC_vs_sueño(data)
        case 'age':
            sleep_quality_vs_age(data)
        case 'report':
            sleep_vs_age_report(data)

