import streamlit as st

st.set_page_config("Model Settings Information", layout="centered")
st.title("Model Settings Information")

info_md = """
---

## **Sampling / Decoding Parameters**

Control how tokens are chosen during generation.

* `temperature: float` → randomness of sampling.
* `top_p: float` → nucleus (probability mass) sampling.
* `top_k: int` → sample only from top-K tokens.
* `min_p: float` → minimum probability cutoff.
* `typical_p: float` → “typical” sampling (entropy-based).
* `tfs_z: float` → Tail Free Sampling.
* `mirostat_mode: int` → enable Mirostat adaptive sampling (0=off, 1=v1, 2=v2).
* `mirostat_tau: float` → target entropy for Mirostat.
* `mirostat_eta: float` → learning rate for Mirostat.

---

## **Repetition / Diversity Controls**

Discourage overuse of the same tokens.

* `presence_penalty: float` → discourages reuse of *any* seen token.
* `frequency_penalty: float` → discourages frequent tokens.
* `repeat_penalty: float` → general penalty multiplier for repeated tokens.
* `repeat_last_n: int` → how many tokens back to apply repetition penalty.

---

## **Output Length & Structure Controls**

Define the format, length, and boundaries of the output.

* `max_tokens: int` → maximum output length.
* `stop: list[str] | None` → stop sequences.
* `response_format` → constrain output structure (e.g. JSON).

---

## **Request / Runtime Settings**

Affect how completions are delivered.

* `n: int` → number of completions to generate.
* `stream: bool` → return tokens incrementally. *(Not yet implemented)*
* `seed: int | None` → RNG seed for reproducibility.

---
"""

st.markdown(info_md)
