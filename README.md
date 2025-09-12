# SmolChat

SmolChat is a lightweight chat interface powered by FastAPI (backend), Streamlit (frontend), and Docker Model Runner (DMR). It lets you chat with small open‑source LLMs (e.g., SmolLM2), tune generation parameters, and request structured JSON output.

The goal is to explore what “small” LLMs can do locally on typical hardware.

---

## Features
- FastAPI backend:
  - `/chat` (OpenAI‑style) and `/structured` endpoints
  - `/healthz` health check
  - Proxies to Docker Model Runner
- Streamlit frontend:
  - Chat UI at `http://localhost:8501`
  - System/user/assistant roles and usage stats
- Dockerized dev & run:
  - Separate `api` and `ui` services with Docker Compose
  - Uses Compose “models” to run the LLM and inject its endpoint URL

---

## What changed (Docker, Compose, env)

The stack now centralizes the model identifier and relies on Compose to inject the model endpoint URL.

- Single source of truth for the model id:
  - Set `MODEL_ID` once in `.env` (for Compose interpolation) and it’s used in `compose.yaml`, backend, and frontend.
- Compose models integration:
  - `compose.yaml` defines a `models.llm` entry with `model: ${MODEL_ID}`.
  - Under each service, `models.llm.endpoint_var: DMR_BASE_URL` makes Compose inject `DMR_BASE_URL` with the correct URL to the model.
- Container env files:
  - `.env.docker` is used for container env defaults (backend URL, API key, etc.).

Key snippet (`compose.yaml`):

```
services:
  api:
    env_file: .env.docker
    environment:
      - MODEL_ID=${MODEL_ID}
    models:
      llm:
        endpoint_var: DMR_BASE_URL

  ui:
    env_file: .env.docker
    environment:
      - MODEL_ID=${MODEL_ID}

models:
  llm:
    model: ${MODEL_ID}
    context_size: 8192
```

With this configuration:
- Compose injects `DMR_BASE_URL` into the `api` service environment (and you can add the same binding to `ui` if needed).
- Both services receive `MODEL_ID` explicitly from `${MODEL_ID}`.

---

## Quickstart

Prerequisites
- Docker Desktop with “Docker Model Runner” enabled

Set your model once in `.env` (project root):

```
MODEL_ID=ai/smollm2:latest
DMR_API_KEY=dmr-no-key-required
DMR_BASE_URL=http://localhost:12434/engines/llama.cpp/v1   # for local (non-Docker) runs
API_BASE_URL=http://localhost:8000                         # for local frontend → backend
```

For Docker runs, containers load defaults from `.env.docker`:

```
DMR_API_KEY=dmr-no-key-required
API_BASE_URL=http://api:8000
MODEL_ID=ai/smollm2:latest
# DMR_BASE_URL is injected by Compose models as `DMR_BASE_URL`
```

Run with Docker
```
docker compose up --build
```

URLs
- Backend (FastAPI): `http://localhost:8000`
- Frontend (Streamlit): `http://localhost:8501`

Run locally without Docker (requires a DMR endpoint running on the host)
```
# Backend
uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Frontend
streamlit run frontend/app.py
```

Ensure `.env` has a reachable `DMR_BASE_URL` for local runs (for Docker Model Runner TCP, the default is `http://localhost:12434/engines/llama.cpp/v1`).

---

## Configuration reference

Environment expected by the app:
- `MODEL_ID`: Model identifier, e.g., `ai/smollm2:latest`
- `DMR_BASE_URL`: Base URL to the model’s OpenAI‑compatible API
- `DMR_API_KEY`: API key (for DMR, can be a placeholder like `dmr-no-key-required`)
- `API_BASE_URL`: Backend URL the frontend calls

Compose models auto‑injection:
- When you bind a model under a service with `models:`, Compose creates env vars.
- In this project, `endpoint_var: DMR_BASE_URL` ensures the container gets `DMR_BASE_URL` automatically.

Switching models (one place)
- Change `MODEL_ID` in `.env`. That updates the Compose model and the value passed into services.
- Recreate the stack:
```
docker compose up -d --build
```

---

## Roadmap

Phase 1 — Core Chat
- [x] OpenAI‑compatible `/chat`
- [x] Streamlit UI
- [x] Dockerized backend and frontend

Phase 2 — Structured Output and Validation
- [x] Structured output endpoint
- [x] Pydantic validation

Phase 3 — Unit Tests
- [x] Tests (pytest)

Phase 4 — Tool Use Integration
- [ ] Function calling (`functions`, `tool_calls`)
- [ ] Tool registry and dispatch
- [ ] UI visualization of tool steps

Phase 5 — RAG
- [ ] Local file QA

Phase 6 — UI
- [ ] Replace Streamlit with React

