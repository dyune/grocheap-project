from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from backend.db.associations import *  # Ensure models are imported

# PostgreSQL Database URL
DATABASE_URL = "postgresql://postgres:pass@localhost:5433/fastapi"

# Create database engine (PostgreSQL doesn't use `connect_args`)
engine = create_engine(DATABASE_URL, echo=True)

# Create session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Initialize database
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
