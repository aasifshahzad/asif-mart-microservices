# Online Aasif Mart API - Event-Driven Microservices Architecture

## Project Overview

This project develops an online mart API using an event-driven microservices architecture. It utilizes modern technologies such as **FastAPI**, **Docker**, **PostgreSQL**, **Kafka**, **Protobuf**, **Schema Registry** and **Kong** to ensure scalability, maintainability, and efficient handling of high transaction volumes in a distributed system. The project follows Test-Driven Development (TDD) and Behavior-Driven Development (BDD) practices to ensure high code quality and alignment with business requirements.

## Objectives

- Develop a **scalable and efficient API** for an online mart using microservices.
- Implement **event-driven architecture** for asynchronous communication between services.
- Leverage **FastAPI**, **Docker**, **Kafka**, and **Protobuf** for microservices and data streaming.
- Utilize **DevContainers** and **Docker Compose** for consistent development environments.
- Incorporate **TDD** and **BDD** for robust development.
  <!-- - Use **Kong API Gateway** for API management. -->
  <!-- - Deploy the system using **Azure Container Apps** with **GitHub Actions** for CI/CD. -->

## Key Technologies

- **FastAPI**: High-performance web framework for building APIs.
- **Docker**: Containerization of microservices.
- **DevContainers**: Consistent development environments.
- **Docker Compose**: Orchestrates multi-container applications.
- **PostgreSQL**: Relational database for data persistence.
- **SQLModel**: ORM for PostgreSQL database interactions.
- **Kafka**: Event-streaming platform for real-time data pipelines.
- **Schema Registry**: Store and Enforces data schemas and consistent data serialization and deserialization across microservices architecture.
- **Protobuf**: Efficient data serialization.
- **GitHub Actions**: CI/CD pipeline for automated testing and deployment.
- **Pytest**: Unit testing for TDD.
- **Behave**: BDD framework for scenario-driven testing.
  <!-- - **Kong**: API Gateway for request routing, authentication, and rate limiting. -->
  <!-- - **Dapr**: Distributed application runtime for microservice connectivity. -->
  <!-- - **Azure Container Apps**: Cloud deployment platform. -->

## Architecture

```bash
.
├── .gitignore
├── compose.yaml
├── procedure.txt
├── README.md
├── rename_env.py
├── structure.py
├── inventory_service/
│ ├── .env.example
│ ├── .gitignore
│ ├── Dockerfile.dev
│ ├── poetry.lock
│ ├── pyproject.toml
│ ├── README.md
│ ├── consumer/
│ │ └── consumer.py
│ ├── inventory/
│ │ ├── db.py
│ │ ├── main.py
│ │ └── setting.py
│ ├── producer/
│ │ └── producer.py
│ ├── router/
│ │ ├── inventory.py
│ │ └── kafka_curd_functions.py
│ └── schemas/
│ ├── inventory.proto
│ ├── inventory_pb2.py
│ ├── model.py
│ └── schema_registry.py
│ └── tests/
│   └── test_inventory.py

├── notification_service/
│ ├── .env.example
│ ├── .gitignore
│ ├── Dockerfile.dev
│ ├── poetry.lock
│ ├── pyproject.toml
│ ├── README.md
│ ├── consumer/
│ │ └── consumer_functions.py
│ ├── notification/
│ │ ├── db.py
│ │ ├── main.py
│ │ └── setting.py
│ ├── producer/
│ │ └── producer_functions.py
│ ├── router/
│ │ ├── kafka_curd_functions.py
│ │ └── notification.py
│ └── schemas/
│ ├── model.py
│ ├── notification.proto
│ ├── notification_pb2.py
│ └── schema_registry.py
│ └── tests/
│ └── test_notification.py
├── order_service/
│ ├── .env.example
│ ├── .gitignore
│ ├── Dockerfile.dev
│ ├── poetry.lock
│ ├── pyproject.toml
│ ├── README.md
│ ├── consumer/
│ │ └── consumer_function.py
│ ├── order/
│ │ ├── db.py
│ │ ├── main.py
│ │ ├── setting.py
│ │ └── **init**.py
│ ├── producer/
│ │ └── producer_function.py
│ ├── router/
│ │ ├── kafka_curd_functions.py
│ │ └── order.py
│ └── schemas/
│ ├── model.py
│ ├── order.proto
│ ├── order_pb2.py
│ └── schema_registry.py
│ └── tests/
│ ├── test_order.py
│ └── **init**.py
├── payment_service/
│ ├── .env.example
│ ├── .gitignore
│ ├── Dockerfile.dev
│ ├── help.txt
│ ├── poetry.lock
│ ├── pyproject.toml
│ ├── README.md
│ ├── requirements.txt
│ ├── consumer/
│ │ └── consumer.py
│ ├── payment/
│ │ ├── db.py
│ │ ├── main.py
│ │ ├── model.py
│ │ ├── setting.py
│ │ └── **init**.py
│ ├── producer/
│ │ └── payment_producer.py
│ ├── router/
│ │ ├── payment.py
│ │ └── payment_curd_functions.py
│ └── schemas/
│ ├── payment.proto
│ ├── payment_pb2.py
│ └── schema_registry.py
│ └── tests/
│ ├── test_payment.py
│ └── **init**.py
├── product_service/
│ ├── .env.example
│ ├── .gitignore
│ ├── Dockerfile.dev
│ ├── poetry.lock
│ ├── pyproject.toml
│ ├── README.md
│ ├── consumer/
│ │ └── consumer_functions.py
│ ├── images/
│ │ ├── 18b77f5f-500e-442b-91ff-6197dadf5f3d.jpg
│ │ ├── 8cbb2ec6-ff3b-4fab-8096-cc4fc2121cfb.jpg
│ │ ├── Linkedin Profile .png
│ │ ├── profile-pic.png
│ │ └── smile.jpeg
│ ├── producer/
│ │ └── producer_functions.py
│ ├── product/
│ │ ├── db.py
│ │ ├── main.py
│ │ ├── setting.py
│ │ └── **init**.py
│ ├── router/
│ │ ├── kafka_curd_functions.py
│ │ └── product.py
│ └── schemas/
│ ├── model.py
│ ├── product.proto
│ ├── product_pb2.py
│ └── schema_registry.py
│ └── tests/
│ ├── test_product.py
│ └── **init**.py
└── user_service/
├── .env.example
├── .gitignore
├── Dockerfile.dev
├── LICENSE
├── poetry.lock
├── pyproject.toml
├── README.md
├── consumer/
│ └── consumer.py
├── producer/
│ └── producer.py
├── router/
│ ├── kafka_curd_functions.py
│ └── user.py
└── schemas/
├── models.py
├── schema_registry.py
├── user.proto
└── user_pb2.py
└── tests/
├── test_user.py
└── **init**.py
└── user/
├── auth.py
├── db.py
├── main.py
├── setting.py
└── **init**.py
```

