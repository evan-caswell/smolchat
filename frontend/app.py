import streamlit as st

chat = st.Page("chat.py", title="Chat with SmolLM2")

pg = st.navigation([chat])
pg.run()
