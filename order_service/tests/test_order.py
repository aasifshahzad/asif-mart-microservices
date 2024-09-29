import pytest
from fastapi.testclient import TestClient

from order.db import get_session_override, get_session
from order.main import app

app.dependency_overrides[get_session] = get_session_override

client = TestClient(app)


@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client


def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Order App running :-}"}


def test_order_page(test_client):
    response = test_client.get("/order/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Order page running :-}"}


def test_create_order(test_client):
    new_order_data = {
        "created_at": "2024-08-05T20:33:26.782027",
        "updated_at": "2024-08-05T15:33:51.038Z",
        "username": "testuser",
        "email": "testuser@example.com",
        "product_name": "test_product",
        "quantity": 10,
        "price": 100.0,
        "status": "pending"
    }
    response = test_client.post("/order/create-order/", json=new_order_data)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["product_name"] == new_order_data["product_name"]


def test_read_orders(test_client):
    response = test_client.get("/order/all/")
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)


def test_read_order(test_client):
    # First, create an order
    new_order_data = {
        "created_at": "2024-08-05T20:33:26.782027",
        "updated_at": "2024-08-05T15:33:51.038Z",
        "username": "testuser",
        "email": "testuser@example.com",
        "product_name": "test_product",
        "quantity": 10,
        "price": 100.0,
        "status": "pending"
    }
    response = test_client.post("/order/create-order/", json=new_order_data)
    assert response.status_code == 200
    created_order = response.json()

    # Then, read the created order
    order_id = created_order["id"]
    response = test_client.get(f"/order/{order_id}")
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["id"] == order_id


def test_read_order_items(test_client):
    response = test_client.get("/order/ordered-items/")
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    for item in response_data:
        assert "product_name" in item
        assert "quantity" in item
        assert "price" in item
        assert "total_price" in item
