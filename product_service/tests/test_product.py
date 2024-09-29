import os
import pytest
from fastapi.testclient import TestClient

from product.db import get_session_override, get_session
from product.main import app
from schemas.model import Product, ProductCreate, ProductUpdate

app.dependency_overrides[get_session] = get_session_override

client = TestClient(app)


@pytest.fixture
def test_client():
    with TestClient(app) as client:
        yield client


def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Product App running :-}"}


def test_notification_page(test_client):
    response = test_client.get("/product/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Product page running :-}"}


def test_create_upload_file(test_client):
    file_path = "images/test_image.jpg"
    with open(file_path, "wb") as f:
        f.write(os.urandom(1024))  # Create a dummy file

    with open(file_path, "rb") as f:
        response = test_client.post(
            "product/upload/", files={"file": ("test_image.jpg", f, "image/jpeg")})
    assert response.status_code == 200
    assert response.json() == {"filename": "test_image.jpg"}
    os.remove(file_path)


def test_read_file(test_client):
    file_path = "./images/test_image.jpg"
    with open(file_path, "wb") as f:
        f.write(os.urandom(1024))  # Create a dummy file

    response = test_client.get("product/show/test_image.jpg")
    assert response.status_code == 200
    os.remove(file_path)


def test_add_product(test_client):
    product_data = {
        "name": "testproduct",
        "description": "test description",
        "category": "test category",
        "cost_price": 10.0,
        "sale_price": 20.0,
        "discount": 0.1
    }
    response = test_client.post("product/add_product", json=product_data)
    print("data inserted")
    assert response.status_code == 200
    assert response.json()["name"] == "testproduct"


def test_all_products(test_client):
    response = test_client.get("product/product_list")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_get_product_by_name(test_client):
    product_data = {
        "name": "testproduct_name",
        "description": "test description",
        "category": "test category",
        "cost_price": 110.0,
        "sale_price": 2020.0,
        "discount": 20.1
    }
    response = test_client.post("/product/add_product", json=product_data)
    product_name = response.json()["name"]
    assert response.status_code == 200

    response2 = test_client.get(f"product/{product_name}")
    assert response2.status_code == 200
    assert response2.json()["name"] == "testproduct_name"


def test_get_product_by_name(test_client):
    response2 = test_client.get(f"product/testproduct")
    assert response2.status_code == 200
    assert response2.json()["name"] == "testproduct"


def test_update_product(test_client):
    product = {  # change structure to correct for test from ProductCreate Class
        "name": "testproduct",
        "description": "test description",
        "category": "test category",
        "cost_price": 10.0,
        "sale_price": 20.0,
        "discount": 0.1
    }
    response = test_client.post("/product/add_product", json=product)
    assert response.status_code == 200

    update_data = {
        "description": "updated description"
    }
    response = test_client.patch("product/patch/testproduct", json=update_data)
    assert response.status_code == 200
    assert response.json()["description"] == "updated description"


def test_delete_product(test_client):
    product = {
        "name": "test2",
        "description": "test description",
        "category": "test category",
        "cost_price": 10.0,
        "sale_price": 20.0,
        "discount": 0.1
    }
    response = test_client.post("/product/add_product", json=product)
    assert response.status_code == 200

    response = test_client.delete("product/del/test2")
    assert response.status_code == 200
    assert response.json() == {"message": "Product deleted successfully"}
