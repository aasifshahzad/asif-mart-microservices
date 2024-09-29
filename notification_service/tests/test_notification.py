import pytest
from fastapi.testclient import TestClient

from notification.db import get_session_override, get_session
from notification.main import app

app.dependency_overrides[get_session] = get_session_override

client = TestClient(app)


@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client


def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Notification App running :-}"}


def test_notification_page(test_client):
    response = test_client.get("/notification/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Notification page running :-}"}


def test_create_notification(test_client):
    notification_data = {
        "recipient_info": {
            "username": "string",
            "contact": 0,
            "address": "string",
            "email": "string"
        },
        "notification": {
            "notification_type": "transactional",
            "event": "Order Confirmation",
            "subject": "Test Notification",
            "message": "This is a test notification",
            "notification_status": "pending",
            "sent_at": "2024-07-31T05:09:12.179Z"
        }
    }
    response = test_client.post(
        "/notification/notify/", json=notification_data)
    assert response.status_code == 200
    assert response.json()["subject"] == "Test Notification"


def test_read_notifications(test_client):
    response = test_client.get("/notification/all/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_read_notification(test_client):
    # First, create a notification to test
    notification_data = {
        "recipient_info": {
            "username": "string",
            "contact": 0,
            "address": "string",
            "email": "string"
        },
        "notification": {
            "notification_type": "transactional",
            "event": "Order Confirmation",
            "subject": "Test Notification",
            "message": "This is a test notification",
            "notification_status": "pending",
            "sent_at": "2024-07-31T05:09:12.179Z"
        }
    }
    create_response = test_client.post(
        "/notification/notify/", json=notification_data)
    notification_id = create_response.json()["id"]

    # Test reading the notification by ID
    response = test_client.get(f"/notification/{notification_id}/")
    assert response.status_code == 200
    assert response.json()["subject"] == "Test Notification"
