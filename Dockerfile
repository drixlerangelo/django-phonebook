# The base image we want to inherit from
FROM python:3.11-slim AS poetry-builder

ARG DJANGO_ENV

ENV DJANGO_ENV=${DJANGO_ENV} \
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
        postgresql \
        zsh \
        supervisor \
        iputils-ping \
    # Cleaning cache:
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* \
    && pip install "poetry==$POETRY_VERSION" && poetry --version

# set work directory
WORKDIR /app
COPY pyproject.toml poetry.lock /app/

# Install dependencies:
RUN poetry export -f requirements.txt --output requirements.txt


FROM poetry-builder AS development
RUN poetry install

# copy project
COPY . .

# setup supervisor
RUN mkdir -p /app/logs
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod a+x /app/entrypoint.sh

CMD ["/app/entrypoint.sh" ]


FROM python:3.11-slim AS production

ARG DJANGO_ENV

ENV DJANGO_ENV=${DJANGO_ENV}

# System deps:
    RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        bash \
        build-essential \
        libpq-dev \
        postgresql \
        supervisor \
    # Cleaning cache:
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=poetry-builder /app/requirements.txt /app/

RUN python -m pip install --no-cache-dir --upgrade pip
RUN python -m pip install -r requirements.txt

# copy project
COPY . .

# setup supervisor
RUN mkdir -p /app/logs
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod a+x /app/entrypoint.sh

CMD ["/app/entrypoint.sh" ]
