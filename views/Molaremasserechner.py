
import streamlit as st
import re
import periodictable as pt
from utils.data_manager import DataManager
from views.Hilfefenster import show_help, show_navigation
import pandas as pd

show_navigation(current_page="Molaremasserechner") 
st.title ("Molaremasse-Rechner")

if 'resultate_mm_rechner' not in st.session_state:
    st.session_state['resultate_mm_rechner'] = pd.DataFrame(columns=['timestamp','Molekül', 'Molare Masse (g/mol)'])

formula = st.text_input("Gib eine chemische Formel ein. \n\n Formel muss in Grossbuchstaben geschrieben werden! (z.B. H2O):")
#Berechnungsbutton
calculate = st.button("Berechnen")

if formula:
    st.write(f"Eingegebene Formel: {formula}")

#Funktion zum Zerlegen der Formel 
def parse_formula(formula):
    pattern = r'([A-Z][a-z]?)(\d*)'
    matches = re.findall(pattern, formula)
    
    composition = {}
    
    for element, count in matches:
        count = int(count) if count else 1
        composition[element] = composition.get(element, 0) + count
            
    return composition

#Verbindung zu Massen aus PSE
def get_atomic_mass(element):
    try:
        return getattr(pt, element).mass
    except AttributeError:
        return None
    
#Berechnung
def calculate_molar_mass(composition):
    total_mass = 0
    
    for element, count in composition.items():
        mass = get_atomic_mass(element)
        
        if mass is None:
            return None
        
        total_mass += mass * count
        
    return total_mass

#Anzeigen im streamlit
if calculate:
    if not formula:
        st.warning("Bitte gib eine Formel ein!")
    else:
        composition = parse_formula(formula)
        
        st.write("Zusammensetzung:", composition)
        
        molar_mass = calculate_molar_mass(composition)
        
        if molar_mass:
            st.success(f"Molare Masse: {molar_mass:.3f} g/mol")
           
            from datetime import datetime

            result = {
                "timestamp": datetime.now(),
                "Molekül": formula,
                "Molare Masse (g/mol)": round(molar_mass, 3)
            }

            st.session_state['resultate_mm_rechner'] = pd.concat(
                [st.session_state['resultate_mm_rechner'], pd.DataFrame([result])],
                ignore_index=True
            )
        else:
            st.error("Unbekanntes Element!")
 
   
  # --- CODE UPDATE: save data to data manager ---
    data_manager = DataManager()
    data_manager.save_user_data(st.session_state['resultate_mm_rechner'], 'data.csv')
    # --- END OF CODE UPDATE ---

st.subheader("Berechnungshistorie")       
# --- NEW CODE to display the history table ---



# --- NEW CODE to create and display the Altair chart ---
if not st.session_state['resultate_mm_rechner'].empty:
    df = st.session_state['resultate_mm_rechner']
    st.dataframe(df, hide_index=True)
# Spezifischer Hilfetext für Molare Masse
help_text = [
    "Gib eine chemische Formel in Grossbuchstaben ein z.B. C6H12O6 für Glucose.",
    "Klicke auf Berechnen, um die molare Masse zu erhalten.",
    "Du kommst immer noch nicht weiter? Dann gehts dir wie uns, also frag doch einfach ChatGPT! :)",
    "[Frag ChatGPT!](https://chat.openai.com)"
]

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Zur Startseite"):
        st.switch_page("pages/home.py")

with col2:
    show_help(title="Hilfe zum Molaremasse-Rechner", text_lines=help_text)