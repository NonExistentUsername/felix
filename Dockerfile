FROM python:3.10.7-slim

WORKDIR /usr/src/app/

RUN pip install poetry
COPY poetry.lock pyproject.toml /usr/src/app/
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y netcat
