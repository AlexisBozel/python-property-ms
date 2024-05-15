from flask import Blueprint, request, jsonify

from app.api.manager.advert import (
    get_advert as retrieve_advert,
    get_adverts as retrieve_adverts,
    get_adverts_by_property_owner as retrieve_advert_by_property_owner,
    post_advert as create_advert,
    put_advert as update_advert,
    delete_advert as remove_advert
)

advert_blueprint = Blueprint('advert', __name__)


@advert_blueprint.route('/advert/<int:advert_id>', methods=['GET'])
def get_advert(advert_id):
    advert = retrieve_advert(advert_id)
    if advert is None:
        return jsonify({'message': 'Advert get failed, no pricing find with this id'}), 404
    return jsonify({
        'message': 'Advert get successfully',
        'status': 'Success',
        "result": advert}), 201


@advert_blueprint.route('/adverts', methods=['GET'])
def get_adverts():
    adverts = retrieve_adverts()
    return jsonify({
        'message': 'Adverts get successfully',
        'status': 'Success',
        "result": adverts}), 201


@advert_blueprint.route('/adverts/<int:advert_id>', methods=['GET'])
def get_adverts_by_owner(advert_id):
    adverts = retrieve_advert_by_property_owner(advert_id)
    return jsonify({
        'message': 'Adverts get successfully',
        'status': 'Success',
        "result": adverts}), 201


@advert_blueprint.route('/advert', methods=['POST'])
def post_advert():
    data = request.get_json()
    advert_id = create_advert(data)
    return jsonify({
        'message': 'Advert post successfully',
        'status': 'Success',
        "result": advert_id}), 201


@advert_blueprint.route('/advert/<int:advert_id>', methods=['PUT'])
def put_advert(advert_id):
    data = request.get_json()
    update_advert(advert_id, data)
    return jsonify({
        'message': 'Advert put successfully',
        'status': 'Success'}), 201


@advert_blueprint.route('/advert/<int:advert_id>', methods=['DELETE'])
def delete_advert(advert_id):
    remove_advert(advert_id)
    return jsonify({
        'message': 'Advert delete successfully',
        'status': 'Success'}), 201
