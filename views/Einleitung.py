import streamlit as st
from views.Hilfefenster import show_help, show_navigation

st.title ("Einletung")
st.write ("Der Laborrechner ist eine kompakte App für cshnelle und präzise Berchnungen im Laboralltag.")
st.write ("Wusstest du schon: Häufig genutzte Bezeichnungen können als Favorit gespeichert werden!")

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

