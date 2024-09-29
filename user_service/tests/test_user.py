import pytest
from fastapi.testclient import TestClient

from user.db import get_session_override, get_session
from user.main import app

app.dependency_overrides[get_session] = get_session_override

client = TestClient(app)


@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client


def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "User App running :-}"}


def test_user_page(test_client):
    response = test_client.get("/user/")
    assert response.status_code == 200
    assert response.json() == {"Message": "User Page running :-}"}


def test_register_user(test_client):
    data = {
        "username": "testuser5",
        "email": "newtestuser@example.com",
        "password": "testpassword3"
    }
    response = test_client.post("/user/register", json=data)
    assert response.status_code == 200
    assert response.json() == {"message": "New User Created Successfully"}


def test_login(test_client):
    data = {
        "username": "testuser5",
        "password": "testpassword3"
    }
    response = test_client.post("/login", data=data)
    assert response.status_code == 200
    json_response = response.json()
    assert "access_token" in json_response
    assert "refresh_token" in json_response
    assert json_response["token_type"] == "bearer"


def test_refresh_token(test_client):
    # First, login to get the refresh token
    login_data = {
        "username": "testuser5",
        "password": "testpassword3"
    }
    login_response = test_client.post("/login", data=login_data)
    assert login_response.status_code == 200
    refresh_token = login_response.json()["refresh_token"]

    # Use the refresh token to get a new access token
    refresh_data = {
        "old_refresh_token": refresh_token
    }
    refresh_response = test_client.post("/login/refresh", params=refresh_data)
    assert refresh_response.status_code == 200
    json_response = refresh_response.json()
    assert "access_token" in json_response
    assert "refresh_token" in json_response
    assert json_response["token_type"] == "bearer"


def test_user_profile(test_client):
    # First, login to get the access token
    login_data = {
        "username": "testuser5",
        "password": "testpassword3"
    }
    login_response = test_client.post("/login", data=login_data)
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    # Use the access token to get the user profile
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    profile_response = test_client.get("/user/me", headers=headers)
    assert profile_response.status_code == 200
    json_response = profile_response.json()
    assert json_response["username"] == "testuser5"
