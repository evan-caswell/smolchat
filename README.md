# SmolChat

SmolChat is a lightweight chat interface powered by [FastAPI](https://fastapi.tiangolo.com/), [Streamlit](https://streamlit.io/), and [Docker Model Runner (DMR)](https://github.com/docker-model-runner).  

It provides a simple way to interact with small open-source LLMs like **SmolLM2**, exposing an OpenAI-compatible `/chat` API and a Streamlit web UI. The app
allows you to adjust all of the input parameters given to the model and shows how to obtain structured JSON output from the model.

the purpose of this project is to explore the capabilities of "small" LLMs that can be comfortably run on average consumer hardware.

---

## Features
- **FastAPI backend**  
  - `/chat` endpoint accepts OpenAI-style chat messages.  
  - `/structured` endpoint gets structured output from the model.
  - Health check at `/healthz`.  
  - Forwards requests to DMR.

- **Streamlit frontend**  
  - Simple chat UI at `http://localhost:8501`.  
  - Supports system / user / assistant roles.  
  - Displays model responses and usage stats.

- **Local deployment**
  - Accesses the model from DMR through TCP

- **Dockerized deployment**  
  - Separate backend (`api`) and frontend (`ui`) containers built with Docker Compose.

---

## Quickstart

Ensure Docker Desktop is running, DMR is enabled, and host-side TCP support is enabled:

- Settings->Beta Features->Enable Docker Model Runner

If not developing in a container:

- Enable host-side TCP support with port `12434`
- Add the API address to CORS Allowed Origins (`http://localhost:8000`)

Pull the local model that will be used from Docker Hub.
This project has been primarily tested with SmolLM2-360M.

### Local
Run each service individually:
```bash
# FastAPI
uvicorn backend.main:app
```
```bash
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

Local environment variables:
- `MODEL_ID` → model name (default: `ai/smollm2:latest`)  
- `DMR_BASE_URL` → model API base (default: `http://localhost:12434/engines/llama.cpp/v1`)  
- `DMR_API_KEY` → API key (use `dmr` for Docker Model Runner)  
- `API_BASE_URL` → backend URL for FastAPI (default: `http://localhost:8000`)

Docker environment variables:
- `MODEL_ID` → model name (default: `ai/smollm2:latest`)  
- `DMR_BASE_URL` → model API base (default: `http://model-runner.docker.internal/engines/v1`)  
- `DMR_API_KEY` → API key (use `dmr` for Docker Model Runner)  
- `API_BASE_URL` → backend URL for FastAPI (default: `http://api:8000`)
---

## Roadmap

### Phase 1 – Core Chat  
- [x] Implement OpenAI-compatible `/chat` endpoint.  
- [x] Provide Streamlit-based chat UI.  
- [x] Dockerize backend and frontend with `docker compose`.

### Phase 2 – Structured Output and Data Validation 
- [x] Add support for structured output from the model.
- [x] Validate data sent from the from the frontend using Pydantic

### Phase 3 - Unit Tests
- [ ] Add unit tests (pytest)

### Phase 4 – Tool Use Integration  
- [ ] Add support for **function calling** (OpenAI-style `functions` and `tool_calls`) in backend schemas.  
- [ ] Define a standard tool registry (e.g., weather lookup, calculator, file search).  
- [ ] Implement dynamic dispatch: model chooses tool → backend executes tool → response is returned to model.  
- [ ] Extend Streamlit UI to visualize tool usage steps.

### Phase 5 - RAG
- [ ] Implement RAG (local file QA)

### Phase 6 - UI
- [ ] Replace Streamlit frontend with React
