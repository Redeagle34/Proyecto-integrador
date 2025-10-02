# Aqui poner las funciones de estadisticas
import pandas as pd

def steps_sleep(data):
    bins = [2000,4000,6000,8000,10000]
    labels = ["2000-4000", "4000-6000", "6000-8000", "8000-10000"]

    data["Daily Steps ranges"] = pd.cut(data["Daily Steps"], bins=bins, labels=labels)

    results = data.groupby("Daily Steps ranges")["Quality of Sleep"].mean().reset_index()

    print(results)