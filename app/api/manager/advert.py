from pydantic import ValidationError
from flask import jsonify
from app.api.schemas.advert import AdvertInputBase, AdvertOutputBase
from app.api.manager.property import (
    get_property
)
from app.api.data_access.advert import (
    select_advert,
    select_adverts,
    select_adverts_by_property_owner,
    insert_advert,
    update_advert,
    select_advert_with_filter,
    delete_advert as remove_advert
)
from app.api.schemas.property import PropertyOutputBase


def get_advert(advert_id):
    advert = select_advert(advert_id)
    advert_base = get_full_advert(advert)
    return advert_base


def get_adverts():
    adverts = select_adverts()
    adverts_base = []
    for advert in adverts:
        advert_tmp = get_full_advert(advert)
        print(advert_tmp)
        adverts_base.append(advert_tmp)
    print(adverts_base)

    return adverts_base


def get_full_advert(advert):
    property_id = advert["idProperty"]
    property = get_property(property_id)
    try:
        advert_base = AdvertOutputBase(
            idAdvert=advert.get("idAdvert"),
            property=property,
            title=advert.get("title"),
            description=advert.get("description"),
            dtCreation=advert.get("dtCreation"),
            dtModification=advert.get("dtModification"),
            dtAvailability=advert.get("dtAvailability"),
        )
    except ValidationError as e:
        missing = [{"field": _["loc"][-1], "errorType": _["type"]} for _ in e.errors()]
        print(missing)
        return jsonify({"status": "error", "stack": missing}), 400
    return advert_base.dict()


def get_adverts_by_property_owner(owner_id):
    advert = select_adverts_by_property_owner(owner_id)
    advert_base = get_full_advert(advert)
    return advert_base


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
    adverts_base = []
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
        adverts = select_advert_with_filter(query)
        for advert in adverts:
            advert_tmp = get_full_advert(advert)
            adverts_base.append(advert_tmp)

    return adverts_base


def add_AND_to_query(query):
    if query != "":
        query += " AND "
    return query
