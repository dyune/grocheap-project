from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.db.associations import *  # Ensure models are imported
import os

user = os.environ["DB_USER"]
password = os.environ["DB_PASS"]
host = os.environ["DB_HOST"]
port = os.environ["DB_PORT"]
database = os.environ["DB_NAME"]

DATABASE_URL = f"postgresql://{user}:{password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL, echo=True)

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
