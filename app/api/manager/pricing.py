from flask import jsonify
from app.api.schemas.pricing import PricingBase
from pydantic import ValidationError
from app.api.data_access.pricing import (
    insert_pricing,
    select_pricing,
    update_pricing,
    delete_pricing as remove_pricing
)


def get_pricing(pricing_id):
    return select_pricing(pricing_id)


def post_pricing(data):
    try:
        pricing = PricingBase(**data)
    except ValidationError as e:
        missing = [{"field": _["loc"][-1], "errorType": _["type"]} for _ in e.errors()]
        return jsonify({"status": "error", "stack": missing}), 400

    return insert_pricing(pricing)


def put_pricing(pricing_id, data):
    keys = ["charge", "price"]

    for key in keys:
        if data.get(key):
            value = data.get(key)
            update_pricing(pricing_id, key, value)


def delete_pricing(pricing_id):
    remove_pricing(pricing_id)
