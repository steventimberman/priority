from flask import Blueprint, request, jsonify
from ..db import mongo
from ..extensions import (flask_bcrypt, jwt)
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)



mod = Blueprint('goals', __name__, url_prefix='/goals')

@mod.route('/all', methods=['GET', 'DELETE'])
@jwt_required
def goals_all():
    identity = get_jwt_identity()
    user = mongo.db.users.find_one({"email": identity["email"]})

    if request.method == 'GET':
        print (user)
        data = user["goals"]
        return jsonify({'ok': True, 'data': data}), 200

    if request.method == 'DELETE':   # TODO add fault tolerance, count to make sure all goals have been dropped
        goal_ids = [goal.goal_id for goal in user.goals]
        for goal_id in goal_ids:
            db_response = mongo.db.goals.delete_one({'_id': goal_id})
        mongo.db.user.update_one(user, {'$set': {'goals': []} })
        return jsonify({'ok': True, 'message': 'record deleted'}), 200





@mod.route('', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@jwt_required
def goal():
    ''' goals endpoint '''
    # TODO: validate request, if data ok:
    identity = get_jwt_identity()
    user = mongo.db.users.find_one({"email" :identity["email"]})
    if request.method == 'GET':
        return get_goal(user)

    data = request.get_json
    if request.method == 'DELETE':
        return delete_goal(user)

    if request.method == 'PATCH':
        return patch_goal(user)

    if request.method == 'POST':
        data = request.get_json()
        return post_goal(user, data)

    return jsonify(
            {'ok': False, 'message': 'Bad request'}
        ), 400

def get_goal(user):
    rank = request.args
    goal = user["goals"][rank]
    goal_id = goal["goal_id"]

    goal_complete_info = mongo.db.goals.find_one({"_id": goal_id})
    return jsonify({'ok': True, 'data': goal_complete_info}), 200

def delete_goal(user):
    pass

def patch_goal(user):
    pass

def post_goal(user, data):
    print (data)
    new_goal_response = mongo.db.goals.insert_one(data).inserted_id
    goal_id = new_goal_response
    print (user)
    current_goals = user["goals"]

    new_goal = data

    rank = new_goal["rank"]
    new_goals = current_goals[:rank] + [new_goal] + current_goals[rank:]
    for goal in new_goals[rank+1:]:
        goal["rank"] += 1
    mongo.db.user.update_one(user, {'$set': {'goals': new_goals} })

    print (new_goal)
    return jsonify({'ok': True, 'data':  new_goal})

def init_app(app):
    app.register_blueprint(mod)


