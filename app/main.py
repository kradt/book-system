from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app import models, config
from app.routes import rooms


app = FastAPI(title="Booking API system")

app.include_router(rooms.router)


@app.on_event("startup")
async def startup_db_client():
    client = AsyncIOMotorClient(config.MONGO_URI)
    app.db = client
    await init_beanie(database=client[config.MONGO_DATABASE_NAME], document_models=[models.Room, models.Seat, models.Event])


@app.on_event("shutdown")
async def shutdown_db_client():
    app.db.close()
