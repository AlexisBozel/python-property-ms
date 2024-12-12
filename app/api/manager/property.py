from flask import jsonify

from app.api.schemas.property import PropertyInputBase, PropertyOutputBase
from pydantic import ValidationError

from app.api.data_access.property import (
    select_property,
    select_properties
)

def get_property(property_id):
    property_data = select_property(property_id)
    return property_base

def get_properties():
    properties_partial_data = select_properties()
    properties = []
    for property_tmp in properties_partial_data:
        properties.append(property_base)
    return properties