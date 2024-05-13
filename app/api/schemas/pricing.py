from app.api.schemas.AbstractSchema import AbstractSchema


class PricingBase(AbstractSchema):
    charge: float
    price: float

