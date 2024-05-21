from fastapi import FastAPI
from api.endpoints import auth
from models import user
from db.database import engine



app = FastAPI()
user.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)