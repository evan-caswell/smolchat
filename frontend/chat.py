import os
import httpx
import streamlit as st

API_URL = os.environ.get("API_URL", "http://localhost:8000")

st.set_page_config("SmolLM2 Chat", layout="centered")
st.title("SmolLM2 — Chat")

if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

with st.sidebar:
    st.header("Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.2, 0.05)
    max_tokens = st.number_input("Max tokens", 32, 2048, 512, step=32)
    st.divider()
    if st.button("Reset chat", use_container_width=True):
        st.session_state.history = [{"role": "system", "content": "You are a helpful assistant."}]
        st.rerun()

for msg in st.session_state.history:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

prompt = st.chat_input("Ask SmolLM2 anything…")
if prompt:
    st.session_state.history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("_thinking…_")

    payload = {
        "messages": st.session_state.history,
        "temperature": float(temperature),
        "max_tokens": int(max_tokens),
    }

    try:
        with httpx.Client(timeout=60) as client:
            r = client.post(f"{API_URL}/chat/", json=payload)
            r.raise_for_status()
            data = r.json()
        answer = data["answer"]
    except Exception as e:
        answer = f"Error: {e}"
        placeholder.markdown(answer)

    placeholder.markdown(answer)
    st.session_state.history.append({"role": "assistant", "content": answer})
