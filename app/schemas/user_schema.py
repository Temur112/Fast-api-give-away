from typing import Optional
from pydantic import BaseModel



class CreateUser(BaseModel):
    username: str
    email: str
    firstname: str
    lastname: Optional[str]
    phone_number :str | None
    password: str


class UpdateUserProfile(BaseModel):
    username: Optional[str] = None
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    phone_number: Optional[str] = None
