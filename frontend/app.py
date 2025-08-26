import streamlit as st
from ui_defaults import DV

chat = st.Page("chat.py", title="Chat with SmolLM2")
structured_output = st.Page("structured.py", title="Structured Output")

pg = st.navigation([chat, structured_output])
pg.run()
