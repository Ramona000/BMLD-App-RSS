print("MOLARE MASSEN MODUL WIRD GELADEN")
import re
from turtle import st
import periodictable as pt
from datetime import datetime
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
        "Molekül": formel,
        "Molare Masse (g/mol)": round(molare_masse, 3),
        "favorite": False
    }

    if 'resultate_mm_rechner' not in st.session_state:
        st.session_state['resultate_mm_rechner'] = pd.DataFrame(
            columns=[
                'timestamp',
                'Molekül',
                'Molare Masse (g/mol)',
                'favorite: False'
            ]
        )

    st.session_state['resultate_mm_rechner'] = pd.concat(
        [
            st.session_state['resultate_mm_rechner'],
            pd.DataFrame([result])
        ],
        ignore_index=True
    )

    return st.session_state['resultate_mm_rechner']