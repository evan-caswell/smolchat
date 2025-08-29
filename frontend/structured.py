import streamlit as st
import httpx
import json
from typing import Any
from ui_defaults import (
    DV,
    API_BASE_URL,
    MODEL_NAME,
    RECIPE_EXAMPLE,
    RECIPE_MD,
    EVENT_EXAMPLE,
    EVENT_MD,
    TIPS_MD,
)

st.set_page_config(page_title=f"{MODEL_NAME} - Structured Output", layout="centered")
st.title(f"{MODEL_NAME} - Structured Output")

with st.sidebar:
    st.header("Schema")
    response_type = st.radio("Response type", ["Recipe", "Event"])

    st.divider()
    st.header("Model Settings")

    if st.button("Reset Model Settings", use_container_width=True):
        for k, v in DV.items():
            st.session_state[k] = v
        st.rerun()

    st.number_input(
        "Seed (zero for no seed)", min_value=0, value=DV["seed"], key="seed"
    )
    st.slider(
        "Temperature", 0.0, 2.0, step=0.1, value=DV["temperature"], key="temperature"
    )
    st.number_input(
        "Max Tokens",
        min_value=32,
        max_value=2048,
        step=32,
        value=DV["max_tokens"],
        key="max_tokens",
    )
    st.slider("Top P", 0.0, 1.0, step=0.01, value=DV["top_p"], key="top_p")
    st.slider(
        "Presence Penalty",
        -2.0,
        2.0,
        step=0.1,
        value=DV["presence_penalty"],
        key="presence_penalty",
    )
    st.slider(
        "Frequency Penalty",
        -2.0,
        2.0,
        step=0.1,
        value=DV["frequency_penalty"],
        key="frequency_penalty",
    )
    st.text_input(
        "Stop Word(s) (no spaces)",
        value=DV["stop"],
        key="stop",
        placeholder="separate,with,commas",
    )
    st.number_input(
        "Number of Responses",
        min_value=1,
        max_value=10,
        step=1,
        value=DV["n"],
        key="n",
        disabled=True,
    )
    st.checkbox("Stream", value=DV["stream"], key="stream", disabled=True)
    st.number_input("Top K", min_value=0, step=1, value=DV["top_k"], key="top_k")
    st.slider("Min P", 0.0, 1.0, step=0.01, value=DV["min_p"], key="min_p")
    st.slider("Typical P", 0.0, 1.0, step=0.1, value=DV["typical_p"], key="typical_p")
    st.slider("Tail-Free Sampling", 0.9, 1.0, step=0.01, value=DV["tfs_z"], key="tfs_z")
    st.slider(
        "Repeat Penalty",
        1.0,
        3.0,
        step=0.1,
        value=DV["repeat_penalty"],
        key="repeat_penalty",
    )
    st.number_input(
        "Repeat Last n",
        min_value=-1,
        step=1,
        value=DV["repeat_last_n"],
        key="repeat_last_n",
    )
    st.number_input(
        "Mirostat Mode",
        min_value=0,
        max_value=2,
        step=1,
        value=DV["mirostat_mode"],
        key="mirostat_mode",
    )
    st.number_input(
        "Mirostat Tau",
        min_value=0.0,
        step=0.1,
        value=DV["mirostat_tau"],
        key="mirostat_tau",
    )
    st.number_input(
        "Mirostat eta",
        min_value=0.0,
        step=0.1,
        value=DV["mirostat_eta"],
        key="mirostat_eta",
    )

# Example: get current settings as a dict
settings = {k: st.session_state[k] for k in DV.keys()}

with st.popover("Schema Info"):
    st.markdown(RECIPE_MD)
    st.json(RECIPE_EXAMPLE)
    st.markdown(EVENT_MD)
    st.json(EVENT_EXAMPLE)

with st.form(key="prompt_form", clear_on_submit=True):
    prompt = st.text_area("Prompt")
    submitted = st.form_submit_button("Send")

if submitted:
    if len(prompt.strip()) < 1:
        st.warning("Prompt cannot be blank.")
    else:
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "response_type": response_type.lower().replace(" ", "_"),
        } | settings

        if payload["seed"] == 0:
            payload["seed"] = None

        s = (
            payload.get("stop") or ""
        ).strip()  # pyright: ignore[reportAttributeAccessIssue]
        payload["stop"] = (
            None if not s else [w.strip() for w in s.split(",") if w.strip()]
        )

        url = f"{API_BASE_URL}structured"
        try:
            with httpx.Client(timeout=60.0) as client:
                r = client.post(url=url, json=payload)
                r.raise_for_status()
                data = r.json()
                st.success("Success")
                st.json(data)
        except Exception as e:
            st.error(f"Error: {e}")

with st.popover("Tips"):
    st.markdown(TIPS_MD)