### Microservices

1. **User Service**: Manages user authentication and profiles.
2. **Product Service**: Handles product catalog and CRUD operations.
3. **Order Service**: Processes orders and tracks status.
4. **Inventory Service**: Manages stock levels.
5. **Notification Service**: Sends notifications (email/SMS) to users.
6. **Payment Service**: Processes payments and records transactions.

### Event-Driven Communication

- **Kafka**: Event bus for asynchronous communication between services.
- **Protobuf**: Defines message structure for efficient data serialization.

### Data Storage

- **PostgreSQL**: Each service has its own database instance.
<!-- ### API Gateway:


- **Kong**: Manages API requests, authentication, and routing. -->

### Development Methodologies

- **TDD**: Writing tests before code using Pytest.
- **BDD**: Aligning development with business requirements using Behave and Gherkin.

## Setup Instructions and Deployment Guide

1. **Ensure you have the following tools installed:**

   - Docker
   - Visual Studio Code with the DevContainers extension

2. **Clone the Repository**:

   ```bash
   git clone https://github.com/aasifshahzad/aasif-mart-microservices
   cd aasif-mart-microservices
   ```

   - Launch Visual Studio Code and open the project folder

3. **Rename the .env.example file to .env file in each repository running the under-mentioned file**:

   ```bash
      rename_env.py
   ```

4. **Docker Compose**

   To set up all services and dependencies, run the following command:

   ```bash
   docker-compose up --build
   ```

5. **Services URL's**

   To view all services on swagger UI click on undermentioned URL's:

   - [**Payment Service**](http://localhost:8001/docs#/)

   - [**Inventory Service**](http://localhost:8002/docs#/)

   - [**Notification Service**](http://localhost:8003/docs#/)

   - [**Order Service**](http://localhost:8004/docs#/)

   - [**Product Service**](http://localhost:8005/docs#/)

   - [**User Service**](http://localhost:8006/docs#/)

   - [**Kafka UI**](http://localhost:8080/)

### Unit Tests

Use Pytest for unit tests by accesing the Docker Dev Container or by Docker Interactive mode:

```bash
pytest
```

## Kafka & Protobuf Setup

- **Kafka**: Configured for event streaming between microservices.
- **Protobuf**: Used for message serialization, ensuring efficient data exchange between services.

<!-- ## Kong API Gateway

- **Kong**: Configured for API management, including routing, authentication, and rate limiting.

### Phase 1: Setup & Initial Development

- Configure DevContainers and Docker Compose.
- Develop core microservices: User, Product, Order, Payment, Notification.
- Set up Kafka and define Protobuf schemas.
- Write and pass unit tests using Pytest and BDD scenarios using Behave.

### Phase 2: Expand Functionality

- Add Inventory and Notification services.
- Integrate event-driven communication with Kafka.

### Phase 3: API Gateway and Finalization

- Configure Kong API Gateway for all microservices.
- Perform load testing and ensure scalability.

### Phase 4 (Optional): Monitoring and Continuous Delivery

- Set up Prometheus and Grafana for monitoring.
- Use GitHub Actions for continuous delivery.

## CI/CD Pipeline

- **Test Automation**: All unit and BDD tests are executed on each commit.
- **Deployment**: Automated deployment to Azure Container Apps after successful tests. -->

## License

This project is licensed under the MIT License.
