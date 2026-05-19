print("Konzentrationsrechner MODULE GELADEN")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def berechne_konzentration(stoffmenge: float, volumen: float) -> float | None:
    if volumen <= 0:
        return None
    return stoffmenge / volumen


def erstelle_verlaufseintrag(stoffmenge, volumen, konzentration):
    return pd.DataFrame([{
        "timestamp": pd.Timestamp.now(),
        "rechner": "Konzentrationsrechner",
        "stoffmenge": stoffmenge,
        "volumen": volumen,
        "konzentration": konzentration,
        "favorite": False
    }])

def speichere_verlauf(data_manager, dataframe, filename="data.csv"):
    data_manager.save_user_data(dataframe, filename)

def validiere_eingaben(stoffmenge: float, volumen: float) -> tuple[bool, str]:
    if volumen <= 0:
        return False, "Volumen muss größer als 0 sein"
    return True, ""

def konzentration_linie():
    volumen = np.array([1,2,3,4,5])
    konz = np.array([2,4,6,8,10])

    fig, ax = plt.subplots()
    ax.plot(volumen, konz, marker='o')

    ax.set_title("Konzentration abhängig vom Volumen")
    ax.set_xlabel("Volumen")
    ax.set_ylabel("Konzentration")

    return fig

def erstelle_verlaufseintrag(stoffmenge, volumen, konzentration):
    return pd.DataFrame([{
        "timestamp": pd.Timestamp.now(),
        "rechner": "Konzentrationsrechner",
        "stoffmenge": stoffmenge,
        "volumen": volumen,
        "konzentration": konzentration,
        "favorite": False
    }])