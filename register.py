from fastapi import APIRouter
from module.register import auth_router

api_router = APIRouter()
api_router.include_router(auth_router)
