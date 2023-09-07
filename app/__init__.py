from motor.motor_asyncio import AsyncIOMotorClient
from beanie import Document, Indexed, init_beanie

from app.config import DevelopmentConfig


config = DevelopmentConfig()
