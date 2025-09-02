import json
from fastapi import APIRouter, HTTPException
from backend.schemas.chat import LLMMessage, LLMRequest
from backend.schemas.structured import Recipe, Event
from backend.external.llm_client import llm_generate_content

router = APIRouter(prefix="/structured", tags=["structured"])

# Registry of structured tasks: map response_type -> (Pydantic model, task prompt).
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
async def get_structured_response(req: LLMRequest) -> list[object] | dict[str, object]:
    """Run a structured LLM task and return validated objects or an error."""
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

    responses: list[object] = []
    try:
        texts = data["choices"]
        for text in texts:
            try:
                parsed = json.loads(text["message"]["content"])
                obj = model_cls.model_validate(parsed)
                responses.append(obj)
            except Exception as e:
                responses.append(
                    {
                        "error": f"Invalid structured JSON: {str(e)}. See Tips for help",
                        "raw_output": text,
                    }
                )

    except Exception as e:
        return {
            "error": (
                "Invalid model response. Response does not contain 'choices': "
                f"{str(e)}"
            ),
            "raw_output": data,
        }
    else:
        return responses
