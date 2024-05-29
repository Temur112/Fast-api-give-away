from db.database import get_db
from fastapi import APIRouter, Depends
from schemas.item_schema import CreateItem
from utils import utils, custom_exceptions
from sqlalchemy.orm import Session
from models.item import Item


router = APIRouter(
    prefix  = "/products",
    tags = ["products"]
)

@router.post("/addproduct")
async def addProducts(newItem: CreateItem, user:dict = Depends(utils.get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise custom_exceptions.get_user_exception()
    
    item = Item()
    item.title = newItem.title
    item.description = newItem.description
    item.price = newItem.price

    item.is_active = True
    item.is_sold = False
    item.owner_id = user.get("id")

    db.add(item)
    db.commit()

    return item


@router.put("/update/{id}")
async def updateItemById(int: id, user: dict = Depends(utils.get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise custom_exceptions.get_user_exception()
    
    item = 