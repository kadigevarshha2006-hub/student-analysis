import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from backend.config import get_settings

settings = get_settings()

def create_resilient_engine():
    """Attempts database connection, gracefully falling back to SQLite if primary DB is offline."""
    db_url = settings.DATABASE_URL
    if db_url.startswith("sqlite"):
        return create_engine(db_url, connect_args={"check_same_thread": False})
    
    try:
        engine = create_engine(db_url, pool_pre_ping=True)
        # Test connection
        with engine.connect() as conn:
            pass
        return engine
    except Exception as e:
        print(f"Primary database ({db_url}) unavailable ({e}). Gracefully falling back to local SQLite database.")
        sqlite_url = "sqlite:///./resume_ai.db"
        return create_engine(sqlite_url, connect_args={"check_same_thread": False})

engine = create_resilient_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """FastAPI Dependency for database session management."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Creates database tables if they do not exist."""
    import backend.models  # noqa
    Base.metadata.create_all(bind=engine)
