from flask import Blueprint, request, jsonify

from app.api.manager.property import (
    get_properties as retrieve_properties,
    get_property as retrieve_property_by_id
)

property_blueprint = Blueprint('property', __name__)


@property_blueprint.route('/property/<int:property_id>', methods=['GET'])
def get_property(property_id):
    property_base = retrieve_property_by_id(property_id)
    if property_base is None:
        return jsonify({'message': 'Property get failed, no property find with this id'}), 404
    return jsonify({
        'message': 'Property get successfully',
        'status': "Success",
        "result": property_base}), 201


@property_blueprint.route('/properties', methods=['GET'])
def get_properties():
    properties = retrieve_properties()
    return jsonify({
        'message': 'Properties get successfully',
        'status': 'Success',
        "result": properties}), 201