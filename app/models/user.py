from email.policy import default
from enum import unique
from pyclbr import Class
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

    password = Column(String)

    is_banned = Column(Boolean, default=False)