from fastapi.testclient import TestClient


def test_healthz(client: TestClient) -> None:
    res = client.get("/healthz")
    assert res.status_code == 200
    data = res.json()
    assert data["ok"] is True
    assert isinstance(data["model"], str)

