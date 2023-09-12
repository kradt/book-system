import os
import secrets
from pydantic import BaseSettings
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


class BaseConfig(BaseSettings):
    APP_NAME: str = "Booking API"
    DEBUG: bool = False
    SECRET_KEY: str = os.getenv("SECRET_KEY", default=secrets.token_hex())
    DATABASE_URL: str = os.getenv("DATABASE_URL")


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True
