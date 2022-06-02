from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from utils.encoder import JSONEncoder


def user_route(app, users_collection):
    @app.route("/api/v1/user", methods=["GET"])
    @jwt_required()
    def profile():
        current_user = get_jwt_identity()  # Get the identity of the current user
        user_from_db = users_collection.find_one({'username': current_user})
        if user_from_db:
            # delete data we don't want to return
            del user_from_db['password']
            return json.loads(JSONEncoder().encode({"results": user_from_db})), 200
        else:
            return jsonify({'msg': 'Profile not found'}), 404
