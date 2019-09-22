from flask import Blueprint, request, jsonify
from ..db import mongo
from ..extensions import (flask_bcrypt, jwt)
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from .utils import UserGoals, RouteResponse

mod = Blueprint('goals', __name__, url_prefix='/goals')

@mod.route('/all', methods=['GET', 'DELETE'])
@jwt_required
def goals_all():
    identity = get_jwt_identity()
    user = UserGoals(identity["email"])

    if request.method == 'GET':
        data = user.goals()
        return RouteResponse(ok=True, data=data).response()

    if request.method == 'DELETE':   # TODO add fault tolerance, count to make sure all goals have been dropped
        goals_were_deleted = user.delete_goals()
        ok = goals_were_deleted['ok']
        message = goals_were_deleted['message']
        return RouteResponse(ok=ok, message=message).response()

@mod.route('', methods=['GET', 'POST', 'DELETE', 'PATCH'])
@jwt_required
def goal():
    ''' goals endpoint '''
    # TODO: validate request, if data ok:
    identity = get_jwt_identity()
    user = UserGoals(identity["email"])
    if request.method == 'GET':
        rank = int(request.args["rank"])
        goal = user.goal(rank)
        return RouteResponse(ok=True, data=goal).response()


    data = request.get_json()
    if request.method == 'DELETE':
        rank = int(request.args["rank"])
        ok = user.delete_goal(rank)
        message = "Goal deleted" if ok else "unable to delete goal"
        return RouteResponse(ok=ok, message=message).response()

    if request.method == 'POST':
        goal_string = data['goal']
        goal_rank = data['rank']
        new_goal = user.insert_goal(goal_string, goal_rank)
        return RouteResponse(ok=True, data=new_goal).response()

    return RouteResponse(ok=False, message='Bad request').response()


def init_app(app):
    app.register_blueprint(mod)
