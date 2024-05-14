from flask import jsonify
from app.api.schemas.room import RoomBase
from pydantic import ValidationError
from app.api.data_access.room import (
    insert_room,
    select_room,
    select_room_by_type,
    update_room_by_type,
    delete_room_by_type as remove_room_by_type,
    delete_room as remove_room
)


def get_room(property_id):
    return select_room(property_id)


def post_room(property_id, data):
    list_room = []
    for room_tmp in data["rooms"]:
        try:
            print(room_tmp)
            room = RoomBase(**room_tmp)

            # check if type exist
            rooms = select_room_by_type(property_id, room.type)

            if rooms is None:
                list_room.append(room)
        except ValidationError as e:
            missing = [{"field": _["loc"][-1], "errorType": _["type"]} for _ in e.errors()]
            return jsonify({"status": "error", "stack": missing}), 400

    for room in list_room:
        insert_room(room, property_id)


def put_room(property_id, data):
    for room_data in data["rooms"]:
        value_type = room_data.get("type")
        value_number = room_data.get("number")
        if value_type and value_number:
            update_room_by_type(property_id, value_type, value_number)


def delete_room_by_type(property_id, data):
    room_type = data.get("type")
    remove_room_by_type(property_id, room_type)


def delete_room(property_id):
    remove_room(property_id)
