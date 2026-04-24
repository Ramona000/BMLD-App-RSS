import streamlit as st
from views.Hilfefenster import show_help, show_navigation
import streamlit as st


show_navigation(current_page="Einheitenumrechner") 
st.title("Einheitenumrechner")
st.write("Hier kannst du verschiedene Einheiten umrechnen. Wähle die Kategorie und die Einheiten aus, die du umrechnen möchtest.")


# Kategorie-Auswahl
kategorien = [
    "Flüssigkeiten in Gewicht",
    "Gewicht in Flüssigkeit",
    "Gewicht in Gewicht",
    "Flüssigkeit in Flüssigkeit"
]
kategorie = st.selectbox("Wähle eine Kategorie", kategorien)

# Einheitenlisten
gewicht_einheiten = ["µg", "mg", "g", "kg", "t"]
volumen_einheiten = ["µl", "ml", "l", "m³", "cm³", "mm³"]  # Ergänzt um Mikro-, Kubik- und weitere
flaeche_einheiten = ["cm²", "m²", "mm²"]  # Für Quadrat-Einheiten (falls relevant)

# Substanzen-Kategorien
substanzen_kategorien = {
    "Standard": {
        "Wasser": 1.0,
        "PBS (Phosphate Buffered Saline)": 1.01,
        "NaCl 0.9% (physiologisch)": 1.005,
    },
    
    "Zellkultur": {
        "DMEM Medium": 1.01,
        "RPMI 1640": 1.01,
        "FBS (Fötales Kälberserum)": 1.03,
        "Serum": 1.025,
    },
    
    "Lösungsmittel": {
        "Ethanol (100%)": 0.789,
        "Ethanol (70%)": 0.867,
        "Methanol": 0.792,
        "Isopropanol": 0.786,
        "Aceton": 0.791,
        "DMSO": 1.10,
        "Glycerol": 1.26,
    },
    
    "Chemikalien": {
        "Formaldehyd (4%)": 1.03,
        "Essigsäure (100%)": 1.05,
        "Salzsäure (1M)": 1.02,
        "Natronlauge (1M NaOH)": 1.04,
    },
    
    "Detergenzien": {
        "Triton X-100": 1.07,
        "Tween 20": 1.10,
    },
    
    "Biologische Proben": {
        "Blut (Vollblut)": 1.06,
    }
}

if kategorie == "Flüssigkeiten in Gewicht":
    st.subheader("Flüssigkeiten in Gewicht umrechnen")
    st.write("Gib das Volumen und die Dichte ein, um die Masse zu berechnen. Formel: Masse = Volumen × Dichte")
    
    # Eingabefelder
    volumen = st.number_input("Volumen", min_value=0.0, step=0.01, help="Gib das Volumen ein (z.B. 100 für 100 ml)")
    volumen_einheit = st.selectbox("Einheit des Volumens", volumen_einheiten, help="Wähle die Einheit des Volumens")
    
    # Substanz-Kategorie und Substanz
    kategorie_substanz = st.selectbox("Substanz-Kategorie", list(substanzen_kategorien.keys()))
    substanzen_liste = list(substanzen_kategorien[kategorie_substanz].keys())
    substanz = st.selectbox("Substanz", substanzen_liste)
    
    dichte = substanzen_kategorien[kategorie_substanz][substanz]
    st.write(f"Vordefinierte Dichte für {substanz}: {dichte} g/ml")
    
    # Einheit für das Ergebnis
    ergebnis_einheit = st.selectbox("Einheit des Ergebnisses", gewicht_einheiten, help="Wähle die Einheit für die Masse")
    
    # Berechnung
    if st.button("Umrechnen"):
        if volumen <= 0 or dichte <= 0:
            st.error("Volumen und Dichte müssen größer als 0 sein!")
        else:
            # Umrechnung des Volumens in ml (Basis-Einheit)
            if volumen_einheit == "l":
                volumen_ml = volumen * 1000
            elif volumen_einheit == "m³":
                volumen_ml = volumen * 1_000_000
            elif volumen_einheit == "cm³":
                volumen_ml = volumen  # 1 cm³ = 1 ml
            elif volumen_einheit == "mm³":
                volumen_ml = volumen / 1000  # 1 mm³ = 0.001 ml
            elif volumen_einheit == "µl":
                volumen_ml = volumen / 1000  # 1 µl = 0.001 ml
            else:  # ml
                volumen_ml = volumen
            
            # Masse in g berechnen
            masse_g = volumen_ml * dichte
            
            # In gewünschte Einheit umrechnen
            if ergebnis_einheit == "µg":
                masse = masse_g * 1_000_000
            elif ergebnis_einheit == "mg":
                masse = masse_g * 1000
            elif ergebnis_einheit == "kg":
                masse = masse_g / 1000
            elif ergebnis_einheit == "t":
                masse_g / 1_000_000
            else:  # g
                masse = masse_g
            
            st.success(f"Die Masse beträgt: {masse:.10g} {ergebnis_einheit}")
            st.write(f"Berechnung: {volumen} {volumen_einheit} × {dichte} g/ml = {masse:.10g} {ergebnis_einheit}")

