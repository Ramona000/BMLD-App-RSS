import streamlit as st

def show_help():

    # CSS nur für unseren Container
    st.markdown("""
    <style>
    .help-button-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
    }
    .help-button-container button {
        border-radius: 50%;
        width: 60px;
        height: 60px;
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    # Container mit eigener Klasse
    st.markdown('<div class="help-button-container">', unsafe_allow_html=True)

    if st.button("❓", key="help_button"):
        st.session_state.show_help = True

    st.markdown('</div>', unsafe_allow_html=True)

    # Popup
    if "show_help" not in st.session_state:
        st.session_state.show_help = False

    if st.session_state.show_help:
        st.markdown("### Hilfe & Support")
        st.write("Du bist überfordert und kommst nicht weiter?")
        st.markdown("[Frag ChatGPT!](https://chat.openai.com)")

        if st.button("Schließen", key="close_help"):
            st.session_state.show_help = False