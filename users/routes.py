from flask import Blueprint, request, jsonify
from ..db import mongo
from ..extensions import (flask_bcrypt, jwt)
from .schema import validate_user
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, jwt_refresh_token_required,
    get_jwt_identity
)

mod = Blueprint('users', __name__)

@jwt.unauthorized_loader
def unauthorized_response(callback):
    return jsonify({
        'ok': False,
        'message': 'Missing Authorization Header'
    }), 401


@mod.route('/auth', methods=['POST'])
def auth_user():
    ''' auth endpoint '''
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        user = mongo.db.users.find_one({'email': data['email']})
        if (user and
             flask_bcrypt.check_password_hash(user['password'],
                data['password'])
             ):
            del user['password']
            access_token = create_access_token(identity=data)
            refresh_token = create_refresh_token(identity=data)
            print (get_jwt_identity())
            user['token'] = access_token
            user['refresh'] = refresh_token
            return jsonify({'ok': True, 'data': user}), 200
        else:
            return jsonify(
                {'ok': False, 'message': 'invalid username or password'}
            ), 401
    else:
        return jsonify(
            {'ok': False, 'message': 'Bad request parameters: {}'.format(
                data['message']
            )}
        ), 400

@mod.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    ''' refresh token endpoint '''
    current_user = get_jwt_identity()
    ret = {
            'token': create_access_token(identity=current_user)
    }
    return jsonify({'ok': True, 'data': ret}), 200

@mod.route('/register', methods=['POST'])
def register():
    ''' register user endpoint '''
    data = validate_user(request.get_json())
    if data['ok']:
        data = data['data']
        data['password'] = flask_bcrypt.generate_password_hash(data['password'])
        data['goals'] = []
        mongo.db.users.insert_one(data)
        return jsonify(
            {'ok': True, 'message': 'User created successfully!'}
        ), 200
    else:
        return jsonify(
            {'ok': False, 'message': 'Bad request parameters: {}'.format(
                data['message'])
            }
        ), 400

@mod.route('/user', methods=['GET', 'DELETE', 'PATCH'])
@jwt_required
def user():
    ''' route read user '''
    if request.method == 'GET':
        query = request.args
        data = mongo.db.users.find_one(query)
        del data["password"]
        return jsonify({'ok': True, 'data': data}), 200

    data = request.json()
    if request.method == 'DELETE':
        if data.get('email', None) is not None:
            db_response = mongo.db.users.delete_one({'email': data['email']})
            if db_response.deleted_count == 1:
                response = {'ok': True, 'message': 'record deleted'}
            else:
                response = {'ok': True, 'message': 'no record found'}
            return jsonify(response), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400

    if request.method == 'PATCH':
        if data.get('query', {}) != {}:
            mongo.db.users.update_one(
                data['query'], {'$set': data.get('payload', {})})
            return jsonify({'ok': True, 'message': 'record updated'}), 200
        else:
            return jsonify({'ok': False, 'message': 'Bad request parameters!'}), 400


def init_app(app):
    app.register_blueprint(mod)
