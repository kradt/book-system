from beanie import Document, Indexed, init_beanie
from bson import ObjectId
from app.schemas.rooms import Place
from app.tools import PyObjectId


class Room(Document):
    id: PyObjectId
    name: str | None = None
    columns: int
    rows: int
    places: list[Place] | None = None

    def __init__(
            self,
            *args,
            columns: int,
            rows: int,
            name: str | None = None,
            places: list[Place] | None = None,
            **kwargs):
        
        if places is None:
            places = []
            for row in range(rows):
                for col in range(columns):
                    new_place = Place(column=col, row=row)
                    places.append(new_place)

        super().__init__(*args, name=name, columns=columns, rows=rows, places=places, **kwargs)

