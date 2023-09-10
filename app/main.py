from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app import config
from app.routes import rooms
from app.models import Room, Seat, Event


app = FastAPI(title="Booking API system")

app.include_router(rooms.router)


@app.on_event("startup")
async def startup():
    client = AsyncIOMotorClient(config.MONGO_URI)
    await init_beanie(database=client[config.MONGO_DATABASE_NAME], document_models=[Room, Seat, Event])
