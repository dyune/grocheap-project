from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """
    Max email len should be 254
    Username max len arbitrarily defined
    Password max len not defined, set by hashing algorithm
    """
    username: str = Field(max_length=50)

    email: str = Field(max_length=254)

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

