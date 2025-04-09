import os
from typing import Annotated, Generator
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from backend.db.models import Base, Item, Store

# Load environment variables
load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_DATABASE")

print(user, password, host, port, database)

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, connect_args={"connect_timeout": 5})

# Create a configured "SessionLocal" class
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db() -> None:
    # Print the tables for debugging purposes
    print(Base.metadata.tables.items())
    # Create all tables defined in the metadata
    Base.metadata.create_all(engine)
    print("Database initialized successfully")


# Dependency to get a session for FastAPI routes
def get_session() -> Generator[Session, None, None]:
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Annotated dependency for FastAPI routes
SessionDep = Annotated[Session, Depends(get_session)]
