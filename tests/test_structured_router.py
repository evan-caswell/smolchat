from typing import Any
import json
import pytest
from fastapi.testclient import TestClient


def test_structured_recipe_success(monkeypatch: pytest.MonkeyPatch, client: TestClient) -> None:
    import backend.routers.structured as structured_router

    recipe_obj = {"recipe_name": "Test", "ingredients": ["a", "b"]}
    payload_json = json.dumps(recipe_obj)

    async def fake_generate(req: Any) -> dict[str, Any]:  # noqa: ANN401 (test helper)
        return {"choices": [{"message": {"content": payload_json}}]}

    monkeypatch.setattr(structured_router, "llm_generate_content", fake_generate)

    req = {
        "messages": [{"role": "user", "content": "Give recipe"}],
        "response_type": "recipe",
    }
    res = client.post("/structured", json=req)
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert data[0]["recipe_name"] == "Test"
    assert data[0]["ingredients"] == ["a", "b"]


def test_structured_event_invalid_json(monkeypatch: pytest.MonkeyPatch, client: TestClient) -> None:
    import backend.routers.structured as structured_router

    # Invalid JSON will be caught and returned as an error entry
    async def fake_generate(req: Any) -> dict[str, Any]:  # noqa: ANN401 (test helper)
        return {"choices": [{"message": {"content": "{not json}"}}]}

    monkeypatch.setattr(structured_router, "llm_generate_content", fake_generate)

    req = {
        "messages": [{"role": "user", "content": "Extract event"}],
        "response_type": "event",
    }
    res = client.post("/structured", json=req)
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert "error" in data[0]
    assert "raw_output" in data[0]


def test_structured_unknown_type(client: TestClient) -> None:
    req = {
        "messages": [{"role": "user", "content": "Hi"}],
        "response_type": "unknown",
    }
    res = client.post("/structured", json=req)
    assert res.status_code == 400
    assert res.json()["detail"] == "Unknown response_type"
