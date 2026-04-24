import streamlit as st

# STYLE
st.markdown("""
<style>
div.stButton > button {
    width: 100%;
    height: 80px;
    font-size: 18px;
    border-radius: 12px;
    margin: 5px 0px;
}
</style>
""", unsafe_allow_html=True)

st.title("🧪 Laborrechner")
st.write("Wähle einen Rechner oder eine Funktion:")

col1, col2 = st.columns(2)

with col1:
    if st.button("📘 Einleitung"):
        st.switch_page("views/Einleitung.py")

    if st.button("🧮 Konzentrationsrechner"):
        st.switch_page("views/Konzentrationsrechner.py")

    if st.button("🧬 Molare Masse"):
        st.switch_page("views/Molaremassenrechner.py")

    if st.button("⚗️ pH-Rechner"):
        st.switch_page("views/pH_Werte_Rechner.py")

    if st.button("💧 Verdünnungsrechner"):
        st.switch_page("views/Verdünnungsrechner.py")

with col2:
    if st.button("📏 Einheitenumrechner"):
        st.switch_page("views/Einheitenumrechner.py")

    if st.button("🧪 Titer-Rechner"):
        st.switch_page("views/Titer.py")

    if st.button("🔬 Periodensystem"):
        st.switch_page("views/PSE.py")

    if st.button("⭐ Favoriten"):
        st.switch_page("views/Favoritenliste.py")

    if st.button("⚙️ Einstellungen"):
        st.switch_page("views/Einstellungen.py")