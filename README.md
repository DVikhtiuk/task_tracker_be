# Task Tracker Backend

This is the backend part of the Task Tracker application. The project is built with Python and uses FastAPI for creating APIs, as well as SQLAlchemy and Alembic for database management.

## Requirements

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Installation and Running the Project


### 1. Build and Start the Docker Containers

To build and start the Docker containers, run the following command:

```bash
docker compose up --build
```

### 2. Apply Database Migrations:

Once the containers are up, apply the database migrations to set up the schema:

```bash
docker compose exec app alembic upgrade head
```

This will create the necessary tables and apply any pending migrations.

### 3. Seed the Database with Initial Data:

To populate the database with default data, run the seed script:

```bash
docker compose exec app python seed.py
```
This script will insert default data like users or other required initial values into the database.

## Stop the Containers:

When you're done, you can stop the containers using:

```bash
docker compose down
```

This command will stop and remove the running containers, but will keep the volumes intact. If you want to remove the volumes as well, use the following:

```bash
docker compose down -v
```