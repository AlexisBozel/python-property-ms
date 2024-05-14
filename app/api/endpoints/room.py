from flask import Blueprint, request, jsonify

from app.api.manager.room import (
    get_room as retrieve_room,
    post_room as create_room,
    put_room as update_room,
    delete_room_by_type as remove_room_by_type,
    delete_room as remove_room
)

room_blueprint = Blueprint('room', __name__)


@room_blueprint.route('/room/<int:property_id>', methods=['GET'])
def get_room(property_id):
    rooms = retrieve_room(property_id)
    if rooms is None:
        return jsonify({'message': 'Room get failed, no room find with this id'}), 404
    return jsonify({
        'message': 'Room get successfully',
        'status': 'Success',
        "result": rooms}), 201


@room_blueprint.route('/room/<int:property_id>', methods=['POST'])
def post_room(property_id):
    data = request.get_json()
    create_room(property_id, data)
    return jsonify({
        'message': 'Room post successfully',
        'status': 'Success'}), 201


@room_blueprint.route('/room/<int:property_id>', methods=['PUT'])
def put_room(property_id):
    # can update only the number attribute
    data = request.get_json()
    update_room(property_id, data)
    return jsonify({
        'message': 'Room put successfully',
        'status': 'Success'}), 201


@room_blueprint.route('/room/<int:property_id>', methods=['DELETE'])
def delete_room(property_id):
    # can delete only the type attribute row
    if request.headers.get("Content-Type") is None:
        remove_room(property_id)
    else:
        data = request.get_json()
        remove_room_by_type(property_id, data)
    return jsonify({
        'message': 'Room delete successfully',
        'status': 'Success'}), 201
