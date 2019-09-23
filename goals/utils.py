import attr
from bson.objectid import ObjectId
from flask import jsonify

from ..db import mongo

@attr.s
class UserGoals(object):
    email = attr.ib()
    user = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.user = mongo.db.users.find_one({"email": self.email})

    def goals(self):
        """
        Returns a user's goals. This is a dictionary of objects with keys
        'goal' (string) and 'rank' (int)
        """
        return self.user["goals"]

    def goal_basic(self, rank):
        """
        Returns a single goal of the user, specified by rank, with keys
        'goal' and 'rank' only
        """
        return self.goals()[rank]

    def goal(self, rank):
        """
        Returns an entire goal object from the goals table (mongo.db.goals)
        """

        goal_id = self.goal_id(rank)
        goal = mongo.db.goals.find_one({"_id": goal_id})
        return goal

    def goal_ids(self):
        """ Returns a list of a users goal ids """
        return [ObjectId(goal["_id"]) for goal in self.goals()]

    def goal_id(self, rank):
        """ Returns the goal id of a user's goal, specified by rank """
        goal = self.goal_basic(rank)
        return ObjectId(goal["_id"])

    def delete_goal(self, rank):
        goal_id = self.goal_id(rank)
        mongo.db.goals.delete_one({'_id': goal_id})
        goals = self.goals()
        new_goals = []
        goal_found = False
        for goal in goals:
            if goal["_id"] == goal_id:
                goal_found = True
            else:
                if goal_found:
                    goal["rank"] -= 1
                new_goals.append(goal)
        mongo.db.users.update_one(self.user, {'$set': {'goals': new_goals} })
        return True

    def delete_goals(self):
        """
        Deletes all goals of a user in both the goals field of the user,
        and in the goals table (mongo.db.goals)
        """
        for goal_id in self.goal_ids():
            mongo.db.goals.delete_one({'_id': goal_id})
        mongo.db.users.update_one(self.user, {'$set': {'goals': []} })
        return {'ok': True, 'message': 'records deleted'}

    def insert_goal(self, goal, rank):
        if rank >= len(self.goals()):

        data = {'goal': goal, 'rank': rank}
        goal_id = mongo.db.goals.insert_one(data).inserted_id
        new_goal = mongo.db.goals.find_one({'_id': goal_id})

        new_goals = self.new_goals(new_goal)
        mongo.db.users.update_one({"_id": self.user["_id"]}, {'$set': {'goals': new_goals} })

        return new_goal

    def new_goals(self, goal):
        rank = goal["rank"]
        current_goals = self.goals()
        new_goals = current_goals[:rank-1] + [goal] + current_goals[rank-1:]

        for i in range(rank, len(new_goals)):
            cur_goal = new_goals[i]
            cur_goal["rank"] += 1
            cur_id = cur_goal["_id"]
            mongo.db.goals.update_one({"_id": cur_id}, {'$set': {'rank': cur_goal["rank"]} })

        return new_goals

@attr.s
class RouteResponse(object):
    ok = attr.ib(default=True)
    data = attr.ib(default=None)
    message = attr.ib(default=None)



    def __attrs_post_init__(self):
        self.response_code = 200 if self.ok else 400
        response_object = {'ok': self.ok}
        if self.data:
            response_object["data"] = self.data
        if self.message:
            response_object["message"] = self.message

        self.response_object = response_object

    def response(self):
        return jsonify(self.response_object), self.response_code




