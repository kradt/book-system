from fastapi import FastAPI
from app.routes import root


app = FastAPI(title="Booking API system")

app.include_router(root.router)
