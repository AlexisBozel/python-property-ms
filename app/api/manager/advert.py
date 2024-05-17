from pydantic import ValidationError
from flask import jsonify
from app.api.schemas.advert import AdvertInputBase
from app.api.data_access.advert import (
    select_advert,
    select_adverts,
    select_adverts_by_property_owner,
    insert_advert,
    update_advert,
    select_advert_with_filter,
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


def get_adverts_with_filters(filter_address, filter_surface_max, filter_surface_min, filter_price_max, filter_price_min,
                             filter_room):
    properties = []
    query = ""
    if filter_address:
        # contains address
        query += " address like %" + filter_address + "% "

    if filter_surface_max and filter_surface_min:
        # between
        add_AND_to_query(query)
        query += " surface BETWEEN " + filter_surface_min + " AND " + filter_surface_max
    elif filter_surface_max:
        add_AND_to_query(query)
        query += " surface <= " + filter_surface_max
    elif filter_surface_min:
        add_AND_to_query(query)
        query += " surface >= " + filter_surface_min

    if filter_price_max and filter_price_min:
        add_AND_to_query(query)
        query += " price BETWEEN " + filter_price_min + " AND " + filter_price_max
    elif filter_price_max:
        add_AND_to_query(query)
        query += " price <= " + filter_price_max
    elif filter_price_min:
        add_AND_to_query(query)
        query += " price >= " + filter_price_max

    if filter_room:
        add_AND_to_query(query)
        query += " type = " + filter_price_max

    if query != "":
        properties = select_advert_with_filter(query)

    return properties


def add_AND_to_query(query):
    if query != "":
        query += " AND "
    return query
