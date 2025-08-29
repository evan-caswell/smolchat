import json
from fastapi import APIRouter, HTTPException
from backend.schemas.chat import LLMMessage, LLMRequest
from backend.schemas.structured import Recipe, Event
from backend.external.llm_client import llm_generate_content

router = APIRouter(prefix="/structured", tags=["structured"])

# Map a client-supplied response_type -> (Pydantic model to validate against, task prompt to guide the LLM).
RESPONSE_TYPES = {
    "recipe": (Recipe, "You should give the requested recipe and ingredients."),
    "event": (
        Event,
        "You should extract the event name, date, and the names of the people involved.",
    ),
}

SYSTEM_PROMPT = """
You are a JSON generator. Respond with VALID JSON ONLY.
Do NOT include backticks, comments, HTML tags, markdown, or any extra text.
"""


@router.post("")
async def get_structured_response(req: LLMRequest):
    """
    Run a structured LLM task and return a Pydantic-validated object.

    Validates `req.response_type` against `RESPONSE_TYPES`, builds a system message
    from `SYSTEM_PROMPT` plus the task prompt, injects the target model's JSON Schema
    via `response_format`, calls the upstream chat completion API, then parses the
    first choice's message content as JSON and validates it with the selected
    Pydantic model.
    """
    if not req.response_type or req.response_type not in RESPONSE_TYPES:
        raise HTTPException(status_code=400, detail="Unknown response_type")

    model_cls, task_prompt = RESPONSE_TYPES[req.response_type]
    schema = model_cls.model_json_schema()

    system_message = LLMMessage(
        role="system", content=f"{SYSTEM_PROMPT}\n{task_prompt}"
    )
    all_messages = [system_message] + req.messages

    clean = req.model_copy(update={"messages": all_messages, "response_schema": schema})
    data = await llm_generate_content(clean)

    try:
        text = data["choices"][0]["message"]["content"]
        parsed = json.loads(text)
        obj = model_cls.model_validate(parsed)  # Validate against Pydantic model
        return obj.model_dump()
    except Exception as e:
        return {
            "error": f"Invalid structured JSON: {str(e)}",
            "raw_output": text,  # pyright: ignore[reportPossiblyUnboundVariable]
        }
