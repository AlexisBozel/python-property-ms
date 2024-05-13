from app.api.schemas.AbstractSchema import AbstractSchema


class RoomBase(AbstractSchema):
    type: str
    number: int
