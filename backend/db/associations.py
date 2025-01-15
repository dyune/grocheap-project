from typing import Annotated
from sqlmodel import Field, SQLModel, Session, select
from fastapi import APIRouter, Depends
from .session import get_session
# from .crud import get_user_by_email, get_item_by_query

SessionDep = Annotated[Session, Depends(get_session)]


router = APIRouter(
    prefix="/associations",
)


class UserToItemAssociation(SQLModel, table=True):
    # Association table defines User -> Item associations
    __tablename__ = "user_to_items"

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    item_id: int = Field(foreign_key="items.id", primary_key=True)


def save(item, session: SessionDep):
    session.add(item)
    session.commit()
    session.refresh(item)


# TODO: Ensure validity of inputs, a user and item must both exist
@router.get("/associations")
async def get_associations(session: SessionDep):
    all_associations = session.exec(select(UserToItemAssociation)).all()
    return all_associations


@router.post("/create/association")
async def create_association(user_id: int, item_id: int, session: SessionDep):
    new_association = UserToItemAssociation(user_id=user_id, item_id=item_id)
    save(new_association, session)
    return new_association
