from typing import Any, AsyncGenerator
import pytest
from fastapi.testclient import TestClient


def test_chat_single_answer(monkeypatch: pytest.MonkeyPatch, client: TestClient) -> None:
    import backend.routers.chat as chat_router

    async def fake_generate(req: Any) -> dict[str, Any]:  # noqa: ANN401 (test helper)
        return {"choices": [{"message": {"content": "hello"}}]}

    monkeypatch.setattr(chat_router, "llm_generate_content", fake_generate)

    payload = {"messages": [{"role": "user", "content": "Hi"}]}
    res = client.post("/chat", json=payload)
    assert res.status_code == 200
    assert res.json() == "hello"


def test_chat_multiple_answers(monkeypatch: pytest.MonkeyPatch, client: TestClient) -> None:
    import backend.routers.chat as chat_router

    async def fake_generate(req: Any) -> dict[str, Any]:  # noqa: ANN401 (test helper)
        return {
            "choices": [
                {"message": {"content": "a"}},
                {"message": {"content": "b"}},
            ]
        }

    monkeypatch.setattr(chat_router, "llm_generate_content", fake_generate)

    payload = {"messages": [{"role": "user", "content": "Hi"}], "n": 2}
    res = client.post("/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["answers"] == ["a", "b"]
    assert "raw" in data


def test_chat_stream(monkeypatch: pytest.MonkeyPatch, client: TestClient) -> None:
    import backend.routers.chat as chat_router

    async def fake_stream(req: Any) -> AsyncGenerator[bytes, None]:  # noqa: ANN401
        yield b"Hello"
        yield b" "
        yield b"world"

    monkeypatch.setattr(chat_router, "llm_generate_content_stream", fake_stream)

    payload = {"messages": [{"role": "user", "content": "Hi"}], "stream": True}
    with client.stream("POST", "/chat/stream", json=payload) as res:
        assert res.status_code == 200
        text = "".join(res.iter_text())
        assert text == "Hello world"
