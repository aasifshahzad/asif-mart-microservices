# Product Service API

This FastAPI application provides APIs for managing products. It includes features for uploading and retrieving product images, managing product information, and integrating with Kafka for event streaming.

## Features

- **Upload Product Image**: Upload product images to the server.
- **Show Product Image**: Retrieve product images by filename.
- **List All Products**: Retrieve a list of all products.
- **Add Product**: Add a new product and publish an event to Kafka.
- **Get Product by Name**: Fetch a product by its name.
- **Update Product**: Update the details of an existing product.
- **Delete Product**: Delete a product by its name.

## API Endpoints

### 1. Upload Image

- **POST** `/product/upload/`
  - **Description**: Upload a product image to the server.
  - **Body**: Form-data with a file.
  - **Response**:
    ```json
    {
      "filename": "example.jpg"
    }
    ```

### 2. Show Image

- **GET** `/product/show/{file_name}`
  - **Description**: Retrieve a product image by filename.
  - **Response**: The image file.

### 3. List All Products

- **GET** `/product/product_list`
  - **Description**: Retrieve a list of all products.
  - **Response**: A list of products.  
    Example response:
    ```json
    [
      {
        "product_id": 1,
        "name": "Product A",
        "description": "Description of Product A",
        "category": "Category A",
        "cost_price": 10.0,
        "sale_price": 15.0,
        "discount": 5.0
      },
      {
        "product_id": 2,
        "name": "Product B",
        "description": "Description of Product B",
        "category": "Category B",
        "cost_price": 20.0,
        "sale_price": 25.0,
        "discount": 10.0
      }
    ]
    ```

### 4. Add Product

- **POST** `/product/add_product`
  - **Description**: Add a new product and publish an event to Kafka.
  - **Body**:
    ```json
    {
      "name": "Product C",
      "description": "Description of Product C",
      "category": "Category C",
      "cost_price": 30.0,
      "sale_price": 35.0,
      "discount": 15.0
    }
    ```
  - **Response**:
    ```json
    {
      "name": "Product C",
      "description": "Description of Product C",
      "category": "Category C",
      "cost_price": 30.0,
      "sale_price": 35.0,
      "discount": 15.0
    }
    ```
  - **Error**:
    ```json
    {
      "detail": "Error while producing message to Kafka"
    }
    ```

### 5. Get Product by Name

- **GET** `/product/{product_name}`
  - **Description**: Fetch a product by its name.
  - **Response**:
    ```json
    {
      "product_id": 1,
      "name": "Product C",
      "description": "Description of Product C",
      "category": "Category C",
      "cost_price": 30.0,
      "sale_price": 35.0,
      "discount": 15.0
    }
    ```
  - **Error**:
    ```json
    {
      "detail": "Product not found"
    }
    ```

### 6. Update Product

- **PATCH** `/product/patch/{product_name}`
  - **Description**: Update the details of an existing product.
  - **Body**:
    ```json
    {
      "description": "Updated description",
      "sale_price": 32.0
    }
    ```
  - **Response**:
    ```json
    {
      "product_id": 1,
      "name": "Product C",
      "description": "Updated description",
      "category": "Category C",
      "cost_price": 30.0,
      "sale_price": 32.0,
      "discount": 15.0
    }
    ```
  - **Error**:
    ```json
    {
      "detail": "Product not found"
    }
    ```

### 7. Delete Product

- **DELETE** `/product/del/{product_name}`
  - **Description**: Delete a product by its name.
  - **Response**:
    ```json
    {
      "message": "Product deleted successfully"
    }
    ```
  - **Error**:
    ```json
    {
      "detail": "Product not found"
    }
    ```

## Kafka Integration

- **Producer**: A Kafka producer is used to send product events.
- **Topic**: The topic for product events is specified in the environment variable `KAFKA_PRODUCT_TOPIC`.
- **Protobuf Serialization**: Products are serialized using Protobuf format before being sent to Kafka.
