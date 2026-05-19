print("MOLARE MASSEN MODUL WIRD GELADEN")
import re
import streamlit as st
import pandas as pd
import periodictable as pt
from datetime import datetime
import matplotlib.pyplot as plt
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

def speichere_verlauf(formel, molare_masse):
    """
    Speichert Berechnung in der Historie
    """

    result = {
        "timestamp": datetime.now(),
        "rechner": "Molaremassen-Rechner",
        "Molekül": formel,
        "Molare Masse (g/mol)": round(molare_masse, 3),
        "favorite": False
    }

    if 'resultate_molare_masse_rechner' not in st.session_state:
        st.session_state['resultate_molare_masse_rechner'] = pd.DataFrame(
            columns=[
                'timestamp',
                'rechner',
                'Molekül',
                'Molare Masse (g/mol)',
                'favorite'
            ]
        )

    st.session_state['resultate_molare_masse_rechner'] = pd.concat(
        [
            st.session_state['resultate_molare_masse_rechner'],
            pd.DataFrame([result])
        ],
        ignore_index=True
    )

    return st.session_state['resultate_molare_masse_rechner']

#Grafik
def molare_masse_kreis(formel):

    # Elemente und Anzahl finden
    teile = re.findall(r'([A-Z][a-z]?)(\d*)', formel)

    labels = []
    werte = []

    for element, anzahl in teile:

        try:
            atommasse = pt.elements.symbol(element).mass

            if anzahl == "":
                anzahl = 1
            else:
                anzahl = int(anzahl)

            masse = atommasse * anzahl

            labels.append(element)
            werte.append(masse)

        except:
            pass

    fig, ax = plt.subplots()

    ax.pie(
        werte,
        labels=labels,
        autopct='%1.1f%%'
    )

    ax.set_title(f"Massenanteile von {formel}")

    return fig