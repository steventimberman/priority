from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

user_goal_schema = {
    "type": "object",
    "properties": {
        "goal": {
            "type": "string"
        },
        "rank": {
            "type": "number"
        }
    },
    "required": ["goal", "rank"],
    "additionalProperties": False
}

def validate_user_goal(data):
    try:
        validate(data, user_goal_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}
