from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

python_path = os.getenv('PYTHONPATH')

SQLALCHEMY_DATABASE_URL = f"sqlite:///{python_path}/db.sqlite3"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# return database session class, we can create session instance to be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@contextmanager
def get_db_session():
    try:
        db = SessionLocal()
        yield db
        db.close()
    except Exception:
        db.rollback()
        raise