elif kategorie == "Gewicht in Flüssigkeit":
    st.subheader("Gewicht in Flüssigkeit umrechnen")
    st.write("Gib das Gewicht und die Dichte ein, um das Volumen zu berechnen. Formel: Volumen = Gewicht / Dichte")
    
    # Eingabefelder
    gewicht = st.number_input("Gewicht", min_value=0.0, step=0.01, help="Gib das Gewicht ein (z.B. 100 für 100 g)")
    gewicht_einheit = st.selectbox("Einheit des Gewichts", gewicht_einheiten, help="Wähle die Einheit des Gewichts")
    
    # Substanz-Kategorie und Substanz
    kategorie_substanz = st.selectbox("Substanz-Kategorie", list(substanzen_kategorien.keys()))
    substanzen_liste = list(substanzen_kategorien[kategorie_substanz].keys())
    substanz = st.selectbox("Substanz", substanzen_liste)
    
    dichte = substanzen_kategorien[kategorie_substanz][substanz]
    st.write(f"Vordefinierte Dichte für {substanz}: {dichte} g/ml")
    
    ergebnis_einheit = st.selectbox("Einheit des Ergebnisses", volumen_einheiten, help="Wähle die Einheit für das Volumen")
    
    if st.button("Umrechnen"):
        if gewicht <= 0 or dichte <= 0:
            st.error("Gewicht und Dichte müssen größer als 0 sein!")
        else:
            # Gewicht in g umrechnen
            if gewicht_einheit == "µg":
                gewicht_g = gewicht / 1_000_000
            elif gewicht_einheit == "mg":
                gewicht_g = gewicht / 1000
            elif gewicht_einheit == "kg":
                gewicht_g = gewicht * 1000
            elif gewicht_einheit == "t":
                gewicht_g = gewicht * 1_000_000
            else:  # g
                gewicht_g = gewicht
            
            # Volumen in ml berechnen
            volumen_ml = gewicht_g / dichte
            
            # In gewünschte Einheit umrechnen
            if ergebnis_einheit == "l":
                volumen = volumen_ml / 1000
            elif ergebnis_einheit == "m³":
                volumen = volumen_ml / 1_000_000
            elif ergebnis_einheit == "cm³":
                volumen = volumen_ml  # 1 ml = 1 cm³
            elif ergebnis_einheit == "mm³":
                volumen = volumen_ml * 1000
            elif ergebnis_einheit == "µl":
                volumen = volumen_ml * 1000
            else:  # ml
                volumen = volumen_ml
            
            st.success(f"Das Volumen beträgt: {volumen:.10g} {ergebnis_einheit}")
            st.write(f"Berechnung: {gewicht} {gewicht_einheit} / {dichte} g/ml = {volumen:.g} {ergebnis_einheit}")

elif kategorie == "Gewicht in Gewicht":
    st.subheader("Gewicht in Gewicht umrechnen")
    st.write("Rechne Gewichtseinheiten um.")
    
    gewicht = st.number_input("Gewicht", min_value=0.0, step=0.01)
    von_einheit = st.selectbox("Von Einheit", gewicht_einheiten)
    zu_einheit = st.selectbox("Zu Einheit", gewicht_einheiten)
    
    if st.button("Umrechnen"):
        if gewicht <= 0:
            st.error("Gewicht muss größer als 0 sein!")
        else:
            # In g umrechnen
            if von_einheit == "µg":
                gewicht_g = gewicht / 1_000_000
            elif von_einheit == "mg":
                gewicht_g = gewicht / 1000
            elif von_einheit == "kg":
                gewicht_g = gewicht * 1000
            elif von_einheit == "t":
                gewicht_g = gewicht * 1_000_000
            else:
                gewicht_g = gewicht
            
            # In Ziel-Einheit
            if zu_einheit == "µg":
                ergebnis = gewicht_g * 1_000_000
            elif zu_einheit == "mg":
                ergebnis = gewicht_g * 1000
            elif zu_einheit == "kg":
                ergebnis = gewicht_g / 1000
            elif zu_einheit == "t":
                ergebnis = gewicht_g / 1_000_000
            else:
                ergebnis = gewicht_g
            
            st.success(f"{gewicht} {von_einheit} = {ergebnis:.g} {zu_einheit}")

elif kategorie == "Flüssigkeit in Flüssigkeit":
    st.subheader("Flüssigkeit in Flüssigkeit umrechnen")
    st.write("Rechne Volumeneinheiten um.")
    
    volumen = st.number_input("Volumen", min_value=0.0, step=0.01)
    von_einheit = st.selectbox("Von Einheit", volumen_einheiten)
    zu_einheit = st.selectbox("Zu Einheit", volumen_einheiten)
    
    if st.button("Umrechnen"):
        if volumen <= 0:
            st.error("Volumen muss größer als 0 sein!")
        else:
            # In ml umrechnen
            if von_einheit == "l":
                volumen_ml = volumen * 1000
            elif von_einheit == "m³":
                volumen_ml = volumen * 1_000_000
            elif von_einheit == "cm³":
                volumen_ml = volumen
            elif von_einheit == "mm³":
                volumen_ml = volumen / 1000
            elif von_einheit == "µl":
                volumen_ml = volumen / 1000
            else:
                volumen_ml = volumen
            
            # In Ziel-Einheit
            if zu_einheit == "l":
                ergebnis = volumen_ml / 1000
            elif zu_einheit == "m³":
                ergebnis = volumen_ml / 1_000_000
            elif zu_einheit == "cm³":
                ergebnis = volumen_ml
            elif zu_einheit == "mm³":
                ergebnis = volumen_ml * 1000
            elif zu_einheit == "µl":
                ergebnis = volumen_ml * 1000
            else:
                ergebnis = volumen_ml
            
            st.success(f"{volumen} {von_einheit} = {ergebnis:.10g} {zu_einheit}")
# ... bestehender Code ...


# ... Rest des Codes, inkl. col1, col2 für Hilfe und Zur Startseite ...
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Zur Startseite"):
        st.switch_page("views/home.py")

with col2:
    show_help(title="Hilfe zum Einheitenumrechner")