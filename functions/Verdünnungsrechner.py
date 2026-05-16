import pandas as pd
import streamlit as st
from datetime import datetime
import pytz
import matplotlib.pyplot as plt


def verduennungsrechner(C1, C2, V2):
    """
    Berechnet Verdünnung: C1 * V1 = C2 * V2
    """

    V1 = (C2 * V2) / C1

    return {
        "timestamp": datetime.now(pytz.timezone("Europe/Zurich")),
        "C1": C1,
        "C2": C2,
        "V2": V2,
        "V1": round(V1, 2)
    }


def speichere_verlauf(result):
    """
    Speichert Verdünnungsberechnung im Streamlit Session-State
    """

    neuer_eintrag = pd.DataFrame([{
        "timestamp": pd.Timestamp.now(),
        "C1": result["C1"],
        "C2": result["C2"],
        "V2": result["V2"],
        "V1": result["V1"],
        "favorite": False
    }])

    if "resultate_verdünnungs_rechner" not in st.session_state:
        st.session_state["resultate_verdünnungs_rechner"] = neuer_eintrag

    else:
        st.session_state["resultate_verdünnungs_rechner"] = pd.concat(
            [st.session_state["resultate_verdünnungs_rechner"], neuer_eintrag],
            ignore_index=True
        )


def plot_verduennung(C1, C2, V2, V1):
    fig, ax = plt.subplots()

    labels = ["C1 (Start)", "C2 (Ziel)"]
    values = [C1, C2]

    ax.bar(labels, values)

    ax.set_title("Verdünnung: Konzentrationsvergleich")
    ax.set_ylabel("Konzentration")

    ax.text(0, C1, f"V1 = {round(V1,2)} ml", ha='center', va='bottom')
    ax.text(1, C2, f"V2 = {round(V2,2)} ml", ha='center', va='bottom')

    return fig