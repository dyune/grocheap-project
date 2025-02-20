from pydantic import BaseModel, Field


class StoreModel(BaseModel):

    name: str = Field(max_length=100)


