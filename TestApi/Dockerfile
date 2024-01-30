FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

COPY . /usr/src/app/