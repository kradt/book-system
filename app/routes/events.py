from fastapi import APIRouter, Depends
from typing import Annotated


router = APIRouter(tags=["events"])


@router.delete("/events/{event_id}", status_code=204)
def delete_event_by_id(event: Annotated[Event, Depends(get_event_by_id)]):
    pass


@router.post("/events/", status_code=201, response_model=Event)
def create_event(event: Event):
    pass


@router.get("/events/{event_id}", status_code=200, response_model=Event)
def get_specific_event_by_id(event: Annotated[Event, Depends(get_event_by_id)]):
    pass


@router.get("/events/", status_code=200, response_model=list[Event])
def get_all_event():
    pass