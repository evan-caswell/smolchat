from typing import Literal
from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    temperature: float | None = 0.2
    max_tokens: int | None = 512


class ChatResponse(BaseModel):
    answer: str
    model: str
    usage: dict | None = None
    raw: dict | None = None
