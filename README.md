# SmolChat

SmolChat is a lightweight chat interface powered by [FastAPI](https://fastapi.tiangolo.com/), [Streamlit](https://streamlit.io/), and [Docker Model Runner](https://github.com/docker-model-runner).  
It provides a simple way to interact with small open-source LLMs like **SmolLM2**, exposing an OpenAI-compatible `/chat/completions` API and a Streamlit web UI.

---

## Features
- **FastAPI backend**  
  - `/chat/` endpoint accepts OpenAI-style chat messages.  
  - Health check at `/chat/healthz`.  
  - Forwards requests to Docker Model Runner.

- **Streamlit frontend**  
  - Simple chat UI at `http://localhost:8501`.  
  - Supports system / user / assistant roles.  
  - Displays model responses and usage stats.

- **Dockerized deployment**  
  - Separate backend (`api`) and frontend (`ui`) containers.  
  - Hot-reload support in development via mounted volumes.

---

## Quickstart

```bash
# build and run all services
docker compose up --build
```

- Backend: http://localhost:8000  
- Frontend: http://localhost:8501  

---

## Configuration

Environment variables:
- `MODEL_ID` → model name (default: `ai/smollm2:latest`)  
- `OPENAI_BASE_URL` → model API base (default: `http://model-runner.docker.internal/engines/v1`)  
- `OPENAI_API_KEY` → API key (use `dmr` for Docker Model Runner)  
- `API_BASE_URL` → backend URL for Streamlit UI (default: `http://api:8000`)  

---

## Roadmap

### Phase 1 – Core Chat  
- [x] Implement OpenAI-compatible `/chat/completions` endpoint.  
- [x] Provide Streamlit-based chat UI.  
- [x] Dockerize backend and frontend with `docker compose`.

### Phase 2 – Tool Use Integration  
- [ ] Add support for **function calling** (OpenAI-style `functions` and `tool_calls`) in backend schemas.  
- [ ] Define a standard tool registry (e.g., weather lookup, calculator, file search).  
- [ ] Implement dynamic dispatch: model chooses tool → backend executes tool → response is returned to model.  
- [ ] Extend Streamlit UI to visualize tool usage steps.
