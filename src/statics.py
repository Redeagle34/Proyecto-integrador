# Aqui poner las funciones de estadisticas
import pandas as pd

def steps_sleep(data):
    bins = [2000,4000,6000,8000,10000]
    labels = ["2000-4000", "4000-6000", "6000-8000", "8000-10000"]

    data["Daily Steps ranges"] = pd.cut(data["Daily Steps"], bins=bins, labels=labels)

    results = data.groupby("Daily Steps ranges")["Quality of Sleep"].mean().reset_index()

    print(results)

def average_sleep_by_age(data):
    # promedio por grupo de edad 
    bins = [20,29,39,49,100]
    labels = ["20-29", "30-39", "40-49", "50+"]  

    # agrupar datos
    data["Age group"] = pd.cut(data['Age'], bins=bins, labels=labels, right=True)

    # promedios
    promedios = data.groupby("Age group")["Quality of Sleep"].mean()

    tabla = promedios.reset_index().rename(columns={"Quality of Sleep": "Avg Quality of Sleep"})
    return tabla