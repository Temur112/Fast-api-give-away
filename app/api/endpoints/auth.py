from datetime import timedelta
from db.database import get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.user_schema import CreateUser, UpdateUserProfile
from models.user import User
from utils import utils, custom_exceptions
from fastapi.security import OAuth2PasswordRequestForm




router = APIRouter(
    prefix = "/auth",
    tags = ["auth"],
    responses = {401: {"user": "Unauthorized"}}
)

@router.post("/register")
async def register_user(user:CreateUser, db: Session = Depends(get_db)):
    newUser = User(
        user.email,
        user.username,
        user.firstname, user.lastname,
        user.phone_number,
        utils.get_hashed_password(user.password)
    )
    newUser.email = user.email
    newUser.firstname = user.firstname
    newUser.lastname = user.lastname
    newUser.username = user.username
    newUser.phone_number = user.phone_number
    newUser.password = utils.get_hashed_password(user.password)
    newUser.is_banned = False

    db.add(newUser)
    db.commit()
    db.refresh(newUser)
    
    return newUser

@router.get("/getAllUsers")
async def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = utils.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise custom_exceptions.token_exceptions()
    
    token_expires = timedelta(minutes=20)

    token = utils.create_access_token(user.email, user.id, token_expires)

    return {
        "message": "Login Successful",
        "token": token
    }

@router.put("/updateProfile")
async def update_user_profile(upUser:UpdateUserProfile, user:dict = Depends(utils.get_current_user), db: Session = Depends(get_db)):
    if not user:
        raise custom_exceptions.get_user_exception()
    
    current_user = db.query(User).filter(User.id == user.get('id')).first()

    if upUser.firstname:
        current_user.firstname = upUser.firstname
    if upUser.lastname:
        current_user.lastname = upUser.lastname
    if upUser.username:
        current_user.username = upUser.username
    if upUser.phone_number:
        current_user.phone_number = upUser.phone_number

    db.commit()
    db.refresh(current_user)
    return {
        "username": current_user.username,
        "firstname": current_user.firstname,
        "lastname": current_user.lastname,
        "phone_number": current_user.phone_number
    }

