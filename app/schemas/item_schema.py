from dataclasses import Field
from typing import Optional
from pydantic import BaseModel


class CreateItem(BaseModel):

    title: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=10, max_length=255)
    price: float = Field(..., min_length=3, max_length=255)
    