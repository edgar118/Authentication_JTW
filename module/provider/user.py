
from fastapi import FastAPI, HTTPException
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
import httpx
from datetime import datetime, timedelta
import jwt
from sqlalchemy import Column, Integer, String, Sequence, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from databases import Database
from module.models.user import User
from module.schema.user import data

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Provider:

    def create_jwt_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def created_user(db, data: data):
        hashed_password = pwd_context.hash(data.password)
        user = Provider.validate_user(data.username, db)
        if not user:
            db_user = User(username=data.username, email=data.email, hashed_password=hashed_password)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)

        return db_user
    
    def validate_user(username: str, db):
        user = db.query(User).filter(User.username == username).first()
        if user:
            raise HTTPException(
                status_code=401,
                detail="Usuario Creado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user
    
    def authenticate_user(username: str, password: str, db):
        user = db.query(User).filter(User.username == username).first()
        if not user or not pwd_context.verify(password, user.hashed_password):
            return None
        return user
    
    def login(db, data: data):
        
        user = Provider.authenticate_user(
            data.username,
            data.password,
            db
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = Provider.create_jwt_token(
            data={"sub": data.username}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}