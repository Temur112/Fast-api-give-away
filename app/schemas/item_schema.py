from typing import List
from email.policy import default
from typing import Optional
from pydantic import BaseModel, Field


class ImageBase(BaseModel):
    url: str

class ImageCreate(ImageBase):
    pass

class Image(ImageBase):
    id: int
    item_id: int

    class Config:
        orm_mode = True


class CreateItem(BaseModel):

    title: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=10, max_length=255)
    price: float = Field()
    images: List[Image] = []

class Item(BaseModel):
    id: int
    title: str = Field(min_length=3, max_length=255)
    description: str = Field(min_length=10, max_length=255)
    price: float = Field(min_length=3, max_length=255)
    is_active:bool = Field(default= True)
    is_sold: bool = Field(default = False)



