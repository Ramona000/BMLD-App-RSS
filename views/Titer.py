import streamlit as st
import pandas as pd

from utils.data_manager import DataManager
from views.Hilfefenster import show_help, show_navigation
from functions import show_header

from functions.Titer import berechnung_titer, interpretiere_titer, speichere_titer

# SESSION STATE
if "resultate_titer_rechner" not in st.session_state:
    st.session_state["resultate_titer_rechner"] = pd.DataFrame(
        columns=["timestamp", "c_soll", "c_eff", "titer"]
    )

# HEADER & NAVIGATION
show_navigation(current_page="Titer")
show_header("Titer-Rechner")

# INPUT
c_soll = st.number_input(
    "Soll-Konzentration (mol/L)",
    min_value=0.0,
    format="%.6f"
)

c_eff = st.number_input(
    "Effektive Konzentration (mol/L)",
    min_value=0.0,
    format="%.6f"
)

# BERECHNUNG
if st.button("Titer berechnen"):

    try:
        # Berechnung
        titer = berechnung_titer(c_soll, c_eff)

        st.success(f"Der berechnete Titer beträgt: {titer:.6f}")

        # 👉 Interpretation (JETZT korrekt genutzt)
        st.info(interpretiere_titer(titer))

        # 👉 Speicherung (JETZT korrekt genutzt)
        speichere_titer(c_soll, c_eff, titer)

        # CSV speichern
        data_manager = DataManager()
        data_manager.save_user_data(
            st.session_state["resultate_titer_rechner"],
            "titer_rechner.csv"
        )

    except ValueError as e:
        st.error(str(e))

# HISTORIE
st.subheader("Berechnungshistorie")

st.dataframe(
    st.session_state["resultate_titer_rechner"],
    use_container_width=True
)

# HELP
help_text = [
    "Gib Soll- und Effektiv-Konzentration ein.",
    "Klicke auf Berechnen.",
    "Interpretation wird automatisch angezeigt."
]

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("Zur Startseite"):
        st.switch_page("views/home.py")

with col2:
    show_help(title="Hilfe zum Titer-Rechner", text_lines=help_text)