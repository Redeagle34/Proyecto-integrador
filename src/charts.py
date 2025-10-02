# Aqui se pondran las funciones de graficacion
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
    

def steps_sleep_chart(results):
    import matplotlib.pyplot as plt
    plt.bar(results["Daily Steps ranges"], results["Quality of Sleep"])

    plt.xlabel("Daily Steps")
    plt.ylabel("Quality of Sleep")
    plt.title("Relation between Daily Steps & Quality of Sleep")
    plt.ylim(0,10)
    plt.show()