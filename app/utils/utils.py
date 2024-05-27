from datetime import datetime, timedelta
from math import log
from typing import Optional
from passlib.context import CryptContext
from models.user import User
from jose import jwt
from core import config
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from . import custom_exceptions
from jose.exceptions import JWTError

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def get_hashed_password(password:str)->str:
    return bcrypt_context.hash(password)

def verify_password(plainpassword:str ,password:str):
    return bcrypt_context.verify(plainpassword, password)

def authenticate_user(email:str, password:str, db)->bool:
    user =db.query(User)\
        .filter(User.email == email)\
        .first()
    
    
    if not user:
        return False
    
    if not verify_password(password, user.password):
        return False
    
    return user

def create_access_token(email:str, userId:int, expires_delta:Optional[timedelta] = None):
    encode = {
        "login": email,
        "id": userId
    }

    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)

    encode.update({"expires": expire.isoformat()})

    return jwt.encode(encode, config.SECRET_KEY, config.ALGORITHM)




oauth2_bearer = OAuth2PasswordBearer(tokenUrl = "token")


async def get_current_user(token:str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        login: str = payload.get('login')
        id: int = payload.get('id')
        if login is None or id is None:
            raise custom_exceptions.get_user_exception()
        
        return {
            "login": login,
            "id": id
        }
    
    except JWTError:
        raise custom_exceptions.get_user_exception()


