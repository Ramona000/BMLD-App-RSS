import streamlit as st
from views.Hilfefenster import show_help, show_navigation

show_navigation(current_page="Konzentrationsrechner") 
st.title("🧪 Konzentrationsrechner")

st.write("Berechne die molare Konzentration (c = n / V)")


#Eingabefelder 
stoffmenge = st.number_input("Stoffmenge n (in mol)", min_value=0.0)
volumen = st.number_input("Volumen V (in Liter)", min_value=0.0)

#Berechnung
if volumen > 0:
    konzentration = stoffmenge / volumen
    st.success(f"Konzentration: {konzentration:.4f} mol/L")
else:
    st.warning("Bitte ein Volumen größer als 0 eingeben!")

#Berechnungsbutton 
if st.button("Berechnen"):
    if volumen > 0:
        konzentration = stoffmenge / volumen
        st.success(f"Konzentration: {konzentration:.4f} mol/L")
    else:
        st.warning("Bitte ein Volumen größer als 0 eingeben!")

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