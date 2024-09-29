# Order Service API

This FastAPI application provides APIs for managing orders. It integrates with Kafka for event streaming and supports operations for creating, retrieving, and deleting orders.

## Features

- **Create Order**: Place a new order and publish an event to Kafka.
- **View Order Page**: Check if the order service is running.
- **List All Orders**: Retrieve a list of all orders stored in the database.
- **Get Order by ID**: Fetch a specific order by its ID.
- **List Ordered Items**: Retrieve a list of items with calculated total prices.
- **Delete Order**: Remove an order from the database.

## API Endpoints

### 1. Create Order

- **POST** `/order/create-order/`
  - **Description**: Place a new order and publish an event to Kafka.
  - **Body**:
    ```json
    {
      "username": "user1",
      "email": "user1@example.com",
      "product_name": "Product A",
      "quantity": 2,
      "price": 29.99
    }
    ```
  - **Response**:
    ```json
    {
      "username": "user1",
      "email": "user1@example.com",
      "product_name": "Product A",
      "quantity": 2,
      "price": 29.99,
      "status": "PENDING"
    }
    ```
  - **Error**:
    ```json
    {
      "detail": "Error while producing message to Kafka"
    }
    ```

### 2. View Order Page

- **GET** `/order/`
  - **Description**: Check if the order service is running.
  - **Response**:
    ```json
    {
      "Message": "Order page running :-}"
    }
    ```

### 3. List All Orders

- **GET** `/order/all/`
  - **Description**: Retrieve a list of all orders stored in the database.
  - **Response**: A list of orders.  
    Example response:
    ```json
    [
      {
        "order_id": 1,
        "username": "user1",
        "email": "user1@example.com",
        "product_name": "Product A",
        "quantity": 2,
        "price": 29.99,
        "status": "PENDING"
      },
      {
        "order_id": 2,
        "username": "user2",
        "email": "user2@example.com",
        "product_name": "Product B",
        "quantity": 1,
        "price": 49.99,
        "status": "PENDING"
      }
    ]
    ```

### 4. Get Order by ID

- **GET** `/order/{order_id}`
  - **Description**: Fetch a specific order by its ID.
  - **Response**:
    ```json
    {
      "order_id": 1,
      "username": "user1",
      "email": "user1@example.com",
      "product_name": "Product A",
      "quantity": 2,
      "price": 29.99,
      "status": "PENDING"
    }
    ```
  - **Error**:
    ```json
    {
      "detail": "Order not found"
    }
    ```

### 5. List Ordered Items

- **GET** `/order/ordered-items/`
  - **Description**: Retrieve a list of items with calculated total prices.
  - **Response**: A list of ordered items with total prices.  
    Example response:
    ```json
    [
      {
        "product_name": "Product A",
        "quantity": 2,
        "price": 29.99,
        "total_price": 59.98
      },
      {
        "product_name": "Product B",
        "quantity": 1,
        "price": 49.99,
        "total_price": 49.99
      }
    ]
    ```

### 6. Delete Order

- **DELETE** `/order/{order_id}`
  - **Description**: Remove an order from the database.
  - **Response**:
    ```json
    {
      "message": "Order deleted successfully"
    }
    ```
  - **Error**:
    ```json
    {
      "detail": "Order not found"
    }
    ```

## Kafka Integration

- **Producer**: A Kafka producer is used to send order events.
- **Topic**: The topic for order events is specified in the environment variable `KAFKA_ORDER_TOPIC`.
- **Protobuf Serialization**: Orders are serialized using Protobuf format before being sent to Kafka.
