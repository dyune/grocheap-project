import os
from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel.main import SQLModel
from backend.db.models import Item, Store
from dotenv import load_dotenv
loaded = load_dotenv()

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
port = os.getenv("DB_PORT")
database = os.getenv("DB_DATABASE")

print(user, password, host, port, database)

DATABASE_URL = (
    f"postgresql://{user}:{password}@{host}:{port}/{database}"
)

engine = create_engine(DATABASE_URL, connect_args={"connect_timeout": 5})

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db():
    print(SQLModel.metadata.tables.items())
    SQLModel.metadata.create_all(engine)
    print("Database initialized successfully")


# Dependency to get a session
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Annotated dependency for FastAPI routes
SessionDep = Annotated[Session, Depends(get_session)]
