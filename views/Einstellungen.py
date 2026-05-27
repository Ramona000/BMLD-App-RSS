import streamlit as st
from functions import show_header
from utils.data_manager import DataManager

show_header("⚙️ Einstellungen") #Titel und Avatar anzeigen

# Initialisiere DataManager für Persistierung
data_manager = DataManager()

#Definiert welcher Tab beim öffnen der Seite gezeigt wird
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "settings"

if "selected_avatar" not in st.session_state:
    # Lade Avatar aus Datei, falls vorhanden, sonst Standardavatar
    saved_avatar = data_manager.load_user_data('user_avatar.json', initial_value={"avatar": "👤"})
    st.session_state.selected_avatar = saved_avatar.get("avatar", "👤")

#oberer, fixer Teil der Seite mit den Tabs
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

        avatars = ["🥼", "🧪", "🦠", "☢️", "🫧", "💥", "🧤", "🪠"]
        cols = st.columns(4)

        for i, avatar in enumerate(avatars):
            with cols[i % 4]:

                is_selected = st.session_state.selected_avatar == avatar

                if st.button(avatar, key=f"avatar_{avatar}"):
                    st.session_state.selected_avatar = avatar
                    # Speichere Avatar persistent in Datei
                    data_manager.save_user_data({"avatar": avatar}, 'user_avatar.json')
                    st.rerun()
                

    elif st.session_state.active_tab == "password":
        st.header("Passwort ändern")
        
        from utils.login_manager import LoginManager
        from utils.data_manager import DataManager
        
        login_mgr = LoginManager(DataManager())

        current_password = st.text_input("Aktuelles Passwort", type="password")
        new_password = st.text_input("Neues Passwort", type="password")
        confirm_password = st.text_input("Neues Passwort bestätigen", type="password")
        
        st.info("Das Passwort muss 8-20 Zeichen lang sein und enthalten: Großbuchstabe, Kleinbuchstabe, Ziffer, Sonderzeichen (@$!%*?&)")

        if st.button("Passwort ändern"):
            username = st.session_state.get("username") or st.session_state.get("name")
            
            if new_password != confirm_password:
                st.error("Die neuen Passwörter stimmen nicht überein.")
            else:
                success, message = login_mgr.change_password(username, current_password, new_password)
                if success:
                    st.success(message)
                else:
                    st.error(message)