from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from backend.schemas.chat import LLMRequest
from backend.external.llm_client import (
    llm_generate_content,
    llm_generate_content_stream,
)

router = APIRouter(prefix="/chat", tags=["chat"])


# Simple chat endpoint
@router.post("")
async def chat(req: LLMRequest):
    """
    Proxy a chat-completions request to the configured LLM and return the answer(s).

    Builds a payload from `LLMRequest`, strips any structured-output fields
    (`response_type`, `response_schema`), calls the upstream chat endpoint, and
    returns either a single string (when one choice is requested) or a JSON
    object with multiple answers and the raw upstream response.
    """
    # Ensure structured-output fields aren't forwarded
    clean = req.model_copy(update={"response_type": None, "response_schema": None})
    data = await llm_generate_content(clean)

    try:
        choices = data["choices"]
    except Exception:
        raise HTTPException(status_code=502, detail="LLM response missing choices")

    # If n>1, return list of answers; else a single string.
    texts = [c["message"]["content"] for c in choices]
    return texts[0] if len(texts) == 1 else {"answers": texts, "raw": data}


@router.post("/stream")
async def chat_stream(req: LLMRequest):
    """
    Proxy a chat-completions request to the configured LLM and return the answer(s)
    with streaming.

    Builds a payload from `LLMRequest`, strips any structured-output fields
    (`response_type`, `response_schema`), calls the upstream chat endpoint, and
    returns a streaming response.
    """
    # Ensure structured-output fields aren't forwarded
    clean = req.model_copy(update={"response_type": None, "response_schema": None})

    return StreamingResponse(
        llm_generate_content_stream(clean), media_type="text/plain"
    )
