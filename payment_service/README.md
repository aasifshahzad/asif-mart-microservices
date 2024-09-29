# Payment Service API

This FastAPI application provides APIs for managing payments. It integrates with Kafka for event streaming and supports operations for creating and retrieving payment records.

## Features

- **Create Payment**: Process a new payment and publish an event to Kafka.
- **View Payment Page**: Check if the payment service is running.
- **List All Payments**: Retrieve a list of all payments stored in the database.
- **Get Payment by ID**: Fetch a specific payment by its ID.
- **Card Number Validation**: Validate the card number that it must be a**6** digit number.
- **CVV Number Validation**: Validate that CVV is a **3** digit number.

## API Endpoints

### 1. Create Payment

- **POST** `/payment/pay-now/`
  - **Description**: Process a new payment and publish an event to Kafka.
  - **Body**:
    ```json
    {
      "card_num": "123456",
      "cvv": "123",
      "valid_thru_month": 12,
      "valid_thru_year": 2025,
      "total_price": 99.99
    }
    ```
  - **Response**:
    ```json
    {
      "card_num": "123456",
      "cvv": "123",
      "valid_thru_month": 12,
      "valid_thru_year": 2025,
      "total_price": 99.99,
      "status": "PENDING"
    }
    ```
  - **Error**:
    ```json
    {
      "detail": "Error while producing message to Kafka"
    }
    ```

### 2. View Payment Page

- **GET** `/payment/`
  - **Description**: Check if the payment service is running.
  - **Response**:
    ```json
    {
      "Message": "Payment Page running :-}"
    }
    ```

### 3. List All Payments

- **GET** `/payment/all/`
  - **Description**: Retrieve a list of all payments stored in the database.
  - **Response**: A list of payments.  
    Example response:
    ```json
    [
      {
        "payment_id": 1,
        "card_num": "1234567812345678",
        "cvv": "123",
        "valid_thru_month": 12,
        "valid_thru_year": 2025,
        "total_price": 99.99,
        "status": "PENDING"
      },
      {
        "payment_id": 2,
        "card_num": "8765432187654321",
        "cvv": "321",
        "valid_thru_month": 11,
        "valid_thru_year": 2024,
        "total_price": 49.99,
        "status": "COMPLETED"
      }
    ]
    ```

### 4. Get Payment by ID

- **GET** `/payment/{payment_id}`
  - **Description**: Fetch a specific payment by its ID.
  - **Response**:
    ```json
    {
      "payment_id": 1,
      "card_num": "1234567812345678",
      "cvv": "123",
      "valid_thru_month": 12,
      "valid_thru_year": 2025,
      "total_price": 99.99,
      "status": "PENDING"
    }
    ```
  - **Error**:
    ```json
    {
      "detail": "Payment not found"
    }
    ```

## Kafka Integration

- **Producer**: A Kafka producer is used to send payment events.
- **Topic**: The topic for payment events is specified in the environment variable `KAFKA_PAYMENT_TOPIC`.
- **Protobuf Serialization**: Payments are serialized using Protobuf format before being sent to Kafka.
