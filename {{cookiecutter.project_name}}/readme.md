# FastAPI Docker Boilerplate

This project is based on [FastAPI Docker Boilerplate](https://github.com/Afaneor/fastapi-docker-boilerplate).

## Table of Contents

- [Setup](#setup)
- [Running the Application](#running-the-application)
- [Configuration](#configuration)
- [Database Migrations](#database-migrations)
- [Translations](#translations)
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

### using docker for development

```shell
docker-compose -f docker-compose.local.yml up -d
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

## Translations

The project supports internationalization using FastAPI-Babel and Pybabel. Translation files are managed using Make commands for easy maintenance.

### Translation Management Commands

1. **Extract Translatable Strings**
   ```shell
   make translations-extract
   ```
   This will scan your project and create/update the message template (POT) file.

2. **Initialize a New Language**
   ```shell
   make translations-init LANG=xx
   ```
   Replace `xx` with the language code (e.g., `ru` for Russian, `de` for German).

3. **Compile Translation Messages**
   ```shell
   make translations-compile
   ```
   Compiles the translation files for use in the application.

4. **Update Existing Translations**
   ```shell
   make translations-update
   ```
   Updates existing translation files with new strings found in the code.

5. **Complete Translation Workflow**
   ```shell
   make translations-all LANG=xx
   ```
   Runs the complete workflow for a new language: extract strings, initialize language, and compile messages.

### Translation File Structure
- `/app/locales/`: Directory containing all translation files
- `/app/locales/messages.pot`: Template file containing all translatable strings
- `/app/locales/<lang>/LC_MESSAGES/`: Language-specific translation files

### Using Translations in Code
The project uses FastAPI-Babel for handling translations. You can use the translation system in your code like this:

```python
from fastapi_babel import _
# In your route or model:
message = _("Your message to translate")
```

## CI/CD

The project includes a basic CI/CD configuration using GitLab CI. The `.gitlab-ci.yml` file contains stage for building image of the application.