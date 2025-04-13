from fastapi.testclient import TestClient
from app.api.server import app


client = TestClient(app)


def test_status():
    response = client.get("/status")
    assert response.status_code == 200


def test_scan_wallet():
    response = client.post("/scan", json={"wallet": "abc"})
    assert response.status_code == 200
