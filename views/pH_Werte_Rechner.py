import pandas as pd  # --- NEW CODE: add pandas to the imports ---
import streamlit as st
import math
from datetime import datetime
import pytz
from utils.data_manager import DataManager  # --- NEW CODE: import data manager ---

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