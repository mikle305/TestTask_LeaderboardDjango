FROM python:3.12.8-alpine

EXPOSE 8080

WORKDIR /code

RUN pip install --upgrade pip
RUN apk add gcc musl-dev libffi-dev
RUN pip install poetry

COPY ./src ./src
COPY .env .
COPY poetry.lock pyproject.toml ./
COPY manage.py .

RUN poetry config virtualenvs.create false \
    && poetry config virtualenvs.in-project false \
    && poetry lock \
    && poetry install --no-interaction --no-ansi 

ENV APP__IS_DOCKERIZED=Yes
