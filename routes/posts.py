from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

from requests import post
from utils.encoder import JSONEncoder


def posts_route(app, posts_collection):
    @app.route("/api/v1/createPost", methods=["POST"])
    @jwt_required()
    def create_post():
        data = request.get_json()
        current_user = get_jwt_identity()

        if data["text"] == '':
            return jsonify({'msg': 'No input data provided'}), 400

        postData = {}
        postData["text"] = data["text"]
        postData["media"] = data["media"]
        postData["author"] = current_user

        posts_collection.insert_one(postData)

        return json.loads(JSONEncoder().encode({"result": "success"})), 200
