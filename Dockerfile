FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY poetry.lock pyproject.toml /code/

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY . /code/
