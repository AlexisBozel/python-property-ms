from flask import Blueprint, request, jsonify

from app.api.manager.property import (
    get_properties as retrieve_properties,
    get_property as retrieve_property_by_id,
    post_property as create_property,
    put_property as update_property,
    delete_property as remove_property
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


@property_blueprint.route('/property', methods=['POST'])
def post_property():
    data = request.get_json()
    create_property(data)
    return jsonify({
        'message': 'Property registered successfully',
        'status': 'Success'}), 201


@property_blueprint.route('/property/<int:property_id>', methods=['PUT'])
def put_property(property_id):
    data = request.get_json()
    update_property(property_id, data)
    return jsonify({
        'message': 'Property update successfully',
        'status': 'Success'}), 201


@property_blueprint.route('/property/<int:property_id>', methods=['DELETE'])
def delete_property(property_id):
    remove_property(property_id)
    return jsonify({
        'message': 'Property delete successfully',
        'status': 'Success'}), 201
