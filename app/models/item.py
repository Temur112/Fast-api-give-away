from models.user import User
from db.database import Base
from sqlalchemy import Boolean, String, Integer, Column, Float, ForeignKey
from sqlalchemy.orm import relationship



class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index = True)

    description = Column(String)
    price = Column(Float)
    is_sold = Column(Boolean, default = False)
    is_active = Column(Boolean, default = True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates='products')