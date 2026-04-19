from datetime import datetime
import pytz
import matplotlib.pyplot as plt

def verduennungsrechner(C1, C2, V2):

    V1 = (C2 * V2) / C1

    return {
        "timestamp": datetime.now(pytz.timezone("Europe/Zurich")),
        "C1": C1,
        "C2": C2,
        "V2": V2,
        "V1": round(V1, 2)
    }

def plot_verduennung(C1, C2, V2, V1):
    fig, ax = plt.subplots()

    # Balken: Vergleich Stammlösung vs. Ziel
    labels = ["C1 (Start)", "C2 (Ziel)"]
    values = [C1, C2]

    ax.bar(labels, values)

    # Titel + Labels
    ax.set_title("Verdünnung: Konzentrationsvergleich")
    ax.set_ylabel("Konzentration")

    # Zusatzinfo als Text
    ax.text(0, C1, f"V1 = {round(V1,2)} ml", ha='center', va='bottom')
    ax.text(1, C2, f"V2 = {round(V2,2)} ml", ha='center', va='bottom')

    return fig