
from sqlalchemy.orm import Session
from fastapi import Depends
from db.session import get_db

from module.schema.user import data
from module.provider.user import Provider
from module.register import auth_router

@auth_router.post("/users/")
def create_user(
    data: data,
    db: Session = Depends(get_db)
    ):
    
    user = Provider.created_user(db, data)
    return {"username": user.username, "email": user.email}

@auth_router.post("/token")
def login(
    data: data,
    db: Session = Depends(get_db)):
        
    return Provider.login(db, data)