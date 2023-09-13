from fastapi import FastAPI

from app import models, config, engine
from app.routes import rooms


app = FastAPI(title="Booking API system")

app.include_router(rooms.router)


@app.on_event("startup")
def startup_db_client():
    models.Base.metadata.create_all(bind=engine)


@app.on_event("shutdown")
def shutdown_db_client():
    pass
    
