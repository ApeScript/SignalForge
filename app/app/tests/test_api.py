from fastapi.testclient import TestClient
from app.api.server import app

# Initialize FastAPI test client
client = TestClient(app)


def test_status():
    """
    Test the /status endpoint.

    Verifies that the API is up and returns a 200 OK status.
    """
    response = client.get("/status")
    assert response.status_code == 200, "Expected 200 OK from /status endpoint"
    assert response.json().get("status") == "SignalForge API is running."


def test_scan_wallet():
    """
    Test the /scan endpoint.

    Sends a dummy wallet address and checks for valid response.
    This does not require the wallet to be real — only ensures API responds.
    """
    test_wallet = "abc"
    response = client.post("/scan", json={"wallet": test_wallet})
    assert response.status_code == 200, "Expected 200 OK from /scan endpoint"

    # Optional sanity checks on structure
    json_data = response.json()
    assert "wallet" in json_data, "Missing 'wallet' in response"
    assert "tokens_held" in json_data, "Missing 'tokens_held' in response"
    assert "activity_type" in json_data, "Missing 'activity_type' in response"
