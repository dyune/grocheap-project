from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    email: str
    hashed_password: str


class UserUpdatePassword(BaseModel):
    email: str
    new_password: str
    old_password: str


class UserPublic(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True


class PrivateUserOut(BaseModel):
    username: str
    email: str
    hashed_password: str

    class Config:
        from_attributes = True

