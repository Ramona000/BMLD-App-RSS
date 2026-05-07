import streamlit as st
from views.Hilfefenster import show_help, show_navigation
from functions import show_header

show_header("Einleitung") #Titel und Avatar anzeigen
st.write ("Der Laborrechner ist eine kompakte App für schnelle und präzise Berechnungen im Laboralltag.\n\n"   
           "Wusstest du schon: Häufig genutzte Bezeichnungen können als Favorit gespeichert werden!")

st.markdown("""
**So nutzt du die App:**  
• **Navigation:** Verwende die Seitenleiste oder die Buttons, um zu den verschiedenen Rechnern zu wechseln  
• **Favoriten:** Speichere häufig verwendete Bezeichnungen und Werte als Favoriten für schnelleren Zugriff  
• **Berechnungen:** Gib die erforderlichen Werte ein und klicke auf 'Berechnen'

**Verfügbare Rechner:**  
•  Konzentrationsrechner - Berechne Stoffkonzentrationen  
•  Molare Massenrechner - Bestimme molare Massen von Verbindungen  
•  pH-Wert Rechner - Berechne pH-Werte und Säurekonstanten  
•  Verdünnungsrechner - Erstelle Verdünnungslösungen  
•  Periodensystem - Schau dir Elementeigenschaften an  
•  Und viele weitere Tools...
""")


help_text = [
    "**Tipp:** Starte mit dem Periodensystem, um die nötigen Atom- und Molmassen für deine Berechnungen zu finden!"
]

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Zur Startseite"):
        st.switch_page("views/home.py")

with col2:
    show_help(title="Hilfe zur Einleitung", text_lines=help_text)

