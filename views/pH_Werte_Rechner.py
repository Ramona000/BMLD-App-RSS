import pandas as pd
import streamlit as st
import math
import os
import altair as alt
from datetime import datetime
import pytz

from utils.data_manager import DataManager
from views.Hilfefenster import show_help, show_navigation
from functions.ph_Rechner import calculate_ph
from functions import show_header

# PAGE SETUP
show_navigation(current_page="pH_Werte_Rechner")
show_header("pH-Rechner")

st.write(
    "Berechnet deine pH-Werte für dich.\n\n"
    "Pflichtfelder sind mit einem Sternchen (*) gekennzeichnet."
)

# FILE PATH
FILE_PATH = "ph_verlauf.csv"

# SESSION STATE INIT
if "resultate_ph_rechner" not in st.session_state:
    if os.path.exists(FILE_PATH):
        st.session_state["resultate_ph_rechner"] = pd.read_csv(FILE_PATH)
    else:
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

# SPEICHER-FUNKTION (HYBRID)
def speichere_verlauf_ph(result):
    """
    Hybrid-Speicher:
    - Session-State
    - CSV persistent
    """

    result = result.copy()

    result["timestamp"] = datetime.now(pytz.timezone("Europe/Zurich"))
    result["favorite"] = False

    neuer_eintrag = pd.DataFrame([result])

    # CSV laden oder erstellen
    if os.path.exists(FILE_PATH):
        df = pd.read_csv(FILE_PATH)
    else:
        df = pd.DataFrame(columns=neuer_eintrag.columns)

    # anhängen
    df = pd.concat([df, neuer_eintrag], ignore_index=True)

    # speichern
    df.to_csv(FILE_PATH, index=False)

    # session sync
    st.session_state["resultate_ph_rechner"] = df

    return df

# INPUT FORM
with st.form("pH_form"):
    typ = st.selectbox("Wähle deinen Lösungstyp", ["starke Säure", "starke Base"])

    konzentration = st.number_input(
        "Konzentration (mol/L)*",
        min_value=0.000001,
        format="%.6f"
    )

    submitted = st.form_submit_button("pH-Wert berechnen")

# CALCULATION
if submitted:
    result = calculate_ph(typ, konzentration)

    st.success(f"Der pH-Wert beträgt: {result['pH']}")
    st.info(f"Die Lösung ist {result['Kategorie']}.")

    speichere_verlauf_ph(result)

# HISTORY TABLE
st.subheader("Berechnungshistorie")

df = st.session_state["resultate_ph_rechner"]

# safety
if "favorite" not in df.columns:
    df["favorite"] = False

df["favorite"] = df["favorite"].fillna(False).astype(bool)

st.dataframe(df)

# CHART
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
        x=alt.X("timestamp:T", title="Zeitpunkt"),
        y=alt.Y("pH:Q", scale=alt.Scale(domain=[0, 14])),
        color=alt.Color(
            "Typ:N",
            scale=alt.Scale(
                domain=["starke Säure", "starke Base"],
                range=["#d62728", "#1f77b4"]
            )
        )
    )

    points = base.mark_point(size=100)
    lines = base.mark_line()

    chart = alt.layer(
        background,
        (points + lines)
    ).properties(
        width=700,
        height=400,
        title="pH-Verlauf"
    ).interactive()

    st.altair_chart(chart, use_container_width=True)

# HELP
help_text = [
    "Wähle Säure oder Base",
    "Gib Konzentration ein",
    "Klicke Berechnen",
    "Chart zeigt Verlauf",
    "[Frag ChatGPT!](https://chat.openai.com)"
]

col1, col2 = st.columns(2)

with col1:
    if st.button("Zur Startseite"):
        st.switch_page("views/home.py")

with col2:
    show_help("Hilfe zum pH-Rechner", help_text)