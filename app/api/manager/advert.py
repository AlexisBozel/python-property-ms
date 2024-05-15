from pydantic import ValidationError
from flask import jsonify
from app.api.schemas.advert import AdvertInputBase
from app.api.data_access.advert import (
    select_advert,
    select_adverts,
    select_adverts_by_property_owner,
    insert_advert,
    update_advert,
    delete_advert as remove_advert
)


def get_advert(advert_id):
    return select_advert(advert_id)


def get_adverts():
    return select_adverts()


def get_adverts_by_property_owner(owner_id):
    return select_adverts_by_property_owner(owner_id)


def post_advert(data):
    try:
        advert = AdvertInputBase(**data)
    except ValidationError as e:
        missing = [{"field": _["loc"][-1], "errorType": _["type"]} for _ in e.errors()]
        return jsonify({"status": "error", "stack": missing}), 400
    return insert_advert(advert)


def put_advert(advert_id, data):
    keys = ["idProperty", "title", "description", "dtAvailability"]

    for key in keys:
        if data.get(key):
            value = data.get(key)
            update_advert(advert_id, key, value)


def delete_advert(advert_id):
    remove_advert(advert_id)
