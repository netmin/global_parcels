# Project README

## Overview

This README provides setup and running instructions for a project that includes a backend service, RabbitMQ for message queuing, 
MySQL for the database, Adminer for database management, and a web interface accessible via a local server. 
The project utilizes Docker and Docker Compose for easy setup and deployment.

## Prerequisites

- Docker and Docker Compose should be installed on your system.

## Setup and Running

### Starting the Project

Start all services defined in the Docker Compose file:

```bash
docker compose up -d
```

This command launches the services in detached mode.

### Database Migrations

Run database migrations to set up the necessary tables:

```bash
docker compose exec backend aerich upgrade
```

### Creating Initial Data

Populate initial data in the `parcel_types` table:

```bash
docker compose exec backend python app/fill_db.py
```

### Running Tests

Execute the test suite:

```bash
docker compose exec backend python -m pytest
```

### Accessing the API Documentation

FastAPI generates and serves interactive API documentation. Once the backend service is up, you can access the API documentation at:

- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

These pages provide an interactive interface to explore and test the API endpoints.

### Web Interface

The web interface for the project is accessible at:

- URL: [http://localhost:3000](http://localhost:3000)

This interface provides a user-friendly way to interact with the system, allowing you to view, create, and manage parcels.

### Adminer - Database Management

Adminer is available for database management:

- URL: [http://localhost:8080](http://localhost:8080)
- Server: `db`
- User: `root`
- Password: `example`

## Additional Notes

- Ensure all Docker containers are running before executing any commands.
- Commands using `docker compose exec` are run within the context of running containers.
- Modify the commands according to any changes in the Docker Compose configuration, such as service names or database credentials.
