FROM python:3.11-slim AS poetry-builder

    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
ENV POETRY_VERSION=1.8.2 \
    # make poetry install to this location
    POETRY_HOME="/app" \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for building python deps
        # build-essential \
        # deps for installing poetry
        curl

WORKDIR $POETRY_HOME

RUN curl -sSL https://install.python-poetry.org | python -

COPY pyproject.toml poetry.lock ./
ENV PATH="$POETRY_HOME/bin:$PATH:/usr/bin/pg_config"
# RUN poetry install --only main --no-root && rm -rf $POETRY_CACHE_DIR
RUN poetry export -f requirements.txt --output $POETRY_HOME/requirements.txt


# The base image we want to inherit from
FROM python:3.11-slim-buster AS development

ARG DJANGO_ENV

ENV DJANGO_ENV=development \
    # python:
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    # pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_VERSION=1.8.2 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry'

# System deps:
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        bash \
        build-essential \
        curl \
        gettext \
        git \
        libpq-dev \
        wget \
        pipx \
    # Cleaning cache:
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
    # install pipx
    && pipx ensurepath && sudo pipx ensurepath --global \
    # install poetry
    && pipx install poetry==$POETRY_VERSION

# set work directory
WORKDIR /app
COPY pyproject.toml poetry.lock /app/

# Install dependencies:
RUN poetry install
# copy project
COPY . .

CMD [ "python", "-Wd", "manage.py", "runserver", "0.0.0.0:8000" ]


FROM python:3.11-slim AS production

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for building python deps
        build-essential \
        # for postgres support
        postgresql \
        # reinstall, for postgres
        --reinstall libpq-dev

    # python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # make poetry install to this location
    PROJECT_DIR="/app"

WORKDIR $PROJECT_DIR

# copy project requirement files here to ensure they will be cached.
COPY --from=poetry-builder $PROJECT_DIR $PROJECT_DIR

RUN python -m pip install --no-cache-dir --upgrade pip
RUN python -m pip install -r requirements.txt

ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]
