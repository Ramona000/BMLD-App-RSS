import streamlit as st
import streamlit.components.v1 as components
from views.Hilfefenster import show_help, show_navigation
from functions import show_header

show_header("Periodensystem") #Titel und Avatar anzeigen
show_navigation(current_page="Konzentrationsrechner") 

html_code = """
<iframe src="https://ptable.com/#Properties"
width="100%" height="800"></iframe>
"""

components.html(html_code, height=800)

help_text = [
    "**Das Periodensystem der Elemente (PSE)** ist eine Übersicht aller bekannten chemischen Elemente, organisiert nach ihren Eigenschaften.",
    "",
    "**So nutzt du das Periodensystem:**",
    "• **Klick auf ein Element** - Zeige Details wie Atommasse, Elektronenkonfiguration und weitere Eigenschaften",
    "• **Farben bedeuten Elementgruppen** - Verschiedene Farben kennzeichnen Metalle, Nichtmetalle, Halogene usw.",
    "• **Periodenzahl (Zeilen)** - Bestimmt die Anzahl der Elektronenschalen",
    "• **Gruppenzahl (Spalten)** - Bestimmt die Anzahl der Valenzelektronen",
    "",
    "**Wichtige Informationen pro Element:**",
    "• Atommasse (durchschnittliche Masse)",
    "• Ordnungszahl (Anzahl der Protonen)",
    "• Elektronenkonfiguration",
    "• Siedepunkt, Schmelzpunkt und Dichte",
    "",
    "Du kommst immer noch nicht weiter? Dann gehts dir wie uns, also frag doch einfach ChatGPT! :)",
    "[Frag ChatGPT!](https://chat.openai.com)"
]

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Zur Startseite"):
        st.switch_page("views/home.py")

with col2:
    show_help(title="Hilfe zum Periodensystem", text_lines=help_text)