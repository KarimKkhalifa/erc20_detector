# ERC20 Detector App

## Prerequisites

Before running the ERC20 Detector App, ensure you have the following installed:

- Docker and Docker Compose
- Python 3.10 or newer
- Access to a PostgreSQL database

## Configuration

1. **Environment Variables**: Configure your environment variables by creating a `.env` file in the root directory of the project. This file should contain the necessary configurations for the PostgreSQL database connection, RabbitMQ connection, and any other sensitive or configurable values.

    Example `.env` file:
    ```
    DB_HOST=""
    RABBITMQ_HOST=""
    DB_NAME=""
    DB_USER=""
    DB_PASS=""
    DB_PORT=""
    RABBITMQ_DEFAULT_USER=""
    RABBITMQ_DEFAULT_PASS=""
    ```

2. **Database Setup**: Ensure your PostgreSQL database is accessible and configured to accept connections from your application. Follow the steps in the project documentation to allow connections from Docker containers.


## Running the Application

To run the ERC20 Detector App, follow these steps:

1. **Build the Docker Image**:
    - Navigate to the root directory of the project where the `docker-compose.yml` file is located.
    - Run the following command to build the Docker image:
    ```
    docker-compose build
    ```

2. **Start the Services**:
    - Once the build is complete, start the application and RabbitMQ services by running:
    ```
    docker-compose up
    ```
    - This command starts all the services defined in `docker-compose.yml`, including the ERC20 Detector App and RabbitMQ.


## Stopping the Application

To stop the ERC20 Detector App and related services:

- Press `Ctrl+C` in the terminal where `docker-compose up` is running.
- To remove the containers, networks, and volumes associated with the application, run:
```
docker-compose down
```


