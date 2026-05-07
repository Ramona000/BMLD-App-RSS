import streamlit as st

#Titel und Avatar Funktion
def show_header(title):
    left, right = st.columns([8, 1])

    with left:
        st.title(title)

    with right:
        avatar = st.session_state.get("selected_avatar", "👤")
        st.markdown(f"# {avatar}")