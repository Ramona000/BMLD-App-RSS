import streamlit as st
import streamlit.components.v1 as components

st.title("Periodensystem")

html_code = """
<iframe src="https://ptable.com/#Properties"
width="100%" height="800"></iframe>
"""

components.html(html_code, height=800)
