from app.api.schemas.AbstractSchema import AbstractSchema

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
