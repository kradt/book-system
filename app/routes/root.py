from fastapi import APIRouter


router = APIRouter(prefix="/auth")


@router.get("/")
def index_auth():
    return {"message": "hello world"}
