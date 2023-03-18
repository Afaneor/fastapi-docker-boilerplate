FROM python:3.10-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PIP_INDEX_URL=https://pypi.letsnova.ru/simple/ \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=off \
    USE_DOCKER=1 \
	# poetry:
	POETRY_VERSION=1.2.0 \
	POETRY_VIRTUALENVS_CREATE=false \
	POETRY_CACHE_DIR='/var/cache/pypoetry' \
	# Locale settings
	LANG=ru_RU.UTF-8 \
	LC_ALL=ru_RU.UTF-8 \
	LC_TIME=ru_RU.UTF-8 \
	LANGUAGE=ru_RU.UTF-8 \
	# paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

###############################################
# Builder Image
###############################################
FROM python-base as builder-base

RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    curl \
    gettext \
    gcc \
  && pip install "poetry==$POETRY_VERSION" && poetry --version \
  # Cleaning cache:
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev

FROM python-base as production
COPY --from=builder-base $PYSETUP_PATH $PYSETUP_PATH
COPY ./app /app/
WORKDIR /app
CMD ["python", "main.py"]
