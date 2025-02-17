# Weather Alerts System

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-D83C3A?style=flat&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814D?style=flat&logo=celery&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![pytest](https://img.shields.io/badge/Pytest-302C2F?style=flat&logo=pytest&logoColor=white)


This repository contains the weather monitoring and alert system using Python. This system will
fetch weather data from a public API, process it asynchronously, and provide various endpoints
for weather information and alerts.

## Table of Contents

1. [Setup Instructions](#setup-instructions)
    - [Requirements](#requirements)
    - [Manual](#manual)
    - [Docker](#docker)
2. [API Documentation](#api-documentation)
    - [Alert Router](#alert-router)
    - [Weather Router](#weather-router)
3. [Architecture Overview](#architecture-overview)
    - [Database](#database)
    - [Redis](#redis)
    - [Rate Limiter](#rate-limiter)
    - [Celery](#celery)
    - [Celery Tasks](#celery-tasks)
4. [Tests](#tests)

4. [Design Decisions and Trade-offs](#design-decisions-and-trade-offs)
5. [Future Improvements](#future-improvements)

## Setup Instructions

### Requirements

- Python 3.8 or higher
- `pip` package manager.

### Manual

- Clone this branch to your local machine

```bash
git clone git@github.com:saleemasekrea000/Weather-Alert-System-.git
```

- Navigate to the `app` folder

```bash
cd app
```

- Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

- Install the required packages

```bash
pip install -r requirements.txt
```

- Create a `.env` file in the root directory to store environment variables following the `.env.example`

- Run the application

```bash
uvicorn src.main:app
```

The application will be available at [localhost:8000](http://localhost:8000/)

## Docker

- make sure you are in the `Weather Alert System` directory

```bash
sudo docker-compose build
```

```bash
sudo docker-compose up
```

The application will be available at [localhost:8000](http://localhost:8000/)

## API Documentation

### Alert Service

#### 1. Subscribe to Alerts

- **Endpoint**: `POST /alert/subscribe`
- **Summary**: Subscribe to Alerts
- **Description**: Allows a user to subscribe to alerts by providing subscription details.
- **Request Body**: `SubscriptionRequest`
- **Response**: `SubscriptionRequest`
- **Dependencies**:
  - `db`: Database session (dependency)
  
| Parameter      | Type               | Description                           |
|----------------|--------------------|---------------------------------------|
| `subscription` | `SubscriptionRequest` | Subscription details (request body)  |
| `db`           | `Session`          | Database session (dependency)        |

#### 2. Get Active Alerts

- **Endpoint**: `GET /alert/active`
- **Summary**: Get Active Alerts
- **Description**: Retrieves a list of currently active alerts.
- **Response**: `List[AlertResponse]`
- **Dependencies**:
  - `db`: Database session (dependency)

| Parameter      | Type       | Description                           |
|----------------|------------|---------------------------------------|
| `db`           | `Session`  | Database session (dependency)        |

---

### Weather Service

#### 1. Get Current Weather

- **Endpoint**: `GET /weather/current/{city}`
- **Summary**: Get Current Weather
- **Description**: Fetches the current weather for a given city.
- **Request Parameters**: `city` (Path parameter)
- **Response**: `dict[str, Any]`
- **Dependencies**:
  - `db`: Database session (dependency)
  - `r`: Redis cache session (dependency)
  - `rate_limit`: Rate limiter (dependency)

| Parameter      | Type       | Description                           |
|----------------|------------|---------------------------------------|
| `city`         | `str`      | The name of the city                 |
| `db`           | `Session`  | Database session (dependency)        |
| `r`            | `Redis`    | Redis cache session (dependency)     |
| `rate_limit`   | `Limiter`  | Rate limiter (dependency)            |

#### 2. Get Weather Forecast

- **Endpoint**: `GET /weather/forecast{city}`
- **Summary**: Get Weather Forecast
- **Description**: Retrieves the weather forecast for the next 5 days.
- **Request Parameters**:
  - `city` (Path parameter)
  - `days` (Query parameter, default: 5)
- **Response**: `dict[str, Any]`
- **Dependencies**:
  - `r`: Redis cache session (dependency)
  - `rate_limit`: Rate limiter (dependency)

| Parameter      | Type       | Description                           |
|----------------|------------|---------------------------------------|
| `city`         | `str`      | The name of the city                 |
| `days`         | `int`      | Number of days for the forecast (default: 5) |
| `r`            | `Redis`    | Redis cache session (dependency)     |
| `rate_limit`   | `Limiter`  | Rate limiter (dependency)            |

## Architecture Overview

- For an overview of the system architecture, please refer to [System Architecture Diagram](https://www.mermaidchart.com/raw/b50e6fd1-067a-4dcb-b6ee-def2a2c61c76?theme=dark&version=v0.1&format=svg).

### Database

- The system uses a Relational Database (PostgreSQL) to store user data, alerts, weather data, etc.

- created indexes on key columns in the database to optimize query performance, especially for frequently accessed data (`city_name`, `is_active`, `sub_id`, `email` )

- For the full database schema, refer to [Database Schema](https://dbdiagram.io/d/67b355f0263d6cf9a072e3dc).
### Redis

- `Caches`: Redis is used to cache weather data to reduce load on the backend and speed up responses for frequently requested weather data.

- `Message Broker`: Redis is used as a message broker for Celery, handling the asynchronous execution of tasks like `sending emails` and `updating weather data`.

- `Rate Limiter`: Redis is used to implement rate limiting

### Rate Limiter

- The rate limiter tracks the number of requests to an endpoint using Redis. weather endpoint has a rate limit defined by a count and window time (60 requests per minute)

- If the request count exceeds the allowed limit, the system responds with an HTTP 429 status code and a message to inform the user to try again later.

### Celery

- task Queue: Celery is used for handling background tasks asynchronously. It executes tasks such as s`ending subscription emails`, `weather alert emails`, and `updating weather data for cities`.

- Scheduled Tasks: Some tasks are scheduled using Celery Beat to run periodically (updating weather data for all subscribed cities every 15 minutes).

### Celery Tasks

- `send_subscription_email`

  - Sends a welcome email to a user upon successful subscription to weather alerts.

- `send_weather_alert_email`

  - Sends a weather alert email to a user if their subscribed conditions (temperature threshold) are met.

- `update_weather_data`

  - Updates the weather data for a specific city and checks if any alert conditions are triggered based on the new data.

- `update_all_weather_data`

  - Updates weather data for all subscribed cities. This task queries the list of cities from the database and triggers the update_weather_data task for each city.

- `check_and_trigger_alerts`

  - Checks all active subscriptions and compares the latest weather data against the user's alert conditions. If conditions are met, an alert is created and a notification email is sent.

### Design Decisions and Trade-offs

- I used redis for multiple purposes: rate limiting, caching weather data, and as a message broker for Celery.

  - `Trade-off`:
        - `cons`: If Redis fails, it could impact the rate limiting, caching, and background processing systems
        - `pros`:  provides low-latency access to data, making it ideal for caching and real-time operations.

- Rate Limiting Implementation Decision:
  - i choosed  `Redis` over `SlowAPI` because

    - `Trade-off`:
      - `cons`: Redis is ideal for counting requests quickly and supports features like automatic expiration
      - `pros`:
          - added complexity of managing Redis configurations
            - I was unsure about `SlowAPI` its scalability and whether it could handle high traffic efficiently in the long term.

- Background Task Execution:
  - i choosed celery over FastAPI’s built-in background task because the  application has multiple background tasks (such as sending emails, fetching weather updates, and triggering alerts), I preferred `Celery`. It allows task execution in a separate worker process, supports distributed task execution, and provides features like retries, `scheduling`, and monitoring.

    - pros:
      - uns tasks in separate worker processes, allowing horizontal scaling across multiple servers.
        - Celery supports periodic tasks via Celery Beat, making it ideal for scheduled jobs like cron jobs.

    - cons:
      - increases complexity.
        - consume more memory and CPU.

### Future Improvements 🚀

- Divide into Microservices (weather, Alert) for Better Scalability

- Enhance Database Scalability

- Allow Users to Track Multiple Weather Conditions

- Implement a More Adaptive Rate Limiting System
  - Instead of a fixed rate limit (e.g., 60 requests/min), implement adaptive rate limiting per user

- Support More Notification Channels (SMS, Telegram/WhatsApp..)


## Tests

- Fixtures: Used for setting up test data and sessions
- Dependency Overriding: Mocking dependencies globally for all tests

- AsyncClient with ASGITransport :Used for testing FastAPI endpoints asynchronously without making real HTTP requests

- Redis Mocking
- Respx: Used for mocking HTTP requests in tests

- tests are maintained in the tests dir. To run the tests, use the following command:

  ```bach
  pytest
  ```
- to check the coverage use 

  ```bash
  python -m coverage run -m pytest
  ```
  ```bach
  coverage report
  ```

  <details>
  <summary>output</summary>

    ```cmd
      test session starts ===================================================================
  platform linux -- Python 3.10.12, pytest-8.3.4, pluggy-1.5.0
  rootdir: /home/saleem/Documents/Weather Alert System/app
  plugins: respx-0.22.0, tornasync-0.6.0.post2, anyio-4.8.0, asyncio-0.25.3, trio-0.8.0, twisted-1.14.3
  asyncio: mode=strict, asyncio_default_fixture_loop_scope=None
  collected 12 items                                                                                                                                       

  tests/integration/test_get_current_weather_router.py ..                                                                                            [ 16%]
  tests/integration/test_health_check.py ..                                                                                                          [ 33%]
  tests/integration/test_subscribe_router.py ..                                                                                                      [ 50%]
  tests/unit/test_alert_service.py ...                                                                                                               [ 75%]
  tests/unit/test_weather_service.py ...                                                                                                             [100%]

  ==================================================================== warnings summary ====================================================================
  ../malysia/lib/python3.10/site-packages/starlette/formparsers.py:12
    /home/saleem/Documents/Weather Alert System/malysia/lib/python3.10/site-packages/starlette/formparsers.py:12: PendingDeprecationWarning: Please use `import python_multipart` instead.
      import multipart

  -- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
  ============================================================= 12 passed, 1 warning in 0.21s ==============================================================

  ```
  </details>

