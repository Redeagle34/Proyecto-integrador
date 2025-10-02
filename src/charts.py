# Aqui se pondran las funciones de graficacion

def steps_sleep_chart(data):
    import matplotlib.pyplot as plt
    plt.bar(results["Daily Steps ranges"], results["Quality of Sleep"])

    plt.xlabel("Daily Steps")
    plt.ylabel("Quality of Sleep")
    plt.title("Relation between Daily Steps & Quality of Sleep")
    plt.ylim(0,10)
    plt.show()