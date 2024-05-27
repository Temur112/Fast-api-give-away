from enum import unique
from sqlalchemy import Boolean, String, ForeignKey, Integer, Column
from db.database import Base
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, index=True)

    firstname = Column(String)
    lastname = Column(String)
    phone_number = Column(String)

    password = Column(String)

    is_banned = Column(Boolean, default=False)


    def __init__(self, email: str, username: str, firstname: str, lastname: str, phone_number: str | None, password:str):
        self.email = email
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        if phone_number:
            self.phone_number = phone_number
        self.password = password
