from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from utils.encoder import JSONEncoder
from bson import ObjectId
from werkzeug.security import generate_password_hash


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
                del user['password']
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
                del user['password']
                user_list.append(user)

        return json.loads(JSONEncoder().encode({"result": user_list})), 200

    @app.route("/api/v1/follow", methods=["POST"])
    @jwt_required()
    def follow():
        data = request.get_json()
        to_follow = data['username']
        current_user = get_jwt_identity()
        current_user_from_db = users_collection.find_one(
            {'username': current_user})
        current_user_from_db['following'].append(to_follow)
        users_collection.find_one_and_update({'_id': ObjectId(current_user_from_db['_id'])}, {
                                             '$set': {"following": current_user_from_db['following']}})

        return json.loads(JSONEncoder().encode({"result": "followed"})), 200

    @app.route("/api/v1/unfollow", methods=["POST"])
    @jwt_required()
    def unfollow():
        data = request.get_json()
        to_unfollow = data['username']
        current_user = get_jwt_identity()
        current_user_from_db = users_collection.find_one(
            {'username': current_user})
        following_arr = current_user_from_db['following']
        following_arr.remove(to_unfollow)
        users_collection.find_one_and_update({'_id': ObjectId(current_user_from_db['_id'])}, {
            '$set': {"following": following_arr}})

        return json.loads(JSONEncoder().encode({"result": "followed"})), 200

    @app.route("/api/v1/getFollowersByUsername", methods=["POST"])
    @jwt_required()
    def get_followers():
        data = request.get_json()
        check_username = data['username']
        users_from_db = users_collection.find({})

        user_list = []

        for user in users_from_db:
            if check_username in user['following']:
                del user['password']
                user_list.append(user)

        return json.loads(JSONEncoder().encode({"result": user_list})), 200

    @app.route("/api/v1/changePassword", methods=["POST"])
    @jwt_required()
    def change_password():
        data = request.get_json()
        current_user = get_jwt_identity()
        user_from_db = users_collection.find_one({'username': current_user})
        users_collection.find_one_and_update({'_id': ObjectId(user_from_db['_id'])}, {
                                             '$set': {"password": generate_password_hash(data['password'])}})

        return json.loads(JSONEncoder().encode({"result": "password changed"})), 200
