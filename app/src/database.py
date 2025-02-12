from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from src.settings import base_settings

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{base_settings.postgres_username}:{base_settings.postgres_password}@"
    f"{base_settings.postgres_host}:{base_settings.postgres_port}/{base_settings.postgres_db}"
)

# Create an engine that manages the connection to the PostgreSQL database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

"""Create a session factory (SessionLocal) for handling transactions with the database
 - autocommit=False: Changes must be committed manually
 - autoflush=False: Prevents automatic flushing (writing) of changes before each query
 - bind=engine: Connects the session to the specified database engine
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for SQLAlchemy models, inherited by all ORM models
Base = declarative_base()
