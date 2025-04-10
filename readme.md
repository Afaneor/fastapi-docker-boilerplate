# FastAPI Boilerplate with TortoiseORM and Docker

This project is a high-performance template for quickly creating APIs using FastAPI, TortoiseORM, and Docker. It's ideal for developers who want to quickly start new projects with a modern technology stack.

### You can find overview of this template in the [youtube video](https://www.youtube.com/watch?v=4AMxbzZYOnU)

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
- 🌍 **Internationalization**: Built-in i18n support with FastAPI-Babel
- 🚀 **GitLab CI**: Basic GitLab CI pipeline for building Docker images
- 📚 **Documentation**: Detailed documentation for easy project setup
- 📦 **Pagination**: Built-in pagination support for listing endpoints

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

## What's Included

- FastAPI
- Sample endpoint
- TortoiseORM
- Sample Test
- Ruff (replaces Flake8 & Isort)
- Pydantic Settings
- Redis support
- Basic GitLab CI pipeline
- Internationalization support with FastAPI-Babel

## Internationalization (i18n)

The boilerplate comes with built-in internationalization support using FastAPI-Babel and Pybabel. Translation management is automated through make commands.

### Translation Commands

Makefile provides several commands for managing translations:

```bash
# Extract translatable strings
make translations-extract

# Initialize a new language (e.g., Russian)
make translations-init LANG=ru

# Compile translation messages
make translations-compile

# Update existing translations
make translations-update

# Complete workflow for new language
make translations-all LANG=xx
```

### Using Translations

1. Mark strings for translation in your code:
```python
from fastapi_babel import _

@app.get("/hello")
async def hello():
    return {"message": _("Hello, World!")}
```

2. Structure of translation files:
```
app/
├── locales/
│   ├── messages.pot      # Template file
│   ├── en/              # English translations
│   │   └── LC_MESSAGES/
│   └── ru/              # Russian translations
│       └── LC_MESSAGES/
```

For more details on translation management, check the project's documentation after generation.

## Frequently Asked Questions

### Model is not reflected in the migration
Add the Model to `__init__.py` in the app/models folder.

### How to create a new migration?
```bash
aerich migrate
```

### How to add a new language?
Use the make command: `make translations-init LANG=xx` where xx is the language code (e.g., de for German).

## GitLab CI Pipeline

The project includes a basic GitLab CI pipeline configuration for building Docker images. You can find the configuration in the `.gitlab-ci.yml` file. This pipeline automates the process of building and potentially deploying your Docker image.

## Pydantic Settings

We use Pydantic for managing application settings. This ensures type-safe and validated configuration. You can find the settings in the `app/config` directory.

## Support

If you have any questions or issues, please create an issue in the project repository.

## TODO

- [x] Liters (Ruff)
- [x] Basic test
- [x] Internationalization support
- [ ] Docker compose for development
- [ ] Optional [Wemake services linter](https://github.com/wemake-services/wemake-python-styleguide) rules
- [ ] Optional Admin panel
- [ ] Optional FastStream
- [ ] Optional GitHub Actions
