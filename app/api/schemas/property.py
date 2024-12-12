from app.api.schemas.AbstractSchema import AbstractSchema
from app.api.schemas.pricing import PricingBase
from app.api.schemas.room import RoomBase


class PropertyInputBase(AbstractSchema):
    idOwner: int
    address: str
    terrace: bool
    surface: float
    internet: str

class PropertyOutputBase(AbstractSchema):
    idProperty: int = None
    idOwner: int
    address: str
    terrace: bool
    surface: float
    internet: str
