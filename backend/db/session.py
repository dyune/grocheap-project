from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlmodel.main import SQLModel

user = "postgres"
password = "wyqtun-wubgic-0sAhca"
host = "grocheap-1-instance-1.c3ees26qorwp.ca-central-1.rds.amazonaws.com"
port = "5432"
database = "postgres"

DATABASE_URL = (
    f"postgresql://{user}:{password}@{host}:{port}/{database}"
    "?sslmode=disable&gssencmode=disable"
)

engine = create_engine(DATABASE_URL, connect_args={"connect_timeout": 5})

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db():
    print(SQLModel.metadata)
    SQLModel.metadata.create_all(engine)


# Dependency to get a session
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Annotated dependency for FastAPI routes
SessionDep = Annotated[Session, Depends(get_session)]
