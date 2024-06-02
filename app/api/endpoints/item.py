from ast import List
from db.database import get_db
from fastapi import APIRouter, Depends
from schemas.item_schema import CreateItem, Item
from utils import utils, custom_exceptions
from sqlalchemy.orm import Session
from models.item import Item


router = APIRouter(
    prefix  = "/products",
    tags = ["products"]
)

@router.get("/getall")
async def get_all_products(db: Session = Depends(get_db)):
    items =  db.query(Item).all()
    return [utils.item_to_dict(item) for item in items]


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
    db.refresh(item)

    return item


@router.put("/update/{id}")
async def updateItemById(id: int, 
                        newItem: CreateItem, 
                        user: dict = Depends(utils.get_current_user), 
                        db: Session = Depends(get_db)):
    
    if user is None:
        raise custom_exceptions.get_user_exception()
    
    item = db.query(Item)\
        .filter(Item.id == id)\
        .filter(Item.owner_id == user.get("id"))\
        .first()
    
    if item is None:
        raise custom_exceptions.http_exception()
    
    item.title = newItem.title
    item.description = newItem.description
    item.price = newItem.price

    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("/getproduct/{id}")
async def getproduct_by_id(id: int, db: Session = Depends(get_db)):
    return db.query(Item).filter(Item.id == id).first()

@router.get("/myproducts")
async def get_users_products(user: dict = Depends(utils.get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise custom_exceptions.get_user_exception()
    
    resultset = db.query(Item).filter(Item.owner_id == user.get("id")).all()

    if resultset is None:
        return custom_exceptions.http_exception()



    return [utils.item_to_dict(item) for item in resultset]

@router.delete("/deleteproduct/{id}")
async def delete_product_by_id(id: int, user: dict = Depends(utils.get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise custom_exceptions.get_user_exception()
    
    item = db.query(Item)\
        .filter(Item.id == id)\
        .filter(Item.owner_id == user.get("id")).first()
    
    if item is None:
        return custom_exceptions.http_exception()
    
    db.delete(item)
    db.commit()
    
    return custom_exceptions.custom_response(200, "Successfull")