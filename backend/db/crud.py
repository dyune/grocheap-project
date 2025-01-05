from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from .models import Item, User, Store
from .session import get_session
from ..schemas.items import ItemCreate
from ..schemas.users import UserCreate, UserPublic, UserUpdate
from ..schemas.stores import StoreModel

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
async def get_store(name: str, session: SessionDep):
    store = session.exec(select(Store).where(Store.name == name))
    return store


@router.get("/get/item-query/")
async def get_item_by_query(identifier: int, session: SessionDep):
    item = session.exec(select(Item).where(Item.id == identifier)).first()
    return item


@router.get("/get/items")
async def get_items(session: SessionDep):
    items = session.exec(select(Item)).all()
    return items


@router.get("/get/user/{email}")
async def get_user_by_email(email: str, session: SessionDep):
    user = session.exec(select(User).where(User.email == email)).first()
    return user


@router.get("/get/users")
async def get_users(session: SessionDep):
    return session.exec(select(User)).all()


@router.post("/create/item")
async def create_item(item: ItemCreate, session: SessionDep):
    try:
        db_item = Item.model_validate(item)
        save(db_item, session)
        return item

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid input detected.")


@router.post("/create/user")
async def create_user(user: UserCreate, session: SessionDep):
    try:
        db_user = User.model_validate(user)
        save(db_user, session)
        public_user = UserPublic.model_validate(db_user)
        return public_user

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid input detected.")


@router.post("/create/store/{name}")
async def create_store(store: StoreModel, session: SessionDep):
    try:
        db_store = Store.model_validate(store)
        save(db_store, session)
        return store

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid input detected.")


@router.put("/update/item/{id}")
async def update_item(identifier: int, session: SessionDep, price: float):
    item = get_item_by_query(identifier, session)
    if item is None:
        return None
    else:
        item.price = price
        save(item, session)
        return item


@router.put("/update/user/{email}")
async def update_user_email(email: str, new_email: str, session: SessionDep):
    user = get_user_by_email(email, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    else:
        user.email = new_email
        save(user, session)


@router.put("/update/user/{password}")
async def update_user_password(password: str, new_password: str, session: SessionDep):
    pass


@router.put("/update/store/{id}")
async def update_store(store: StoreModel, session: SessionDep):
    pass


@router.delete("/delete/item/{id}")
async def delete_item(identifier: int, session: SessionDep):
    item = get_item_by_query(identifier, session)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found.")
    else:
        session.delete(item)
        session.commit()
        print(f"Item deleted: {item}")


@router.delete("/delete/user/{id}")
async def delete_user(email: str, session: SessionDep):
    user = get_user_by_email(email, session)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    else:
        session.delete(user)
        session.commit()
        print(f"Deleted user: {user}")


@router.delete("/delete/store/{id}")
async def delete_store(store: StoreModel, session: SessionDep):
    store = get_store(store, session)
    if store is None:
        raise HTTPException(status_code=404, detail="Store not found.")
    else:
        session.delete(store)
        session.commit()
        print(f"Deleted store: {store}")
