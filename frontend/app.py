import streamlit as st
from ui_defaults import MODEL_NAME, DV

# Seed session state with defaults on first load, then rerun so widgets bind values.
if "init_ui" not in st.session_state:
    st.session_state.init_ui = False

if not st.session_state.init_ui:
    for k, v in DV.items():
        st.session_state[k] = v
    st.session_state.init_ui = True
    st.rerun()

chat = st.Page("chat.py", title=f"Chat with {MODEL_NAME}")
structured_output = st.Page("structured.py", title="Structured Output")
settings_info = st.Page("info.py", title="Model Settings Information")

pg = st.navigation([chat, structured_output, settings_info])
pg.run()
