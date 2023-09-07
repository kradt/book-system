from fastapi import APIRouter


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/")
def index_auth():
    return {"message": "hello world"}
