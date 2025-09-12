import httpx
import asyncio
import json
from typing import Any, AsyncGenerator
from backend.schemas.chat import LLMRequest
from backend.settings import settings

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {settings.DMR_API_KEY}",
}


async def llm_generate_content(req: LLMRequest) -> dict[str, Any]:
    """Call the upstream chat-completions API and return its JSON response."""
    payload = {
        "model": settings.MODEL_ID,
        # Convert Pydantic message objects to plain dicts for JSON serialization.
        "messages": [m.model_dump() for m in req.messages],
        "seed": req.seed,
        "temperature": req.temperature,
        "max_tokens": req.max_tokens,
        "top_p": req.top_p,
        "presence_penalty": req.presence_penalty,
        "frequency_penalty": req.frequency_penalty,
        "stop": req.stop,  # list[str] or None
        "n": req.n,
        "stream": req.stream,
        "top_k": req.top_k,
        "min_p": req.min_p,
        "typical_p": req.typical_p,
        "tfs_z": req.tfs_z,
        "repeat_penalty": req.repeat_penalty,
        "repeat_last_n": req.repeat_last_n,
        "mirostat_mode": req.mirostat_mode,
        "mirostat_tau": req.mirostat_tau,
        "mirostat_eta": req.mirostat_eta,
    }

    # Request structured (schema-constrained) JSON when a schema is provided.
    # Uses the OpenAI "response_format": {"type": "json_schema", ...} contract.
    if req.response_schema is not None:
        payload["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": req.response_type,
                "schema": req.response_schema,
                "strict": True,
            },
        }

    url = f"{settings.DMR_BASE_URL}/chat/completions"

    # Docker Model Runner chat completions does not accept n > 1.
    # Normalize to n=1 and, if multiple results are desired, issue that many
    # parallel single-result calls and merge responses.
    # Normalize to n=1; if caller requested n>1, fan out parallel calls and merge.
    target_n = max(1, int(payload.get("n") or 1))
    payload_single = {**payload, "n": 1}

    async with httpx.AsyncClient(timeout=60.0) as client:
        if target_n == 1:
            r = await client.post(url, headers=HEADERS, json=payload_single)
            r.raise_for_status()
            return r.json()

        async def one_call():
            resp = await client.post(url, headers=HEADERS, json=payload_single)
            resp.raise_for_status()
            return resp.json()

        responses = await asyncio.gather(*[one_call() for _ in range(target_n)])

        # Base the combined response on the first, then merge choices and (if present) usage.
        base = responses[0]
        combined_choices = []
        for resp in responses:
            combined_choices.extend(resp.get("choices", []))
        base["choices"] = combined_choices

        # Best-effort usage aggregation if available.
        if all("usage" in r for r in responses):
            usage_keys = set().union(
                *[
                    r["usage"].keys()
                    for r in responses
                    if isinstance(r.get("usage"), dict)
                ]
            )
            # Treat all usage values as floats to avoid type ambiguity.
            agg: dict[str, float] = {k: 0.0 for k in usage_keys}
            for r in responses:
                for k, v in (r.get("usage") or {}).items():
                    if isinstance(v, (int, float)):
                        agg[k] = agg.get(k, 0.0) + float(v)
            base["usage"] = agg

        return base


async def llm_generate_content_stream(req: LLMRequest) -> AsyncGenerator[bytes, None]:
    """Stream partial response chunks from the upstream chat-completions API."""
    payload = {
        "model": settings.MODEL_ID,
        "messages": [m.model_dump() for m in req.messages],
        "seed": req.seed,
        "temperature": req.temperature,
        "max_tokens": req.max_tokens,
        "top_p": req.top_p,
        "presence_penalty": req.presence_penalty,
        "frequency_penalty": req.frequency_penalty,
        "stop": req.stop,  # list[str] or None
        "n": 1,
        "stream": True,
        "top_k": req.top_k,
        "min_p": req.min_p,
        "typical_p": req.typical_p,
        "tfs_z": req.tfs_z,
        "repeat_penalty": req.repeat_penalty,
        "repeat_last_n": req.repeat_last_n,
        "mirostat_mode": req.mirostat_mode,
        "mirostat_tau": req.mirostat_tau,
        "mirostat_eta": req.mirostat_eta,
    }

    url = f"{settings.DMR_BASE_URL}/chat/completions"
    # Open streaming POST to DMR and iterate SSE-style lines prefixed with "data:".
    async with httpx.AsyncClient(timeout=None) as client:
        async with client.stream("POST", url, headers=HEADERS, json=payload) as r:
            r.raise_for_status()
            async for line in r.aiter_lines():
                # Server-sent event framing: lines start with "data:"; [DONE] marks end.
                if not line or not line.startswith("data:"):
                    continue
                data = line[5:].strip()  # strip "data:"
                if data == "[DONE]":
                    break
                try:
                    obj = json.loads(data)
                    delta = (obj.get("choices") or [{}])[0].get("delta") or {}
                    piece = delta.get("content")
                    if piece:
                        yield piece.encode("utf-8")
                except Exception:
                    continue
