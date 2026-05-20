import math
import pandas as pd
import streamlit as st
from datetime import datetime
import pytz
import matplotlib.pyplot as plt
import numpy as np

def calculate_ph(typ, konzentration):
    """
    Berechnet pH-Wert strukturiert
    """

    if typ == "starke Säure":
        pH = -math.log10(konzentration)
    else:
        pOH = -math.log10(konzentration)
        pH = 14 - pOH

    if pH < 7:
        category = "sauer"
    elif pH == 7:
        category = "neutral"
    else:
        category = "basisch"

    return {
        "timestamp": datetime.now(pytz.timezone("Europe/Zurich")),
        "Typ": typ,
        "Konzentration (mol/L)": konzentration,
        "pH": round(pH, 2),
        "Kategorie": category
    }


def speichere_verlauf_ph(result):
    """
    Speichert pH-Rechner Verlauf in Streamlit Session-State
    """

    neuer_eintrag = pd.DataFrame([{
        "timestamp": pd.Timestamp.now(),
        "rechner": "pH-Rechner",
        "Typ": result["Typ"],
        "Konzentration (mol/L)": result["Konzentration (mol/L)"],
        "pH": result["pH"],
        "Kategorie": result["Kategorie"],
        "favorite": False
    }])

    if "resultate_ph_rechner" not in st.session_state:
        st.session_state["resultate_ph_rechner"] = neuer_eintrag

    else:
        st.session_state["resultate_ph_rechner"] = pd.concat(
            [st.session_state["resultate_ph_rechner"], neuer_eintrag],
            ignore_index=True
        )

#Grafik
def ph_skala_farbe(ph_wert=None):

    fig, ax = plt.subplots(figsize=(10, 2))

    # Automatischer Farbverlauf
    farben = plt.cm.rainbow(np.linspace(0, 1, 14))

    for i in range(14):

        ax.barh(
            0,
            1,
            left=i,
            color=farben[i],
            edgecolor='black'
        )

    # Marker für aktuellen pH-Wert
    if ph_wert is not None:

        ax.plot(
            ph_wert - 0.5,
            0,
            marker='v',
            markersize=15,
            color='black'
        )

    ax.set_xlim(0, 14)
    ax.set_ylim(-0.5, 0.5)

    ax.set_xticks(range(15))
    ax.set_yticks([])

    ax.set_title("pH-Skala")

    # Beschriftungen
    ax.text(1.5, 0.3, 'starke Säure', ha='center')
    ax.text(5, 0.3, 'schwache Säure', ha='center')
    ax.text(7, 0.3, 'neutral', ha='center')
    ax.text(9, 0.3, 'schwache Base', ha='center')
    ax.text(12.5, 0.3, 'starke Base', ha='center')

    return fig