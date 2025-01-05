from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    hashed_password: str


class UserUpdate(BaseModel):
    username: str
    hashed_password: str


class UserPublic(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True
