from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from app import models, config, engine
from app.routes import rooms


app = FastAPI(title="Booking API system")

app.include_router(rooms.router)


@app.on_event("startup")
async def startup_db_client():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown_db_client():
    pass
