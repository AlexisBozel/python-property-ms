from flask import Blueprint, request, jsonify

from app.api.manager.pricing import (
    get_pricing as retrieve_pricing,
    post_pricing as create_pricing,
    put_pricing as update_pricing,
    delete_pricing as remove_pricing
)

pricing_blueprint = Blueprint('pricing', __name__)


@pricing_blueprint.route('/pricing/<int:pricing_id>', methods=['GET'])
def get_pricing(pricing_id):
    pricing = retrieve_pricing(pricing_id)
    if pricing is None:
        return jsonify({'message': 'Pricing get failed, no pricing find with this id'}), 404
    return jsonify({
        'message': 'Pricing get successfully',
        'status': 'Success',
        "result": pricing}), 201


@pricing_blueprint.route('/pricing', methods=['POST'])
def post_pricing():
    data = request.get_json()
    pricing_id = create_pricing(data)
    return jsonify({
        'message': 'Pricing post successfully',
        'status': 'Success',
        "result": pricing_id}), 201


@pricing_blueprint.route('/pricing/<int:pricing_id>', methods=['PUT'])
def put_pricing(pricing_id):
    data = request.get_json()
    update_pricing(pricing_id, data)
    return jsonify({
        'message': 'Pricing put successfully',
        'status': 'Success'}), 201


@pricing_blueprint.route('/pricing/<int:pricing_id>', methods=['DELETE'])
def delete_pricing(pricing_id):
    remove_pricing(pricing_id)
    return jsonify({
        'message': 'Pricing delete successfully',
        'status': 'Success'}), 201
