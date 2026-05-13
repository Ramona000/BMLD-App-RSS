import streamlit as st
import pandas as pd
import datetime
from views.Hilfefenster import show_help, show_navigation
from utils.data_manager import DataManager
from functions.Verdünnungsrechner import verduennungsrechner, plot_verduennung, speichere_verlauf
from functions import show_header
import os

FILE_PATH = "verdünnungs_verlauf.csv"

if "resultate_verdünnungs_rechner" not in st.session_state:
    if os.path.exists(FILE_PATH):
        st.session_state["resultate_verdünnungs_rechner"] = pd.read_csv(FILE_PATH)
    else:
        st.session_state["resultate_verdünnungs_rechner"] = pd.DataFrame(
            columns=["timestamp", "C1", "C2", "V2", "V1", "favorite"]
        )

show_header("Verdünnungsrechner") #Titel und Avatar anzeigen
show_navigation(current_page="Verdünngsrechner") 

C1 = st.number_input("Anfangskonzentration (C1)", min_value=0.01)
C2 = st.number_input("Zielkonzentration (C2)", min_value=0.01)
V2 = st.number_input("Endvolumen (V2)", min_value=0.01)


if st.button("Berechnen"):

    if C1 > 0 and C2 > 0 and V2 > 0:

        result = verduennungsrechner(C1, C2, V2)

        st.success(f"V1: {result['V1']} ml")

        fig = plot_verduennung(C1, C2, V2, result["V1"])
        st.pyplot(fig)
        speichere_verlauf(result)

        # CSV speichern
        data_manager = DataManager()
        data_manager.save_user_data(
            st.session_state['resultate_verdünnungs_rechner'],
            'data.csv'
        )

    else:
        st.error("Fehlerhafte Eingabe")

st.subheader("Berechnungshistorie")       
# --- NEW CODE to display the history table ---
st.session_state['resultate_verdünnungs_rechner']["favorite"] = (
    st.session_state['resultate_verdünnungs_rechner']["favorite"]
    .fillna(False)
    .astype(bool)
)
st.session_state['resultate_verdünnungs_rechner'] = st.data_editor(
    st.session_state['resultate_verdünnungs_rechner'],
    use_container_width=True
)


# Spezifischer Hilfetext für Verdünnungsrechner
help_text = [
    "Gib die Anfangskonzentration (C1) ein.",
    "Gib die Zielkonzentration (C2) ein.",
    "Gib das Endvolumen (V2) ein.",
    "Klicke auf 'Berechnen', um das Ergebnis zu erhalten.",
    "Du kommst immer noch nicht weiter? Dann gehts dir wie uns, also frag doch einfach ChatGPT! :)",
    "[Frag ChatGPT!](https://chat.openai.com)"
]

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Zur Startseite"):
        st.switch_page("views/home.py")

with col2:
    show_help(title="Hilfe zum Verdünnungsrechner", text_lines=help_text)