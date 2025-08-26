# SmolChat

SmolChat is a lightweight chat interface powered by [FastAPI](https://fastapi.tiangolo.com/), [Streamlit](https://streamlit.io/), and [Docker Model Runner](https://github.com/docker-model-runner).  

It provides a simple way to interact with small open-source LLMs like **SmolLM2**, exposing an OpenAI-compatible `/chat/completions` API and a Streamlit web UI. The app
allows you to adjust all of the input parameters given to the model and shows how to obtain structured JSON output from the model.

---

## Features
- **FastAPI backend**  
  - `/chat` endpoint accepts OpenAI-style chat messages.  
  - `/structured` endpoint gets structured output from the model.
  - Health check at `/healthz`.  
  - Forwards requests to Docker Model Runner.

- **Streamlit frontend**  
  - Simple chat UI at `http://localhost:8501`.  
  - Supports system / user / assistant roles.  
  - Displays model responses and usage stats.

- **Local deployment**
  - Accesses the model from docker model runner through TCP

- **Dockerized deployment**  
  - Separate backend (`api`) and frontend (`ui`) containers.  
  - Hot-reload support in development via mounted volumes.

---

## Quickstart

### Local
Run each service individually:
```bash
# Docker containers
docker compose up --build
```
```bash
# FastAPI
uvicorn backend.main:app
# Streamlit
streamlit run frontend/app.py
```

### Docker
```bash
# build and run all services
docker compose up --build
```

- Backend: http://localhost:8000  
- Frontend: http://localhost:8501  

---

## Configuration

Environment variables:
- `MODEL_ID` → model name (default: `smollm2`)  
- `DMR_BASE_URL` → model API base (default: `http://model-runner:3000/v1`)  
- `DMR_API_KEY` → API key (use `dmr` for Docker Model Runner)  
- `API_BASE_URL` → backend URL for Streamlit UI (default: `http://api:8000`)  

---

## Roadmap

### Phase 1 – Core Chat  
- [x] Implement OpenAI-compatible `/chat/completions` endpoint.  
- [x] Provide Streamlit-based chat UI.  
- [x] Dockerize backend and frontend with `docker compose`.

### Phase 2 – Structured Output and Data Validation 
- [x] Add support for structured output from the model.
- [x] Validate data sent from the from the frontend using Pydantic

### Phase 3 – Tool Use Integration  
- [ ] Add support for **function calling** (OpenAI-style `functions` and `tool_calls`) in backend schemas.  
- [ ] Define a standard tool registry (e.g., weather lookup, calculator, file search).  
- [ ] Implement dynamic dispatch: model chooses tool → backend executes tool → response is returned to model.  
- [ ] Extend Streamlit UI to visualize tool usage steps.
