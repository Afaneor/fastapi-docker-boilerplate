# FastAPI Docker Boilerplate

This project is based on [FastAPI Docker Boilerplate](https://github.com/Afaneor/fastapi-docker-boilerplate).

## Table of Contents

- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Configuration](#configuration)
- [Database Migrations](#database-migrations)
- [CI/CD](#cicd)

## Setup

1. Clone the repository
2. Create a `.env` file based on `.env.example`:
   ```
   cp .env.example .env
   ```
3. Configure the environment variables in the `.env` file

## Running the Application

### Locally

```shell
python3 app/main.py
```

### Using Docker

```shell
docker-compose up -d
```

## Configuration

Project settings are divided into components and environments (development/production). They are located in the `app/config/components/` directory.

The main logic for combining settings is in the `__init__.py` file.

To switch between environments, change the `ENVIRONMENT` variable in the `.env` file.

## Database Migrations

The project uses [Tortoise ORM](https://github.com/tortoise/tortoise-orm) and [Aerich](https://github.com/tortoise/aerich) for managing migrations.

### Initializing Migrations

```shell
aerich init-db
```

This will create a migrations folder in the db module. All models in `__init__.py` (db module) will be reflected in the migration.

### Creating a New Migration

```shell
aerich migrate
```

### Applying Migrations

```shell
aerich upgrade
```

## CI/CD

The project includes a basic CI/CD configuration using GitLab CI. The `.gitlab-ci.yml` file contains stage for building image of the application.
