from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from backend.schemas.chat import LLMRequest
from backend.external.llm_client import (
    llm_generate_content,
    llm_generate_content_stream,
)

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("")
async def chat(req: LLMRequest) -> str | dict:
    """Proxy a chat request to the configured LLM and return results."""
    # Ensure structured-output fields aren't forwarded
    clean = req.model_copy(update={"response_type": None, "response_schema": None})
    data = await llm_generate_content(clean)

    try:
        choices = data["choices"]
    except Exception:
        raise HTTPException(status_code=502, detail="LLM response missing choices")

    # Single choice returns a string; multiple choices return answers + raw upstream data.
    texts = [c["message"]["content"] for c in choices]
    return texts[0] if len(texts) == 1 else {"answers": texts, "raw": data}


@router.post("/stream")
async def chat_stream(req: LLMRequest) -> StreamingResponse:
    """Proxy a chat request to the configured LLM and stream the response."""
    # Ensure structured-output fields aren't forwarded
    clean = req.model_copy(update={"response_type": None, "response_schema": None})

    return StreamingResponse(
        llm_generate_content_stream(clean), media_type="text/plain"
    )
