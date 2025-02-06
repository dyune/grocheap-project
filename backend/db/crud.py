from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import NoResultFound
from sqlmodel import Session, select
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
        store = session.exec(select(Store).where(Store.name == name)).one()
        return store
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Store not found")


@router.get("/get/item-query/")
async def get_item_by_query(identifier: int, session: SessionDep) -> Item | None:
    return session.exec(select(Item).where(Item.id == identifier)).first()


@router.get("/get/items")
async def get_items(session: SessionDep) -> Sequence[Item]:
    return session.exec(select(Item)).all()


@router.get("/get/user/{email}")
async def get_user_by_email(email: str, session: SessionDep) -> User | None:
    return session.exec(select(User).where(User.email == email)).first()


@router.get("/get/users")
async def get_users(session: SessionDep) -> Sequence[User]:
    return session.exec(select(User)).all()


# TODO: Delete this endpoint, the scraper will handle creation logic for *items*
@router.post("/create/item")
async def create_item(item: ItemCreate, session: SessionDep) -> Item:
    try:
        db_item = Item(
            name=item.name,
            brand=item.brand,
            link=item.link,
            image_url=item.image_url,
            size=item.size,
            store_id=item.store_id,
            price=item.price
        )

        session.add(db_item)  # Error happens here
        session.commit()
        session.refresh(db_item)
        return db_item

    except Exception as e:
        print(f"Error type: {type(e)}")
        print(f"Error message: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


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
        return db_store  # Return db_store instead of store

    except ValidationError:
        raise HTTPException(status_code=400, detail="Invalid input detected.")


@router.put("/update/item/{identifier}")
async def update_item(identifier: int, price: float, session: SessionDep) -> Item:
    item = await get_item_by_query(identifier, session)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.price = price
    save(item, session)
    return item


@router.put("/update/user")
async def update_user_password(data: UserUpdatePassword, session: SessionDep) -> User:
    # NEEDED TO AWAIT THE ASYNC FUNCTION, NOT THE DB QUERY INSIDE THE FUNCTION
    user = await get_user_by_email(data.email, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not hash.verify_password(data.old_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    user.hashed_password = hash.hash_password(data.new_password)  # Added new_password field
    save(user, session)
    return user


@router.put("/update/store/{store_name}")
async def update_store(store_name: str, store: StoreModel, session: SessionDep) -> Store:
    try:
        db_store = await get_store(store_name, session)
        for key, value in store.model_dump(exclude_unset=True).items():
            setattr(db_store, key, value)
        save(db_store, session)
        return db_store

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Store not found")


@router.delete("/delete/item/{identifier}")
async def delete_item(identifier: int, session: SessionDep):
    item = await get_item_by_query(identifier, session)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    session.delete(item)
    session.commit()
    return {"message": f"Item {identifier} deleted successfully"}


@router.delete("/delete/user/{email}")
async def delete_user(email: str, session: SessionDep):
    user = await get_user_by_email(email, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    session.delete(user)
    session.commit()
    return {"message": f"User {email} deleted successfully"}
