from typing import Annotated, Sequence

from fastapi import APIRouter, Depends
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from .models import *

FILE_NAME = "grocery_items_data.db"
DATABASE_URL = f"sqlite:///{FILE_NAME}"
connection_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, connect_args=connection_args, echo=True)


def init_db():
    print(SQLModel.metadata.tables.keys())
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine, tables=[Store.__table__, Item.__table__])


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


