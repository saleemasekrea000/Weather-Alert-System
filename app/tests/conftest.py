from collections import namedtuple

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.database import Base
from src.dependencies import get_cache_redis, get_db, rate_limit
from src.main import app
from src.settings import base_settings


@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine(
        f"postgresql://{base_settings.postgres_username}:{base_settings.postgres_password}@"
        f"{base_settings.postgres_host}:{base_settings.postgres_port}/{base_settings.test_postgres_db}",
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    TestSession = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestSession(bind=connection)

    yield session

    # this make sure that the database is empty before the next test starts.
    session.rollback()  # Undo all changes
    connection.close()


@pytest.fixture
def subscription_data():
    return {
        "email": "saleemasekrea000@gmail.com",
        "city": "New York",
        "condition_thresholds": {
            "temperature": 70,
        },
    }


@pytest.fixture
def client():
    return TestClient(app)


# https://fastapi.tiangolo.com/advanced/testing-dependencies/#use-the-appdependency_overrides-attribute
# Mock dependencies for the tests

"""autouse : True means that this fixture will be automatically used by all tests
 wthiout the need to explicitly pass it as an argument to the test function.
 """


@pytest.fixture(autouse=True)
def override_dependencies():
    def mock_get_db():
        return "mock_db_session"

    def mock_get_cache_redis():
        return "mock_redis_cache"

    def mock_rate_limit():
        return True

    # Override dependencies globally for all tests in this file
    app.dependency_overrides[get_db] = mock_get_db
    app.dependency_overrides[get_cache_redis] = mock_get_cache_redis
    app.dependency_overrides[rate_limit] = mock_rate_limit

    yield

    app.dependency_overrides.clear()
