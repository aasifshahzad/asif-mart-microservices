# Notification Service API

This FastAPI application provides APIs for managing and sending notifications. It integrates with Kafka for event streaming and supports basic operations for creating and retrieving notifications.

## Features

- **Create Notification**: Send a notification to a recipient and publish an event to Kafka.
- **View Notification Page**: Check if the notification service is running.
- **List All Notifications**: Retrieve a list of all notifications stored in the database.
- **Get Notification by ID**: Fetch a specific notification by its ID.

## API Endpoints

### 1. Create Notification

- **POST** `/notification/notify/`
  - **Description**: Send a notification to a recipient and publish an event to Kafka.
  - **Body**:
    ```json
    {
      "recipient_info": {
        "username": "user1",
        "address": "123 Main St",
        "contact": "1234567890",
        "email": "user1@example.com"
      },
      "notification": {
        "subject": "Payment Confirmation",
        "message": "Your payment has been confirmed."
      }
    }
    ```
  - **Response**:
    ```json
    {
      "recipient_info": {
        "username": "user1",
        "address": "123 Main St",
        "contact": "1234567890",
        "email": "user1@example.com"
      },
      "subject": "Payment Confirmation",
      "message": "Your payment has been confirmed."
    }
    ```
  - **Error**:
    ```json
    {
      "detail": "Error while producing message to Kafka"
    }
    ```

### 2. View Notification Page

- **GET** `/notification/`
  - **Description**: Check if the notification service is running.
  - **Response**:
    ```json
    {
      "Message": "Notification page running :-}"
    }
    ```

### 3. List All Notifications

- **GET** `/notification/all/`
  - **Description**: Retrieve a list of all notifications stored in the database.
  - **Response**: A list of notifications.  
    Example response:
    ```json
    [
      {
        "id": 1,
        "username": "user1",
        "address": "123 Main St",
        "contact": "1234567890",
        "email": "user1@example.com",
        "notification_type": "PROMOTIONAL",
        "event": "PAYMENT_CONFIRMATION",
        "subject": "Payment Confirmation",
        "message": "Your payment has been confirmed.",
        "notification_status": "SENT",
        "sent_at": 1694778246
      },
      {
        "id": 2,
        "username": "user2",
        "address": "456 Elm St",
        "contact": "0987654321",
        "email": "user2@example.com",
        "notification_type": "INFORMATIONAL",
        "event": "ACCOUNT_CREATION",
        "subject": "Account Created",
        "message": "Your account has been created successfully.",
        "notification_status": "SENT",
        "sent_at": 1694778246
      }
    ]
    ```

### 4. Get Notification by ID

- **GET** `/notification/{id}/`
  - **Description**: Fetch a specific notification by its ID.
  - **Response**:
    ```json
    {
      "id": 1,
      "username": "user1",
      "address": "123 Main St",
      "contact": "1234567890",
      "email": "user1@example.com",
      "notification_type": "PROMOTIONAL",
      "event": "PAYMENT_CONFIRMATION",
      "subject": "Payment Confirmation",
      "message": "Your payment has been confirmed.",
      "notification_status": "SENT",
      "sent_at": 1694778246
    }
    ```
  - **Error**:
    ```json
    {
      "detail": "Notification not found"
    }
    ```

## Kafka Integration

- **Producer**: A Kafka producer is used to send notification events.
- **Topic**: The topic for notification events is specified in the environment variable `KAFKA_NOTIFICATION_TOPIC`.
- **Protobuf Serialization**: Notifications are serialized using Protobuf format before being sent to Kafka.
