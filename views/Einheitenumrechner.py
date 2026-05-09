import pandas as pd
import streamlit as st
from functions.Einheitenumrechner import (
    umrechnen_gewicht,
    umrechnen_volumen,
    volumen_zu_gewicht,
    gewicht_zu_volumen,
    speichere_historie
)
from utils.data_manager import DataManager
from views.Hilfefenster import show_help, show_navigation
from functions import show_header

# SESSION STATE
if "resultate_einheitenumrechner" not in st.session_state:
    st.session_state["resultate_einheitenumrechner"] = pd.DataFrame(columns=[
        "timestamp",
        "kategorie",
        "eingabewert",
        "eingabeeinheit",
        "ausgabewert",
        "ausgabeeinheit",
        "substanz_kategorie",
        "substanz",
        "dichte"
    ])

# HEADER
show_header("Einheitenumrechner")
show_navigation(current_page="Einheitenumrechner")

st.write("Hier kannst du verschiedene Einheiten umrechnen.")

# EINHEITEN (nur UI)
gewicht_einheiten = ["µg", "mg", "g", "kg", "t"]
volumen_einheiten = ["µl", "ml", "l", "cm³", "mm³", "m³"]

# SUBSTANZEN (bleibt hier sinnvoll, da UI-abhängig)
substanzen_kategorien = {
    "Standard": {"Wasser": 1.0, "PBS": 1.01, "NaCl 0.9%": 1.005},
    "Zellkultur": {"DMEM": 1.01, "RPMI 1640": 1.01, "FBS": 1.03},
    "Lösungsmittel": {"Ethanol (100%)": 0.789, "Aceton": 0.791},
    "Chemikalien": {"Formaldehyd": 1.03, "NaOH": 1.04}
}

# KATEGORIE AUSWAHL
kategorien = [
    "Flüssigkeiten in Gewicht",
    "Gewicht in Flüssigkeit",
    "Gewicht in Gewicht",
    "Flüssigkeit in Flüssigkeit"
]

kategorie = st.selectbox("Kategorie wählen", kategorien)

# FLÜSSIGKEIT → GEWICHT
if kategorie == "Flüssigkeiten in Gewicht":

    st.subheader("Flüssigkeit → Gewicht")

    volumen = st.number_input("Volumen", min_value=0.0, step=0.01)
    volumen_einheit = st.selectbox("Volumeneinheit", volumen_einheiten)

    kategorie_substanz = st.selectbox(
        "Substanz-Kategorie",
        list(substanzen_kategorien.keys())
    )

    substanz = st.selectbox(
        "Substanz",
        list(substanzen_kategorien[kategorie_substanz].keys())
    )

    dichte = substanzen_kategorien[kategorie_substanz][substanz]

    ziel_einheit = st.selectbox("Ziel-Einheit", gewicht_einheiten)

    if st.button("Umrechnen"):

        ergebnis = volumen_zu_gewicht(
            volumen,
            volumen_einheit,
            dichte,
            ziel_einheit
        )

        st.success(f"{ergebnis:.4f} {ziel_einheit}")

        speichere_historie(
            kategorie,
            volumen,
            volumen_einheit,
            ergebnis,
            ziel_einheit,
            kategorie_substanz,
            substanz,
            dichte
        )

# GEWICHT → FLÜSSIGKEIT
elif kategorie == "Gewicht in Flüssigkeit":

    st.subheader("Gewicht → Flüssigkeit")

    gewicht = st.number_input("Gewicht", min_value=0.0, step=0.01)
    gewicht_einheit = st.selectbox("Gewichtseinheit", gewicht_einheiten)

    kategorie_substanz = st.selectbox(
        "Substanz-Kategorie",
        list(substanzen_kategorien.keys())
    )

    substanz = st.selectbox(
        "Substanz",
        list(substanzen_kategorien[kategorie_substanz].keys())
    )

    dichte = substanzen_kategorien[kategorie_substanz][substanz]

    ziel_einheit = st.selectbox("Ziel-Einheit", volumen_einheiten)

    if st.button("Umrechnen"):

        ergebnis = gewicht_zu_volumen(
            gewicht,
            gewicht_einheit,
            dichte,
            ziel_einheit
        )

        st.success(f"{ergebnis:.4f} {ziel_einheit}")

        speichere_historie(
            kategorie,
            gewicht,
            gewicht_einheit,
            ergebnis,
            ziel_einheit,
            kategorie_substanz,
            substanz,
            dichte
        )

# GEWICHT → GEWICHT
elif kategorie == "Gewicht in Gewicht":

    st.subheader("Gewicht → Gewicht")

    gewicht = st.number_input("Gewicht", min_value=0.0, step=0.01)

    von_einheit = st.selectbox("Von", gewicht_einheiten)
    zu_einheit = st.selectbox("Nach", gewicht_einheiten)

    if st.button("Umrechnen"):

        ergebnis = umrechnen_gewicht(
            gewicht,
            von_einheit,
            zu_einheit
        )

        st.success(f"{ergebnis:.4f} {zu_einheit}")

        speichere_historie(
            kategorie,
            gewicht,
            von_einheit,
            ergebnis,
            zu_einheit
        )

# FLÜSSIGKEIT → FLÜSSIGKEIT
elif kategorie == "Flüssigkeit in Flüssigkeit":

    st.subheader("Flüssigkeit → Flüssigkeit")

    volumen = st.number_input("Volumen", min_value=0.0, step=0.01)

    von_einheit = st.selectbox("Von", volumen_einheiten)
    zu_einheit = st.selectbox("Nach", volumen_einheiten)

    if st.button("Umrechnen"):

        ergebnis = umrechnen_volumen(
            volumen,
            von_einheit,
            zu_einheit
        )

        st.success(f"{ergebnis:.4f} {zu_einheit}")

        speichere_historie(
            kategorie,
            volumen,
            von_einheit,
            ergebnis,
            zu_einheit
        )

# HISTORIE + CSV
data_manager = DataManager()

data_manager.save_user_data(
    st.session_state["resultate_einheitenumrechner"],
    "data.csv"
)

st.subheader("Berechnungshistorie")

st.dataframe(
    st.session_state["resultate_einheitenumrechner"],
    use_container_width=True
)

# NAVIGATION
col1, col2 = st.columns(2)

with col1:
    if st.button("Zur Startseite"):
        st.switch_page("views/home.py")

with col2:
    show_help(title="Hilfe zum Einheitenumrechner")