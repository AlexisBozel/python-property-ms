from flask import jsonify

from app.api.schemas.pricing import PricingBase
from app.api.schemas.property import PropertyInputBase, PropertyOutputBase
from pydantic import ValidationError

from app.api.data_access.room import (
    select_room,
    insert_room,
    update_room_by_type,
    delete_room
)

from app.api.data_access.pricing import (
    select_pricing,
    insert_pricing,
    update_pricing,
    delete_pricing
)

from app.api.data_access.property import (
    select_property,
    select_properties,
    insert_property,
    update_property,
    delete_property as remove_property
)


def get_full_data_from_property(property_data):
    property_id = property_data.get("idProperty")
    rooms = select_room(property_id)
    print(rooms)
    pricing_id = property_data.get("idPricing")
    pricing = select_pricing(pricing_id)

    try:
        pricing = PricingBase(**pricing)
        print(pricing)
        property_base = PropertyOutputBase(
            idProperty=property_id,
            idOwner=property_data.get("idOwner"),
            address=property_data.get("address"),
            surface=property_data.get("surface"),
            terrace=property_data.get("terrace"),
            internet=property_data.get("internet"),
            rooms=rooms,
            pricing=pricing
        )
    except ValidationError as e:
        missing = [{"field": _["loc"][-1], "errorType": _["type"]} for _ in e.errors()]
        print(missing)
        return jsonify({"status": "error", "stack": missing}), 400
    return property_base.dict()


def get_property(property_id):
    property_data = select_property(property_id)
    property_base = get_full_data_from_property(property_data)
    return property_base


def get_properties():
    properties_partial_data = select_properties()
    properties = []
    for property_tmp in properties_partial_data:
        property_base = get_full_data_from_property(property_tmp)
        print(property_base)
        properties.append(property_base)
    return properties


def post_property(data):
    try:
        property_base = PropertyInputBase(**data)
        pricing = property_base.pricing
    except ValidationError as e:
        missing = [{"field": _["loc"][-1], "errorType": _["type"]} for _ in e.errors()]
        return jsonify({"status": "error", "stack": missing}), 400

    pricing_id = insert_pricing(pricing)

    property_id = insert_property(property_base, pricing_id)

    for room in property_base.rooms:
        insert_room(room, property_id)


def put_property(property_id, data):
    property_data = select_property(property_id)
    print(property_data)
    pricing_id = property_data["idPricing"]

    keys = ["idOwner", "address", "terrace", "surface", "internet"]

    for key in keys:
        if data.get(key):
            value = data.get(key)
            update_property(property_id, key, value)

    if data.get("pricing"):
        keys = ["charge", "price"]

        for key in keys:
            if data.get(key):
                value = data.get(key)
                update_pricing(pricing_id, key, value)

    if data.get("rooms"):
        for room_data in data["rooms"]:
            value_type = room_data.get("type")
            value_number = room_data.get("number")
            if value_type and value_number:
                update_room_by_type(property_id, value_type, value_number)


def delete_property(property_id):
    property_data = select_property(property_id)
    pricing_id = property_data.get("idPricing")

    delete_room(property_id)
    remove_property(property_id)
    delete_pricing(pricing_id)
