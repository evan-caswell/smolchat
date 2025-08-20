import os
import httpx
from fastapi.routing import APIRouter
from schemas.chat_schema import ChatResponse, ChatRequest

router = APIRouter(prefix="/chat")

MODEL_ID = os.getenv("MODEL_ID", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "dmr")


@router.get("/healthz")
async def healthz():
    return {"ok": True, "model": MODEL_ID}


# Simple chat endpoint
@router.post("/", response_model=ChatResponse)
async def chat(req: ChatRequest):
    body = {
        "model": MODEL_ID,
        "messages": [m.model_dump() for m in req.messages],
        "temperature": req.temperature,
        "max_tokens": req.max_tokens,
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    url = f"{OPENAI_BASE_URL}/chat/completions"

    async with httpx.AsyncClient(timeout=30.0) as client:
        r = await client.post(url, headers=headers, json=body)
        r.raise_for_status()
        data = r.json()

    choice = data["choices"][0]
    answer = choice["message"]["content"]

    return ChatResponse(
        answer=answer,
        model=data.get("model", MODEL_ID),
        usage=data.get("usage"),
        raw=data,
    )
