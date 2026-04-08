# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from src.api.main import app


@pytest.fixture(scope="module")
def client():
   
    with TestClient(app) as c:
        yield c


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_valid_prediction(client):
    response = client.post("/predict", json={
        "text": "win a free iPhone now click here"
    })
    assert response.status_code == 200
    assert "is_spam" in response.json()
    assert "confidence" in response.json()


def test_spam_detected(client):
    response = client.post("/predict", json={
        "text": "Congratulations you won a free prize click here now"
    })
    assert response.status_code == 200
    assert response.json()["is_spam"] is True


def test_ham_not_spam(client):
    response = client.post("/predict", json={
        "text": "Hi can we schedule a meeting for tomorrow afternoon"
    })
    assert response.status_code == 200
    assert response.json()["is_spam"] is False


def test_empty_text_rejected(client):
    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 422


def test_null_text_rejected(client):
    response = client.post("/predict", json={"text": None})
    assert response.status_code == 422


def test_missing_text_rejected(client):
    response = client.post("/predict", json={})
    assert response.status_code == 422
