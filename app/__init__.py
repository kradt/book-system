from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.config import DevelopmentConfig


config = DevelopmentConfig()
engine = create_engine(config.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)