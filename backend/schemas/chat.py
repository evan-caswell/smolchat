from typing import Literal, Any
from pydantic import BaseModel, Field


class LLMMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str


class LLMRequest(BaseModel):
    messages: list[LLMMessage]
    response_type: str | None = None
    response_schema: dict[str, Any] | None = None
    seed: int | None = None
    temperature: float = Field(0.8, ge=0.0, le=2.0)
    max_tokens: int = Field(512, ge=32, le=2048)
    top_p: float = Field(0.95, ge=0.0, le=1.0)
    presence_penalty: float = Field(0.0, ge=-2.0, le=2.0)
    frequency_penalty: float = Field(0.0, ge=-2.0, le=2.0)
    stop: list[str] | None = None
    n: int = Field(1, ge=1, le=10)
    stream: bool = False
    top_k: int = Field(40, ge=0)
    min_p: float = Field(0.05, ge=0.0, le=1.0)
    typical_p: float = Field(1.0, ge=0.0, le=1.0)
    tfs_z: float = Field(1.0, ge=0.0, le=1.0)
    repeat_penalty: float = Field(1.0, ge=0.0)
    repeat_last_n: int = Field(64, ge=-1)
    mirostat_mode: int = Field(0, ge=0, le=2)
    mirostat_tau: float = Field(5.0, ge=0.0)
    mirostat_eta: float = Field(0.1, ge=0.0)


class ChatResponse(BaseModel):
    answer: str
    model: str
    usage: dict | None = None
    raw: dict | None = None
