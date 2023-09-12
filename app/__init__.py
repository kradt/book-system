import databases
import sqlalchemy
from sqlalchemy.orm import create_session, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from app.config import DevelopmentConfig


config = DevelopmentConfig()

engine = create_async_engine(config.DATABASE_URL, echo=True)
# Expite on commit if true session won't use queries to already commited items
