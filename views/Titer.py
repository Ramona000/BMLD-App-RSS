from unittest import result

import streamlit as st
from utils.data_manager import DataManager
from views.Hilfefenster import show_help, show_navigation
from functions import show_header
import pandas as pd

if 'resultate_titer_rechner' not in st.session_state:
    st.session_state['resultate_titer_rechner'] = pd.DataFrame(columns=["timestamp","c_soll","c_eff","titer"])


show_navigation(current_page="Titer") 
show_header("Titer-Rechner") #Titel und Avatar anzeigen

c_soll = st.number_input("Soll-Konzentration (mol/L)", min_value=0.0, format="%.6f")
c_eff = st.number_input("Effektive Konzentration (mol/L)", min_value=0.0, format="%.6f")


def berechne_titer(c_soll, c_eff):
    if c_eff == 0:
        raise ValueError("Die effektive Konzentration darf nicht 0 sein.")
    
    titer = c_eff / c_soll
    return titer

if st.button("Titer berechnen"):
    try:
        titer = berechne_titer(c_soll, c_eff)
        st.success(f"Der berechnete Titer beträgt: {titer:.6f}")

        # Interpretation
        if titer > 1:
            st.success("Lösung ist stärker als erwartet")
        elif titer < 1:
            st.warning("Lösung ist schwächer als erwartet")
        else:
            st.info("Lösung ist genau richtig")

        # Verlauf speichern
        st.session_state['resultate_titer_rechner'] = pd.concat(
            [
                st.session_state['resultate_titer_rechner'],
                pd.DataFrame([{
                    "timestamp": pd.Timestamp.now(),
                    "c_soll": c_soll,
                    "c_eff": c_eff,
                    "titer": titer
                }])
            ],
            ignore_index=True
        )

        # CSV speichern
        data_manager = DataManager()
        data_manager.save_user_data(
            st.session_state['resultate_titer_rechner'],
            'titer_rechner.csv'
        )

    except ValueError as e:
        st.error(str(e))

st.subheader("Berechnungshistorie")       
# --- NEW CODE to display the history table ---
st.dataframe(st.session_state['resultate_titer_rechner'])

# Spezifischer Hilfetext für Titer
help_text = [
    "Gib die Ausgangskonzentration und das Volumen ein.",
    "Klicke auf Berechnen, um das Ergebnis zu sehen.",
    "Du kommst immer noch nicht weiter? Dann gehts dir wie uns, also frag doch einfach ChatGPT! :)",
    "[Frag ChatGPT!](https://chat.openai.com)"
]

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Zur Startseite"):
        st.switch_page("views/home.py")

with col2:
    show_help(title="Hilfe zum Titer-Rechner", text_lines=help_text)