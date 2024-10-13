# FastAPI Boilerplate with TortoiseORM and Docker

This project is a high-performance template for quickly creating APIs using FastAPI, TortoiseORM, and Docker. It's ideal for developers who want to quickly start new projects with a modern technology stack.

## Community

Join our Russian-speaking community for discussions, questions, and support:

- Telegram Channel: [@pavlin_share](https://t.me/pavlin_share)
- Telegram Chat: [@share_it_group](https://t.me/share_it_group)

## Features

- 🚀 **FastAPI**: Modern, fast (high-performance) web framework for building APIs with Python 3.7+
- 🐢 **TortoiseORM**: Easy-to-use asyncio ORM for Python
- 🐳 **Docker**: Full containerization support for easy deployment
- 📊 **Migrations**: Built-in database migration support with Aerich
- 🧪 **Testing**: Sample tests for quick TDD start
- 🧹 **Linters**: Configured Ruff for maintaining clean code
- 🔒 **Pydantic Settings**: Secure and type-safe configuration management
- 🔄 **Redis Support**: Built-in Redis integration for caching and session management
- 🚀 **GitLab CI**: Basic GitLab CI pipeline for building Docker images

## Getting Started

### Prerequisites

Make sure you have Python 3.7+ and pip installed. Then install Cookiecutter:

```bash
pip install "cookiecutter>=1.7.0"
```

### Creating a New Project

Use the following command to create a new project:

```bash
cookiecutter https://github.com/Afaneor/fastapi-docker-boilerplate
```

### Setting Up the Environment

1. Create the `.env` file:
   ```bash
   cp .env.example .env
   ```

2. Configure PyCharm (if using):
   Mark the app folder as a source root.
   ![PyCharm Configuration](img.png)

3. Start the database and Redis in Docker:
   ```bash
   docker-compose up -d postgres redis
   ```

4. Initialize migrations:
   ```bash
   aerich init
   ```

## Frequently Asked Questions

### Model is not reflected in the migration
Add the Model to `__init__.py` in the app/models folder.

### How to create a new migration?
```bash
aerich migrate
```

## What's Included

- FastAPI
- Sample endpoint
- TortoiseORM
- Sample Test
- Ruff (replaces Flake8 & Isort)
- Pydantic Settings
- Redis support
- Basic GitLab CI pipeline

## GitLab CI Pipeline

The project includes a basic GitLab CI pipeline configuration for building Docker images. You can find the configuration in the `.gitlab-ci.yml` file. This pipeline automates the process of building and potentially deploying your Docker image.

## Pydantic Settings

We use Pydantic for managing application settings. This ensures type-safe and validated configuration. You can find the settings in the `app/config` directory.

## Support

If you have any questions or issues, please create an issue in the project repository.

## TODO

- [x] Liters (Ruff)
- [x] Basic test
- [ ] Docker compose for development
- [ ] Optional [Wemake services linter](https://github.com/wemake-services/wemake-python-styleguide) rules
- [ ] Optional Admin panel
- [ ] Optional FastStream
- [ ] Optional GitHub Actions
