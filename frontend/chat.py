import json
import httpx
import streamlit as st
from typing import Any, cast
from ui_defaults import DV, API_BASE_URL, MODEL_NAME

st.set_page_config(f"{MODEL_NAME} Chat", layout="centered")
st.title(f"{MODEL_NAME} — Chat")

if "history" not in st.session_state:
    st.session_state.history = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]
if "pending_answers" not in st.session_state:
    st.session_state.pending_answers = None


def _on_stream_change() -> None:
    """Ensure `n` stays 1 when streaming is enabled."""
    if st.session_state.stream:
        st.session_state.n = 1


def _on_n_change() -> None:
    """Disable streaming when requesting multiple responses."""
    if st.session_state.n > 1:
        st.session_state.stream = False


disable_n = st.session_state.get("stream", False)
disable_stream = st.session_state.get("n", 1) > 1

with st.sidebar:
    if st.button("Reset Chat", use_container_width=True):
        st.session_state.history = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
        # Clear any pending multi-answer selection state
        st.session_state.pending_answers = None
        st.session_state.pop("candidate_choice", None)
        st.rerun()

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
        disabled=disable_n,
        on_change=_on_n_change,
    )
    st.checkbox(
        "Stream",
        value=DV["stream"],
        key="stream",
        disabled=disable_stream,
        on_change=_on_stream_change,
    )
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

    settings: dict[str, Any] = {k: st.session_state[k] for k in DV.keys()}
    payload = {"messages": st.session_state.history} | settings

    if payload["seed"] == 0:
        payload["seed"] = None

    s: str = str(payload.get("stop") or "").strip()
    payload["stop"] = None if not s else [w.strip() for w in s.split(",") if w.strip()]

    if st.session_state.stream:
        url = f"{API_BASE_URL}/chat/stream"
        running_text = ""
        try:
            with httpx.stream("POST", url, json=payload, timeout=None) as r:
                r.raise_for_status()
                # Stream tokens and update the placeholder for a live typing effect.
                for piece in r.iter_text():
                    running_text += piece
                    placeholder.markdown(running_text)
            st.session_state.history.append(
                {"role": "assistant", "content": running_text}
            )
        except Exception as e:
            st.error(f"Streaming error: {e}")
    else:
        url = f"{API_BASE_URL}/chat"
        try:
            with httpx.Client(timeout=60.0) as client:
                r = client.post(url=url, json=payload)
                r.raise_for_status()
                data = r.json()
        except Exception as e:
            placeholder.markdown(f"Error: {e}")
            st.session_state.history.append(
                {"role": "assistant", "content": f"Error: {e}"}
            )
        else:
            if isinstance(data, dict) and "answers" in data:
                # Persist candidates and render a chooser after this block
                st.session_state.pending_answers = data["answers"]
                placeholder.markdown("Please make a selection")
            else:
                text = data if isinstance(data, str) else json.dumps(data)
                placeholder.markdown(text)
                st.session_state.history.append({"role": "assistant", "content": text})

# Render pending multi-answer chooser outside of the prompt block so it persists across reruns
if st.session_state.pending_answers:
    # Persist multi-answer chooser across reruns; selection appends chosen answer to history.
    st.success("Received multiple candidates")
    with st.form("pick_answer"):
        answers = cast(list[str], st.session_state.pending_answers)
        choice = st.radio(
            "Pick an answer to keep in the chat:",
            answers,
            index=0,
            key="candidate_choice",
        )
        submitted = st.form_submit_button("Confirm")

    if submitted:
        selected: str = cast(str, choice)
        # Append the chosen answer to history and clear chooser state
        st.session_state.history.append(
            {
                "role": "assistant",
                "content": selected,
            }
        )
        st.session_state.pending_answers = None
        st.session_state.pop("candidate_choice", None)
        st.rerun()
