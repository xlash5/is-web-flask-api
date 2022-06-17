from flask import jsonify, request
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
            return json.loads(JSONEncoder().encode({"result": user_from_db})), 200
        else:
            return jsonify({'msg': 'Profile not found'}), 404

    @app.route("/api/v1/username", methods=["POST"])
    @jwt_required()
    def user_by_name():
        data = request.get_json()  # store the json body request
        print(data)
        user_from_db = users_collection.find_one(
            {'username': data['username']})  # find the user in the database
        if user_from_db:
            # delete data we don't want to return
            del user_from_db['password']
            return json.loads(JSONEncoder().encode({"result": user_from_db})), 200
        else:
            return jsonify({'msg': 'User not found'}), 404

    @app.route("/api/v1/getFollowing", methods=["GET"])
    @jwt_required()
    def get_following():
        current_user = get_jwt_identity()
        users_from_db = users_collection.find({})
        current_user_from_db = users_collection.find_one(
            {'username': current_user})

        user_list = []

        for user in users_from_db:
            if user['username'] in current_user_from_db['following']:
                user_list.append(user)

        return json.loads(JSONEncoder().encode({"result": user_list})), 200

    @app.route("/api/v1/getNotFollowing", methods=["GET"])
    @jwt_required()
    def get_not_following():
        current_user = get_jwt_identity()
        users_from_db = users_collection.find({})
        current_user_from_db = users_collection.find_one(
            {'username': current_user})

        user_list = []

        for user in users_from_db:
            if user['username'] not in current_user_from_db['following'] and user['username'] != current_user:
                user_list.append(user)

        return json.loads(JSONEncoder().encode({"result": user_list})), 200
