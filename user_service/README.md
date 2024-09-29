# User Service API

This FastAPI application provides APIs for user management, including registration, profile retrieval, login, and token refresh. It integrates with Kafka for event streaming.

## Features

- **Register User**: Register a new user and publish an event to Kafka.
- **Get User Profile**: Retrieve the profile of the currently authenticated user.
- **Login**: Authenticate a user and issue access and refresh tokens.
- **Refresh Token**: Refresh the access token using a refresh token.

## API Endpoints

### 1. Register User

- **POST** `/user/register`
  - **Description**: Register a new user and publish an event to Kafka.
  - **Body**:
    ```json
    {
      "username": "newuser",
      "email": "newuser@example.com",
      "password": "securepassword"
    }
    ```
  - **Response**:
    ```json
    {
      "message": "New User Created Successfully"
    }
    ```
  - **Error**:
    ```json
    {
      "detail": "User with these credentials already exists"
    }
    ```

### 2. Get User Profile

- **GET** `/user/me`
  - **Description**: Retrieve the profile of the currently authenticated user.
  - **Response**:
    ```json
    {
      "username": "existinguser",
      "email": "existinguser@example.com",
      "created_at": "timestamp",
      "updated_at": "timestamp"
    }
    ```
  - **Authentication Required**: Yes

### 3. Login

- **POST** `/user/login`
  - **Description**: Authenticate a user and issue access and refresh tokens.
  - **Body**:
    ```json
    {
      "username": "existinguser",
      "password": "userpassword"
    }
    ```
  - **Response**:
    ```json
    {
      "access_token": "your_access_token",
      "token_type": "bearer",
      "refresh_token": "your_refresh_token"
    }
    ```
  - **Error**:
    ```json
    {
      "detail": "Invalid username or password"
    }
    ```

### 4. Refresh Token

- **POST** `/user/login/refresh`
  - **Description**: Refresh the access token using a refresh token.
  - **Body**:
    ```json
    {
      "old_refresh_token": "your_old_refresh_token"
    }
    ```
  - **Response**:
    ```json
    {
      "access_token": "your_new_access_token",
      "token_type": "bearer",
      "refresh_token": "your_new_refresh_token"
    }
    ```
  - **Error**:
    ```json
    {
      "detail": "Invalid token, Please login again"
    }
    ```

## Kafka Integration

- **Producer**: A Kafka producer is used to send user events.
- **Topic**: The topic for user events is specified in the environment variable `KAFKA_USER_TOPIC`.
- **Protobuf Serialization**: Users are serialized using Protobuf format before being sent to Kafka.

## Authentication

- **JWT Tokens**: Access and refresh tokens are used for authentication and authorization.
- **Password Hashing**: Passwords are hashed before storage.

## Dependencies

- **FastAPI**: Web framework for building APIs.
- **SQLModel**: ORM for database operations.
- **aiokafka**: Kafka client for asynchronous communication.
- **requests**: HTTP library for making requests.

## Environment Variables

- `KAFKA_USER_TOPIC`: Kafka topic for user events.
- `EXPIRY_TIME`: Expiry time for access tokens in minutes.

## Notes

- Ensure Kafka is properly configured and running.
- Make sure to handle exceptions and errors appropriately in a production environment.
