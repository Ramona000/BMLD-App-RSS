print("🔥 TITER MODULE WIRD GELADEN")
def berechnung_titer(c_soll, c_eff):
    if c_eff == 0:
        raise ValueError("Die effektive Konzentration darf nicht 0 sein.")
    
    titer = c_eff / c_soll
    return titer

def interpretiere_titer(titer):
    """
    Gibt eine textuelle Interpretation des Titers zurück.
    """

    if titer > 1:
        return "Lösung ist stärker als erwartet"

    elif titer < 1:
        return "Lösung ist schwächer als erwartet"

    else:
        return "Lösung ist genau richtig"

def speichere_titer(c_soll, c_eff, titer):
    """
    Speichert eine Titer-Berechnung in der Streamlit-Historie.
    """

    import pandas as pd
    import streamlit as st

    neuer_eintrag = pd.DataFrame([{
        "timestamp": pd.Timestamp.now(),
        "c_soll": c_soll,
        "c_eff": c_eff,
        "titer": titer
    }])

    # sicherstellen, dass DataFrame existiert
    if "resultate_titer_rechner" not in st.session_state:
        st.session_state["resultate_titer_rechner"] = neuer_eintrag
    else:
        st.session_state["resultate_titer_rechner"] = pd.concat(
            [st.session_state["resultate_titer_rechner"], neuer_eintrag],
            ignore_index=True
        )