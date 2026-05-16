import math
import pandas as pd
import streamlit as st
from datetime import datetime
import pytz


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