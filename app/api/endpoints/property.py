from flask import Blueprint, request, jsonify

from app.api.schemas.pricing import PricingBase
from app.dependencies import get_db
from app.api.schemas.property import PropertyInputBase, PropertyOutputBase
from pydantic import ValidationError
from app.api.data_access.room import select_room_by_id, insert_room, update_room_by_id_by_type, del_room_by_id
from app.api.data_access.pricing import select_pricing_by_id, insert_pricing, update_pricing_by_id, del_pricing_by_id

from app.api.data_access.property import select_property_by_id, select_properties, insert_property, \
    update_property_by_id, del_property_by_id

property_blueprint = Blueprint('property', __name__)


def get_full_data_from_property(property_data):
    db = get_db()
    cursor = db.cursor()

    property_id = property_data.get("idProperty")
    rooms = select_room_by_id(property_id)

    pricing_id = property_data.get("idPricing")
    pricing = select_pricing_by_id(pricing_id)

    try:
        pricing = PricingBase(**pricing)
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
        return jsonify({"status": "error", "stack": missing}), 400
    return property_base


@property_blueprint.route('/property/<int:property_id>', methods=['GET'])
def getPropertyById(property_id):
    property_data = select_property_by_id(property_id)

    property_base = get_full_data_from_property(property_data)

    if property_base is None:
        return jsonify({'message': 'Property get failed, no property find with this id'}), 404

    return jsonify({
        'message': 'Property get successfully',
        "result": property_base.dict()}), 201


@property_blueprint.route('/properties', methods=['GET'])
def getProperties():
    properties_partial_info = select_properties()

    properties = []
    for property_tmp in properties_partial_info:
        property_base = get_full_data_from_property(property_tmp)
        properties.append(property_base.dict())

    return jsonify({
        'message': 'Properties get successfully',
        "result": properties}), 201


@property_blueprint.route('/property', methods=['POST'])
def postProperty():
    data = request.get_json()

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

    return jsonify({'message': 'Property registered successfully'}), 201


@property_blueprint.route('/property/<int:property_id>', methods=['PUT'])
def putProperty(property_id):
    data = request.get_json()

    property_data = select_property_by_id(property_id)
    pricing_id = property_data.get("idPricing")

    keys = ["idOwner", "address", "terrace", "surface", "internet"]

    for key in keys:
        if data.get(key):
            value = data.get(key)
            update_property_by_id(property_id, key, value)

    if data.get("pricing"):
        keys = ["charge", "price"]

        for key in keys:
            if data.get(key):
                value = data.get(key)
                update_pricing_by_id(pricing_id, key, value)

    if data.get("rooms"):
        for room_data in data["rooms"]:
            value_type = room_data.get("type")
            value_number = room_data.get("number")
            if value_type and value_number:
                update_room_by_id_by_type(property_id, value_type, value_number)

    return jsonify({'message': 'Property update successfully'}), 201


@property_blueprint.route('/property/<int:property_id>', methods=['DELETE'])
def deletePropertyById(property_id):
    property_data = select_property_by_id(property_id)
    pricing_id = property_data.get("idPricing")

    del_room_by_id(property_id)
    del_property_by_id(property_id)
    del_pricing_by_id(pricing_id)

    return jsonify({'message': 'Property delete successfully'}), 201
