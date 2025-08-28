import streamlit as st
from ui_defaults import MODEL_NAME

chat = st.Page("chat.py", title=f"Chat with {MODEL_NAME}")
structured_output = st.Page("structured.py", title="Structured Output")

pg = st.navigation([chat, structured_output])
pg.run()
