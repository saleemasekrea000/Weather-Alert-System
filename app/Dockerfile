FROM python:3.12.8-alpine3.21@sha256:ba13ef990f6e5d13014e9e8d04c02a8fdb0fe53d6dccf6e19147f316e6cc3a84

LABEL description="Weather Alert System" maintainer="saleemasekrea000@gmail.com"

# prevents Python from writing compiled Python files to the disk --> reduces image size
ENV PYTHONDONTWRITEBYTECODE=1

# logs and output are shown in real-time on terminal --> easier to debug
ENV PYTHONUNBUFFERED=1

# Create a non-root user
RUN addgroup -S app_group && adduser -S app_user -G app_group

WORKDIR /app

# To wait for the Postgres container to be available
COPY --from=ghcr.io/ufoscout/docker-compose-wait:latest /wait /wait

# required for the health check 
RUN apk add --no-cache curl

# Requiments is copied first to cache installation of dependencies
COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade pip==25.0 \
    && pip install --no-cache-dir --upgrade -r requirements.txt

COPY src /app/src/
COPY alembic /app/alembic/
COPY alembic.ini /app/alembic.ini

# Change the owner of the app directory
RUN chown -R app_user:app_group /app/

# Switch to the non-root user
USER app_user
