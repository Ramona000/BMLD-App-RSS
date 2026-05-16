import streamlit as st
import pandas as pd
import altair as alt

from views.Hilfefenster import show_help, show_navigation
from functions import show_header
from functions.ph_Rechner import calculate_ph, speichere_verlauf_ph

# SESSION STATE INIT
if "resultate_ph_rechner" not in st.session_state:
    st.session_state["resultate_ph_rechner"] = pd.DataFrame(
        columns=[
            "timestamp",
            "Typ",
            "Konzentration (mol/L)",
            "pH",
            "Kategorie",
            "favorite"
        ]
    )

# UI HEADER
show_navigation(current_page="pH_Werte_Rechner")
show_header("pH-Rechner")

st.write("Berechnet pH-Werte deiner Lösung.")

# INPUT
typ = st.selectbox("Wähle Lösungstyp", ["starke Säure", "starke Base"])

konzentration = st.number_input(
    "Konzentration (mol/L)",
    min_value=0.000001,
    format="%.6f"
)

# BERECHNUNG
if st.button("pH berechnen"):

    result = calculate_ph(typ, konzentration)

    st.success(f"pH-Wert: {result['pH']}")
    st.info(f"Kategorie: {result['Kategorie']}")

    speichere_verlauf_ph(result)

# HISTORIE
st.subheader("Berechnungshistorie")

df = st.session_state["resultate_ph_rechner"]

if "favorite" not in df.columns:
    df["favorite"] = False

df["favorite"] = df["favorite"].fillna(False).astype(bool)

st.data_editor(df, use_container_width=True)

# CHART (optional, bleibt wie vorher)
if not df.empty:

    df = df.copy()
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    zones = pd.DataFrame([
        {"start": 0, "end": 6.5, "color": "#ffcccc"},
        {"start": 6.5, "end": 7.5, "color": "#e2f0d9"},
        {"start": 7.5, "end": 14, "color": "#ccd9ff"}
    ])

    background = alt.Chart(zones).mark_rect(opacity=0.3).encode(
        y="start:Q",
        y2="end:Q",
        color=alt.Color("color:N", scale=None)
    )

    base = alt.Chart(df).encode(
        x="timestamp:T",
        y=alt.Y("pH:Q", scale=alt.Scale(domain=[0, 14])),
        color="Typ:N"
    )

    chart = alt.layer(
        background,
        base.mark_line(),
        base.mark_point(size=80)
    ).properties(
        width=700,
        height=400,
        title="pH-Verlauf"
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

# HELP
help_text = [
    "Typ wählen",
    "Konzentration eingeben",
    "Berechnen klicken",
    "Verlauf wird gespeichert"
]

col1, col2 = st.columns(2)

with col1:
    if st.button("Zur Startseite"):
        st.switch_page("views/home.py")

with col2:
    show_help("Hilfe zum pH-Rechner", help_text)