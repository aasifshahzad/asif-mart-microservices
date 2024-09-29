import pytest
from fastapi.testclient import TestClient

from inventory.db import get_session_override, get_session
from inventory.main import app

app.dependency_overrides[get_session] = get_session_override

client = TestClient(app)


@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client


def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Inventory App running :-}"}


def test_inventory_page(test_client):
    response = test_client.get("/inventory/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Inventory Page running :-}"}

#  Test for adding the stock of product


def test_add_inventory_item(test_client):
    new_inventory_data = {
        "product_name": "test4",
        "stock_level": 70,
    }

    response = test_client.post(
        "/inventory/add-stock/", json=new_inventory_data)

    assert response.status_code == 200
    response_data = response.json()
    assert response_data["product_name"] == new_inventory_data["product_name"]
    assert response_data["stock_level"] == new_inventory_data["stock_level"]


# Test for listing all inventory items
def test_list_inventory(test_client):

    response = test_client.get("/inventory/all-inventory/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

# Test for getting inventory by product name


def test_get_inventory_by_product_name(test_client):
    # First, add a test inventory item
    new_inventory_data = {
        "product_name": "test7",  # this will look for new product which is not in inventory
        "stock_level": 70,
    }

    response = test_client.post(
        "/inventory/add-stock/", json=new_inventory_data)
    assert response.status_code == 200
    # update this according to upper
    response = test_client.get("/inventory/get-stock/test7")
    assert response.status_code == 200
    # update this according to upper
    assert response.json()["product_name"] == "test7"

# Test for updating an inventory item


def test_update_inventory_item(test_client):
    # First, add a test inventory item
    new_inventory_data = {
        "product_name": "test3",  # this will look for new product which is not in inventory
        "stock_level": 70,
    }

    response = test_client.post(
        "/inventory/add-stock/", json=new_inventory_data)
    assert response.status_code == 200
    response = test_client.patch("/inventory/patch-stock/test3", json={
        "stock_level": 99
    })
    assert response.status_code == 200
    assert response.json()["stock_level"] == 99

# Test for deleting an inventory item


def test_delete_inventory_item(test_client):
    # First, add a test inventory item
    test_client.post("/inventory/add-stock/", json={
        "product_name": "test8",
        "stock_level": 99
    })

    response = test_client.delete("/inventory/del-stock/test8")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Inventory item deleted successfully"}

    # Verify item is deleted
    response = test_client.get("/inventory/get-stock/test8")
    assert response.status_code == 404
