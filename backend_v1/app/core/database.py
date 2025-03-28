# app/core/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import PostgresDsn
from app.core.config import settings

# Configure MySQL connection parameters
DATABASE_URI = f"mysql+mysqlconnector://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(
    DATABASE_URI,
    pool_size=10,                 # Maximum permanent connections
    max_overflow=20,              # Temporary connections allowed
    pool_recycle=3600,            # Recycle connections after 1 hour
    pool_pre_ping=True,           # Validate connections before use
    connect_args={
        "connect_timeout": 5      # 5 second connection timeout
    }
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

Base = declarative_base()

def get_db():
    """Dependency for FastAPI route handlers"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
