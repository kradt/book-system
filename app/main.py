from fastapi import FastAPI
from app.routes import root, rooms


app = FastAPI(title="Booking API system")

app.include_router(root.router)
app.include_router(rooms.router)