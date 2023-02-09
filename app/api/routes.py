from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Collection, collect_schema, collects_schema

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/collection', methods = ['POST'])
@token_required
def create_beer(current_user_token):
    brand = request.json['brand']
    type = request.json['type']
    abv = request.json['abv']
    ibu = request.json['ibu']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    collect = Collection(brand, type, abv, ibu, user_token=user_token)

    db.session.add(collect)
    db.session.commit()

    response = collect_schema.dump(collect)
    return jsonify(response)

@api.route('/collection', methods = ['GET'])
@token_required
def get_allbeer(current_user_token):
    a_user = current_user_token.token
    collects = Collection.query.filter_by(user_token = a_user).all()
    response = collects_schema.dump(collects)
    return jsonify(response)

@api.route('/collection/<id>', methods = ['GET'])
@token_required
def get_beer(current_user_token, id):
    collect = Collection.query.get(id)
    response = collect_schema.dump(collect)
    return jsonify(response)

@api.route('/collection/<id>', methods = ['POST', 'PUT'])
@token_required
def update_beer(current_user_token, id):
    collect = Collection.query.get(id)
    collect.name = request.json['brand']
    collect.email = request.json['type']
    collect.phone_number = request.json['abv']
    collect.address = request.json['ibu']
    collect.user_token = current_user_token.token

    db.session.commit()
    response = collect_schema.dump(collect)
    return jsonify(response)

@api.route('/collection/<id>', methods = ['DELETE'])
@token_required
def delete_beer(current_user_token, id):
    collect = Collection.query.get(id)
    db.session.delete(collect)
    db.session.commit()
    response = collect_schema.dump(collect)
    return jsonify(response)

    