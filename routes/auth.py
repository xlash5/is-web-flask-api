from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash


def auth_route(app, users_collection):
    @app.route("/api/v1/register", methods=["POST"])
    def register():
        new_user = request.get_json()  # store the json body request
        new_user["password"] = generate_password_hash(
            new_user["password"])  # encrpt password
        doc = users_collection.find_one(
            {"username": new_user["username"]})  # check if user exist
        if not doc:
            users_collection.insert_one(new_user)
            return jsonify({'msg': 'User created successfully'}), 201
        else:
            return jsonify({'msg': 'Username already exists'}), 409

    @app.route("/api/v1/login", methods=["POST"])
    def login():
        login_details = request.get_json()  # store the json body request
        user_from_db = users_collection.find_one(
            {'username': login_details['username']})  # search for user in database

        if user_from_db:
            if check_password_hash(user_from_db['password'], login_details['password']):
                access_token = create_access_token(
                    identity=user_from_db['username'])  # create jwt token
                return jsonify(access_token=access_token), 200

        return jsonify({'msg': 'The username or password is incorrect'}), 401

    @app.route("/api/v1/is-authenticated", methods=["GET"])
    @jwt_required()
    def is_authenticated():
        return jsonify({'result': True}), 200
