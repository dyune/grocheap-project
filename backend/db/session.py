import os

from sqlalchemy import create_engine

from .associations import *

# Local development DB PATH
FILE_NAME = os.path.join("/Users/davidwang/PycharmProjects/grocheap-dev-project/backend/", "grocery_items_data.db")
# When deployed on container
# FILE_NAME = "grocery_items_data.db"

DATABASE_URL = f"sqlite:///{FILE_NAME}"
connection_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, connect_args=connection_args, echo=True)
print(FILE_NAME)


def init_db():
    print(SQLModel.metadata)
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


