from flask import Blueprint, request, jsonify
from app.api.schemas.room import RoomBase
from pydantic import ValidationError
from app.api.data_access.room import select_room_by_id, insert_room, select_room_by_id_by_type, \
    update_room_by_id_by_type, del_room_by_id_by_type, del_room_by_id

room_blueprint = Blueprint('room', __name__)


@room_blueprint.route('/room/<int:property_id>', methods=['GET'])
def get_room_by_id(property_id):
    rooms = select_room_by_id(property_id)

    if rooms is None:
        return jsonify({'message': 'Room get failed, no room find with this id'}), 404

    return jsonify({
        'message': 'Room get successfully',
        "result": rooms}), 201


@room_blueprint.route('/room/<int:property_id>', methods=['POST'])
def post_room(property_id):
    data = request.get_json()

    list_room = []
    for room_tmp in data["rooms"]:
        try:
            print(room_tmp)
            room = RoomBase(**room_tmp)

            # check if type exist
            rooms = select_room_by_id_by_type(property_id, room.type)

            if rooms is None:
                list_room.append(room)
        except ValidationError as e:
            missing = [{"field": _["loc"][-1], "errorType": _["type"]} for _ in e.errors()]
            return jsonify({"status": "error", "stack": missing}), 400

    if len(list_room) == 0:
        return jsonify({'message': 'Room post failed, can not add an existing type'}), 400

    for room in list_room:
        insert_room(room, property_id)

    return jsonify({'message': 'Room post successfully'}), 201


@room_blueprint.route('/room/<int:property_id>', methods=['PUT'])
def put_room_by_id(property_id):
    # can update only the number attribute
    data = request.get_json()

    for room_data in data["rooms"]:
        value_type = room_data.get("type")
        value_number = room_data.get("number")
        if value_type and value_number:
            update_room_by_id_by_type(property_id, value_type, value_number)

    return jsonify({'message': 'Room put successfully'}), 201


@room_blueprint.route('/room/<int:property_id>', methods=['DELETE'])
def partial_delete_room_by_id(property_id):
    # can delete only the type attribute row
    data = request.get_json()
    room_type = data.get("type")

    del_room_by_id_by_type(property_id, room_type)

    return jsonify({'message': 'Room delete successfully'}), 201


@room_blueprint.route('/room/<int:property_id>', methods=['DELETE'])
def delete_room_by_id(property_id):
    del_room_by_id(property_id)
    return jsonify({'message': 'Room delete successfully'}), 201
