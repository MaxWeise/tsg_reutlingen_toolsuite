# Dockerfile for the Fastapi Backend
FROM python:3.12-slim

WORKDIR /code

COPY ./pyproject.toml /code/pyproject.toml

RUN pip install --no-cache-dir --upgrade .

COPY ./saison_kickstarter /code/saison_kickstarter

CMD ["fastapi", "run", "saison_kickstarter/api.py"]
