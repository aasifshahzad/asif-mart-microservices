# Inventory Management API

This FastAPI application provides a set of REST APIs to manage inventory items. It supports basic CRUD operations (Create, Read, Update, Delete) on inventory, integrates with Kafka for event streaming, and communicates with a product service to validate products.

## Features

- **View Inventory Page**: A simple root endpoint to check the status of the inventory service.
- **Get Product Details**: Fetch detailed product information from an external product service.
- **Retrieve Inventory by Product Name**: Get the current stock details for a product by its name.
- **List All Inventory Items**: Fetch all inventory items.
- **Add New Inventory Item**: Add a new product to the inventory with stock level information and send an event to Kafka.
- **Update Existing Inventory Item**: Update the stock level or other fields for an existing inventory item.
- **Delete Inventory Item**: Remove an inventory item from the database.

## API Endpoints

### 1. Root Endpoint

- **GET** `/inventory/`
  - **Description**: Check if the inventory page is running.
  - **Response**:
    ```json
    {
      "Message": "Inventory Page running :-}"
    }
    ```

### 2. Get Inventory by Product Name

- **GET** `/inventory/get-stock/{product_name}`
  - **Description**: Fetch inventory details for a given product name.
  - **Response**: Returns the inventory information for the product.
  - **Error**:
    ```json
    {
      "detail": "Inventory item not found"
    }
    ```

### 3. List All Inventory Items

- **GET** `/inventory/all-inventory/`
  - **Description**: Get a list of all inventory items.
  - **Response**: A list of inventory items.  
    Example response:
    ```json
    [
      {
        "product_name": "Product 1",
        "stock_level": 10,
        "created_at": "2024-09-16T00:00:00Z",
        "updated_at": "2024-09-16T00:00:00Z"
      },
      {
        "product_name": "Product 2",
        "stock_level": 25,
        "created_at": "2024-09-15T00:00:00Z",
        "updated_at": "2024-09-15T00:00:00Z"
      }
    ]
    ```

### 4. Add New Inventory Item

- **POST** `/inventory/add-stock/`
  - **Description**: Add a new item to the inventory. It validates the product with the product service before adding and sends a Kafka message.
  - **Body**:
    ```json
    {
      "product_name": "Product 1",
      "stock_level": 100
    }
    ```
  - **Response**:
    ```json
    {
      "product_name": "Product 1",
      "stock_level": 100,
      "created_at": 1694778246,
      "updated_at": 1694778246
    }
    ```
  - **Error**:
    ```json
    {
      "detail": "Invalid product Name"
    }
    ```

### 5. Update Existing Inventory Item

- **PATCH** `/inventory/patch-stock/{product_name}`
  - **Description**: Update the stock or other fields of an inventory item for a given product name.
  - **Body**:
    ```json
    {
      "stock_level": 150
    }
    ```
  - **Response**:
    ```json
    {
      "product_name": "Product 1",
      "stock_level": 150,
      "created_at": 1694778246,
      "updated_at": 1694778246
    }
    ```
  - **Error**:
    ```json
    {
      "detail": "Inventory item not found"
    }
    ```

### 6. Delete Inventory Item

- **DELETE** `/inventory/del-stock/{product_name}`
  - **Description**: Delete an inventory item for a given product name.
  - **Response**:
    ```json
    {
      "message": "Inventory item deleted successfully"
    }
    ```
  - **Error**:
    ```json
    {
      "detail": "Inventory item not found"
    }
    ```

## Kafka Integration

- **Producer**: A Kafka producer is used to send events when a new inventory item is added.
- **Topic**: The topic for inventory events is specified in the environment variable `KAFKA_INVENTORY_TOPIC`.
- **Protobuf Serialization**: Messages sent to Kafka are serialized using Protobuf format.
