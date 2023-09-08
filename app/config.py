import os
import secrets
from pydantic import BaseSettings
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


class BaseConfig(BaseSettings):
    APP_NAME: str = "Booking API"
    DEBUG: bool = False
    SECRET_KEY: str = os.getenv("SECRET_KEY", default=secrets.token_hex())
    MONGO_URI: str = os.getenv("MONGO_URI")
    MONGO_DATABASE_NAME: str = os.getenv("MONGO_DATABASE_NAME")


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True
