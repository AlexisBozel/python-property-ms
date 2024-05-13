from flask import Blueprint, request, jsonify
from app.api.schemas.pricing import PricingBase
from pydantic import ValidationError
from app.api.data_access.pricing import insert_pricing, select_pricing_by_id, update_pricing_by_id, del_pricing_by_id

pricing_blueprint = Blueprint('pricing', __name__)


@pricing_blueprint.route('/pricing/<int:pricing_id>', methods=['GET'])
def get_pricing_by_id(pricing_id):
    pricing = select_pricing_by_id(pricing_id)

    if pricing is None:
        return jsonify({'message': 'Pricing get failed, no pricing find with this id'}), 404

    return jsonify({
        'message': 'Pricing get successfully',
        "result": pricing}), 201


@pricing_blueprint.route('/pricing>', methods=['POST'])
def post_pricing():
    data = request.get_json()

    try:
        pricing = PricingBase(**data)
    except ValidationError as e:
        missing = [{"field": _["loc"][-1], "errorType": _["type"]} for _ in e.errors()]
        return jsonify({"status": "error", "stack": missing}), 400

    pricing_id = insert_pricing(pricing)
    return jsonify({
        'message': 'Pricing post successfully',
        "result": pricing_id}), 201


@pricing_blueprint.route('/pricing/<int:pricing_id>', methods=['PUT'])
def put_pricing_by_id(pricing_id):
    data = request.get_json()

    keys = ["charge", "price"]

    for key in keys:
        if data.get(key):
            value = data.get(key)
            update_pricing_by_id(pricing_id, key, value)

    return jsonify({'message': 'Pricing put successfully'}), 201


@pricing_blueprint.route('/pricing/<int:pricing_id>', methods=['DELETE'])
def delete_pricing_by_id(pricing_id):
    del_pricing_by_id(pricing_id)

    return jsonify({'message': 'Pricing delete successfully'}), 201
