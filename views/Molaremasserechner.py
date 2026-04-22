import streamlit as st
import re
import periodictable as pt

st.title ("Molaremasse-Rechner")

formula = st.text_input("Gib eine chemische Formel ein (z.B. H2O):")
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
if formula:
    composition = parse_formula(formula)
    
    st.write("Zusammensetzung:", composition)
    
    molar_mass = calculate_molar_mass(composition)
    
    if molar_mass:
        st.success(f"Molare Masse: {molar_mass:.3f} g/mol")
    else:
        st.error("Unbekanntes Element!")