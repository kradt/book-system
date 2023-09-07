from fastapi import APIRouter


router = APIRouter(name="Auth of booking system", prefix="/auth")


@router.get("/")
def index_auth():
    return {"message": "hello world"}
