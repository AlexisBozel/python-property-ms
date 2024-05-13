from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


class AbstractSchema(BaseModel):
    def to_json(self):
        return jsonable_encoder(self, exclude_none=True)
