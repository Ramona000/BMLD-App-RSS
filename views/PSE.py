import streamlit as st
import streamlit.components.v1 as components
from views.Hilfefenster import show_help, show_navigationst.title("Periodensystem")

st.title("Periodensystem")

html_code = """
<iframe src="https://ptable.com/#Properties"
width="100%" height="800"></iframe>
"""

components.html(html_code, height=800)

help_text = [
    "Gib Stoffmenge und Volumen ein.",
    "Klicke auf Berechnen, um die Konzentration zu erhalten.",
    "Du kommst immer noch nicht weiter? Dann gehts dir wie uns, also frag doch einfach ChatGPT! :)",
    "[Frag ChatGPT!](https://chat.openai.com)"
]

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Zur Startseite"):
        st.switch_page("views/home.py")

with col2:
    show_help(title="Hilfe zum Konzentrationsrechner", text_lines=help_text)