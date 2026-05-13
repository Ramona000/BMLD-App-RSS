import streamlit as st
import re
import periodictable as pt
import pandas as pd

from utils.data_manager import DataManager
from views.Hilfefenster import show_help, show_navigation
from functions import show_header
from functions.Molaremassenrechner import (
    parse_formula,
    calculate_molar_mass,
    speichere_verlauf
)

# HEADER
show_header("Molare Masse-Rechner")
show_navigation(current_page="Molaremasserechner")

# SESSION STATE INIT
if "resultate_mm_rechner" not in st.session_state:
    st.session_state["resultate_mm_rechner"] = pd.DataFrame(
        columns=[
            "timestamp",
            "Molekül",
            "Molare Masse (g/mol)",
            "favorite"
        ]
    )

df = st.session_state["resultate_mm_rechner"]

# INPUT
formula = st.text_input(
    "Gib eine chemische Formel ein.\n\n"
    "Formel muss in Grossbuchstaben sein (z.B. H2O):"
)

calculate = st.button("Berechnen")

if formula:
    st.write(f"Eingegebene Formel: {formula}")

# CALCULATION
if calculate:
    if not formula:
        st.warning("Bitte gib eine Formel ein!")
    else:
        composition = parse_formula(formula)
        st.write("Zusammensetzung:", composition)

        molar_mass = calculate_molar_mass(composition)

        if molar_mass:
            st.success(f"Molare Masse: {molar_mass:.3f} g/mol")

            # 🔥 wichtig: Verlauf speichern muss favorite enthalten
            speichere_verlauf(formula, molar_mass)

            # CSV speichern
            data_manager = DataManager()
            data_manager.save_user_data(df, "data.csv")
        else:
            st.error("Unbekanntes Element!")

# HISTORY
st.subheader("Berechnungshistorie")

df = st.session_state["resultate_mm_rechner"]

# 🔥 FIX: favorite Spalte absichern
if "favorite" not in df.columns:
    df["favorite"] = False
else:
    df["favorite"] = df["favorite"].fillna(False).astype(bool)

# DATA EDITOR (SAFE VERSION)
edited_df = st.data_editor(
    df,
    column_config={
        "favorite": st.column_config.CheckboxColumn("Favorit")
    },
    disabled=[
        "timestamp",
        "Molekül",
        "Molare Masse (g/mol)"
    ],
    hide_index=True,
    use_container_width=True
)

st.session_state["resultate_mm_rechner"] = edited_df

# HELP SECTION
help_text = [
    "Gib eine chemische Formel ein z.B. C6H12O6 für Glucose.",
    "Klicke auf Berechnen, um die molare Masse zu erhalten.",
    "Wenn es nicht klappt: ChatGPT fragen 😄",
    "[Frag ChatGPT!](https://chat.openai.com)"
]

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Zur Startseite"):
        st.switch_page("pages/home.py")

with col2:
    show_help(title="Hilfe zum Molaremasse-Rechner", text_lines=help_text)