from datetime import datetime

from app.api.schemas.AbstractSchema import AbstractSchema
from app.api.schemas.property import PropertyOutputBase


class AdvertInputBase(AbstractSchema):
    idProperty: int
    title: str
    description: str
    dtAvailability: datetime


class AdvertOutputBase(AbstractSchema):
    idAdvert: int
    property: PropertyOutputBase
    title: str
    description: str
    dtCreation: datetime
    dtModification: datetime
    dtAvailability: datetime
