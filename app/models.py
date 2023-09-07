from beanie import Document, Indexed, init_beanie
from app.schemas.rooms import Place


class Room(Document):
    name: str | None = None
    columns: int
    rows: int
    places: list[Place] | None = None

    def __init__(
            self,
            columns: int,
            rows: int,
            name: str | None = None,
            places: list[Place] | None = None):
        
        if places is None:
            places = []
            for row in range(rows):
                for col in range(columns):
                    new_place = Place(column=col, row=row)
                    places.append(new_place)

        super().__init__(name=name, columns=columns, rows=rows, places=places)

