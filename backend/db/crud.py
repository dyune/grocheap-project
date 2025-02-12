from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import NoResultFound
from sqlalchemy.future import select
from sqlmodel import Session
from backend.db.models import Item, User, Store
from backend.db.session import get_session
from backend.schemas.items import ItemCreate
from backend.schemas.users import UserCreate, UserPublic, UserUpdatePassword, PrivateUserOut
from backend.schemas.stores import StoreModel
from backend.utils import hash

SessionDep = Annotated[Session, Depends(get_session)]
AuthenticationDep = None

router = APIRouter(
    prefix="/database"
)


def save(item, session: SessionDep):
    session.add(item)
    session.commit()
    session.refresh(item)


@router.get("/get/store/{name}")
async def get_store(name: str, session: SessionDep) -> Store:
    try:
        result = session.execute(select(Store).where(Store.name == name))
        store = result.scalar_one()
        return store
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Store not found")


@router.get("/get/item-query/")
async def get_item_by_query(identifier: int, session: SessionDep) -> Item | None:
    result = session.execute(select(Item).where(Item.id == identifier))
    return result.scalar_one_or_none()


@router.get("/get/items")
async def get_items(session: SessionDep) -> Sequence[Item]:
    result = session.execute(select(Item))
    return result.scalars().all()


@router.get("/get/user/{email}")
async def get_user_by_email(email: str, session: SessionDep) -> User | None:
    result = session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


@router.get("/get/users")
async def get_users(session: SessionDep) -> Sequence[User]:
    result = session.execute(select(User))
    return result.scalars().all()


@router.post("/create/user")
async def create_user(user: UserCreate, session: SessionDep) -> UserPublic:
    try:
        db_user = User.model_validate(user)
        db_user.hashed_password = hash.hash_password(db_user.hashed_password)
        save(db_user, session)
        return UserPublic.model_validate(db_user)

    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid input detected.")


@router.post("/create/store/{name}")
async def create_store(store: StoreModel, session: SessionDep) -> Store:
    try:
        db_store = Store.model_validate(store)
        save(db_store, session)
        return db_store

    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid input detected.")


@router.put("/update/user")
async def update_user_password(data: UserUpdatePassword, session: SessionDep) -> User:
    user = await get_user_by_email(data.email, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not hash.verify_password(data.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    user.hashed_password = hash.hash_password(data.new_password)
    save(user, session)
    return user


@router.delete("/delete/user/{email}")
async def delete_user(email: str, session: SessionDep):
    user = await get_user_by_email(email, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()
    return {"message": f"User {email} deleted successfully"}