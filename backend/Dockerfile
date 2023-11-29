FROM python:3.11-slim-buster

WORKDIR /app


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install python dependencies
COPY ./app/pyproject.toml ./app/poetry.lock ./
ARG INSTALL_DEV=true
RUN pip install --upgrade pip && pip install poetry && poetry config virtualenvs.create false && bash -c "if [ $INSTALL_DEV == 'true' ] ; then poetry install --no-root ; else poetry install --no-root --no-dev ; fi"

# add app
COPY . .