import streamlit as st

#Definiert welcher Tab beim öffnen der Seite gezeigt wird
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "settings"

#oberer, fixer Teil der Seite mit den Tabs
st.title("⚙️ Einstellungen")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Einstellungen"):
        st.session_state.active_tab = "settings"
with col2:
    if st.button("Avatar"):
        st.session_state.active_tab = "avatar"
with col3:
    if st.button("Passwort"):
        st.session_state.active_tab = "password"

st.divider()

#unterer, dynamischer Teil
content = st.container()
with content:
    if st.session_state.active_tab == "settings":
        st.header("Allgemeine Einstellungen")

        username = st.text_input("Benutzername")
        email = st.text_input("E-Mail-Adresse")

        st.button("Änderungen speichern")

    elif st.session_state.active_tab == "avatar":
        st.header("Avatar auswählen")

        cols = st.columns(4)

        avatars = ["🥼", "🧪", "🦠", "☢️", "🫧", "💥", "🧤", "🪠"]

        for i, avatar in enumerate(avatars):
            with cols[i % 4]:
                st.button(avatar)
    
    elif st.session_state.active_tab == "password":
        st.header("Passwort ändern")

        current_password = st.text_input("Aktuelles Passwort", type="password")
        new_password = st.text_input("Neues Passwort", type="password")
        confirm_password = st.text_input("Neues Passwort bestätigen", type="password")

        if st.button("Passwort ändern"):
            if new_password == confirm_password:
                st.success("Passwort erfolgreich geändert!")
            else:
                st.error("Die neuen Passwörter stimmen nicht überein.")