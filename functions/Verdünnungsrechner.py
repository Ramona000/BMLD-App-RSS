print(" Verdünnungsrechner MODULE WIRD GELADEN")
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

def speichere_verlauf(result):
    """
    Speichert eine Verdünnungs-Berechnung:
    - in Streamlit Session-State (schnell)
    - in CSV Datei (persistent nach Logout/Login)
    """

    import pandas as pd
    import streamlit as st
    import os

    FILE_PATH = "verdünnungs_verlauf.csv"

    # ----------------------------
    # neuer Eintrag
    # ----------------------------
    neuer_eintrag = pd.DataFrame([{
        "timestamp": pd.Timestamp.now(),
        "C1": result.get("C1"),
        "C2": result.get("C2"),
        "V2": result.get("V2"),
        "V1": result.get("V1"),
        "favorite": False
    }])

    # ----------------------------
    # CSV laden (falls vorhanden)
    # ----------------------------
    if os.path.exists(FILE_PATH):
        df = pd.read_csv(FILE_PATH)
    else:
        df = pd.DataFrame(columns=["timestamp", "C1", "C2", "V2", "V1", "favorite"])

    # ----------------------------
    # neuen Eintrag anhängen
    # ----------------------------
    df = pd.concat([df, neuer_eintrag], ignore_index=True)

    # ----------------------------
    # CSV speichern (persistenz)
    # ----------------------------
    df.to_csv(FILE_PATH, index=False)

    # ----------------------------
    # Session-State aktualisieren
    # ----------------------------
    st.session_state["resultate_verdünnungs_rechner"] = df

    return df