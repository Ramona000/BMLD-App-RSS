import streamlit as st
import pandas as pd

from views.Hilfefenster import show_help, show_navigation
from functions import show_header
from functions.Verdünnungsrechner import (
    verduennungsrechner,
    speichere_verlauf,
    plot_verduennung
)

# SESSION STATE
if "resultate_verdünnungs_rechner" not in st.session_state:
    st.session_state["resultate_verdünnungs_rechner"] = pd.DataFrame(
        columns=["timestamp", "C1", "C2", "V2", "V1", "favorite"]
    )

# HEADER
show_header("Verdünnungsrechner")
show_navigation(current_page="Verdünnungsrechner")

# INPUT
C1 = st.number_input("Anfangskonzentration (C1)", min_value=0.01)
C2 = st.number_input("Zielkonzentration (C2)", min_value=0.01)
V2 = st.number_input("Endvolumen (V2)", min_value=0.01)

# BERECHNUNG
if st.button("Berechnen"):

    if C1 > 0 and C2 > 0 and V2 > 0:

        result = verduennungsrechner(C1, C2, V2)

        st.success(f"V1: {result['V1']} ml")

        fig = plot_verduennung(C1, C2, V2, result["V1"])
        st.pyplot(fig)

        speichere_verlauf(result)

    else:
        st.error("Fehlerhafte Eingabe")

# HISTORIE
st.subheader("Berechnungshistorie")

st.session_state["resultate_verdünnungs_rechner"]["favorite"] = (
    st.session_state["resultate_verdünnungs_rechner"]["favorite"]
    .fillna(False)
    .astype(bool)
)

st.data_editor(
    st.session_state["resultate_verdünnungs_rechner"],
    use_container_width=True
)

# HELP
help_text = [
    "C1 eingeben",
    "C2 eingeben",
    "V2 eingeben",
    "Berechnen klicken"
]

col1, col2 = st.columns(2)

with col1:
    if st.button("Zur Startseite"):
        st.switch_page("views/home.py")

with col2:
    show_help(title="Hilfe", text_lines=help_text)