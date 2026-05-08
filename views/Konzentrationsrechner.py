import pandas as pd
import streamlit as st

from utils.data_manager import DataManager
from views.Hilfefenster import show_help, show_navigation
from functions import show_header

# Session State initialisieren
if 'resultate_konzentrations_rechner' not in st.session_state:
    st.session_state['resultate_konzentrations_rechner'] = pd.DataFrame(
        columns=["timestamp", "stoffmenge", "volumen", "konzentration"]
    )

show_header("🧪 Konzentrationsrechner")
show_navigation(current_page="Konzentrationsrechner")

st.write("Berechne die molare Konzentration (c = n / V)")

# Eingaben
stoffmenge = st.number_input("Stoffmenge n (in mol)", min_value=0.0)
volumen = st.number_input("Volumen V (in Liter)", min_value=0.0)

konzentration = None

# Berechnung
if st.button("Berechnen"):
    if volumen > 0:
        konzentration = stoffmenge / volumen
        st.success(f"Konzentration: {konzentration:.4f} mol/L")

        # Verlauf speichern
        st.session_state['resultate_konzentrations_rechner'] = pd.concat(
            [
                st.session_state['resultate_konzentrations_rechner'],
                pd.DataFrame([{
                    "timestamp": pd.Timestamp.now(),
                    "stoffmenge": stoffmenge,
                    "volumen": volumen,
                    "konzentration": konzentration
                }])
            ],
            ignore_index=True
        )

        # CSV speichern
        data_manager = DataManager()
        data_manager.save_user_data(
            st.session_state['resultate_konzentrations_rechner'],
            'data.csv'
        )
    else:
        st.warning("Bitte ein Volumen größer als 0 eingeben!")

st.subheader("Berechnungshistorie")
st.dataframe(st.session_state['resultate_konzentrations_rechner'])

help_text = [
    "Gib Stoffmenge und Volumen ein.",
    "Klicke auf Berechnen, um die Konzentration zu erhalten.",
    "Du kommst immer noch nicht weiter? Dann gehts dir wie uns, also frag doch einfach ChatGPT! :)",
    "[Frag ChatGPT!](https://chat.openai.com)"
]

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Zur Startseite"):
        st.switch_page("views/home.py")

with col2:
    show_help(title="Hilfe zum Konzentrationsrechner", text_lines=help_text)