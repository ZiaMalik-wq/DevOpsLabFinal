"""
Database configuration — Supabase (PostgreSQL) via SQLAlchemy.
Connection URL is loaded from the .env file.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        "DATABASE_URL is not set. "
        "Please configure it in environment variables or backend/.env with your PostgreSQL connection string."
    )

# SQLAlchemy engine — no check_same_thread needed for PostgreSQL
engine = create_engine(
    DATABASE_URL,
    echo=False,
    # Connection pool settings suited for Supabase's connection limits
    pool_pre_ping=True,       # Detect stale connections automatically
    pool_size=5,              # Keep up to 5 open connections
    max_overflow=10,          # Allow up to 10 extra connections under load
    pool_recycle=1800,        # Recycle connections every 30 minutes
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    """FastAPI dependency — yields a DB session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all tables in the Supabase PostgreSQL database."""
    Base.metadata.create_all(bind=engine)
