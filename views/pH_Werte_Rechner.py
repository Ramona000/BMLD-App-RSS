import pandas as pd  # --- NEW CODE: add pandas to the imports ---
import streamlit as st
import math
from datetime import datetime
import pytz
from utils.data_manager import DataManager  # --- NEW CODE: import data manager ---
import altair as alt

# --- NEW CODE: initialize the session state for the history DataFrame ---
if 'data_df' not in st.session_state:
    st.session_state['data_df'] = pd.DataFrame(columns=['timestamp','Typ', 'Konzentration (mol/L)','pH', 'Kategorie'])

def calculate_ph(typ, konzentration):

    if typ == "starke Säure":
        pH = -math.log10(konzentration)
    else:
        pOH = -math.log10(konzentration)
        pH = 14 - pOH

    if pH < 7:
        category = "sauer"
    elif pH == 7:
        category = "neutral"
    else:
        category = "basisch"

    return {
        "timestamp": datetime.now(pytz.timezone("Europe/Zurich")),
        "Typ": typ,
        "Konzentration (mol/L)": konzentration,
        "pH": round(pH, 2),
        "Kategorie": category
    }
st.title("pH-Rechner")

st.write("Berechnet deine pH-Werte für dich.\n\nPflichtfelder sind mit einem Sternchen (*) gekennzeichnet und müssen für optimale Berechnungen ausgefüllt werden :)")

pH = None 

with st.form("pH_form"):
    typ= st.selectbox("Wähle deinen Lösungstyp", ["starke Säure", "starke Base"])

    konzentration = st.number_input(
    "Konzentration (mol/L)*",
    min_value=0.000001,
    format="%.6f")

    submitted = st.form_submit_button("pH-Wert berechnen")

if submitted:
    result = calculate_ph(typ, konzentration)

    st.success(f"Der pH-Wert der Lösung beträgt: {result['pH']}")

    st.info(f"Die Lösung ist {result['Kategorie']}.")

 # --- NEW CODE to update history in session state and display it ---
    st.session_state['data_df'] = pd.concat([st.session_state['data_df'], pd.DataFrame([result])], ignore_index=True)
 
  # --- CODE UPDATE: save data to data manager ---
    data_manager = DataManager()
    data_manager.save_user_data(st.session_state['data_df'], 'data.csv')
    # --- END OF CODE UPDATE ---

st.subheader("Berechnungshistorie")       
# --- NEW CODE to display the history table ---
st.dataframe(st.session_state['data_df'])



# --- NEW CODE to create and display the Altair chart ---
if not st.session_state['data_df'].empty:
    df = st.session_state['data_df'].copy()

    # 1. Hintergrund-Zonen definieren (Sauer, Neutral, Basisch)
    zones_data = pd.DataFrame([
        {"start": 0, "end": 6.5, "name": "sauer", "color": "#ffcccc"},   # Hellrot
        {"start": 6.5, "end": 7.5, "name": "neutral", "color": "#e2f0d9"}, # Hellgrün
        {"start": 7.5, "end": 14, "name": "basisch", "color": "#ccd9ff"}  # Hellblau
    ])

    zones = alt.Chart(zones_data).mark_rect(opacity=0.3).encode(
        y='start:Q',
        y2='end:Q',
        color=alt.Color('color:N', scale=None) 
    )

    # 2. Basis-Chart (Achsen-Definition)
    base = alt.Chart(df).encode(
        x=alt.X(
            'timestamp:T', 
            title='Zeitpunkt der Messung',
            axis=alt.Axis(format='%d.%m. %H:%M', labelAngle=-45)
        ), # Formatiert als 20.03. 14:00,
        y=alt.Y(
            'pH:Q', 
            scale=alt.Scale(domain=[0, 14]), 
            title='pH-Wert'
        ),
        color=alt.Color('Typ:N', 
                        scale=alt.Scale(domain=['starke Säure', 'starke Base'], 
                                       range=['#d62728', '#1f77b4']),
                        legend=alt.Legend(title="Lösungstyp")
        )
    )

    # 3. Daten-Layer: Punkte und Verbindungslinien
    points = base.mark_point(size=100, filled=True)
    lines = base.mark_line(strokeWidth=2)

    # Tooltips hinzufügen
    chart_elements = (points + lines).encode(
        tooltip=[
            alt.Tooltip('timestamp:T', title='Zeit', format='%H:%M:%S'),
            alt.Tooltip('Typ:N'),
            alt.Tooltip('Konzentration (mol/L):Q'),
            alt.Tooltip('pH:Q')
        ]
    )

    # 4. Alles kombinieren und anzeigen
    final_chart = alt.layer(zones, chart_elements).properties(
        title='Zeitlicher Verlauf der pH-Messungen',
        width=700,
        height=400
    ).interactive()

    st.altair_chart(final_chart, use_container_width=True)
    
if st.button("Zur Startseite"):
    st.switch_page("views/home.py")