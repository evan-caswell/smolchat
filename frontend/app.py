import streamlit as st
from ui_defaults import MODEL_NAME

chat = st.Page("chat.py", title=f"Chat with {MODEL_NAME}")
structured_output = st.Page("structured.py", title="Structured Output")
settings_info = st.Page("info.py", title="Model Settings Information")

pg = st.navigation([chat, structured_output, settings_info])
pg.run()
