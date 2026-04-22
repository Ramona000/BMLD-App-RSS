import streamlit as st

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