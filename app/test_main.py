from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_availability():
    response = client.get("/?start_date=2024-01-01&end_date=2024-01-10")
    assert response.status_code == 200
