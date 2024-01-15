from fastapi import FastAPI
from register import api_router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("Running default data version scripts")

app.include_router(api_router)