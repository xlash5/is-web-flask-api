from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import json
from datetime import datetime
from bson import ObjectId
from utils.encoder import JSONEncoder


def posts_route(app, posts_collection, users_collection):
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
        postData["date"] = datetime.now().timestamp()*1000

        posts_collection.insert_one(postData)

        return json.loads(JSONEncoder().encode({"result": "success"})), 200

    @app.route("/api/v1/getPosts", methods=["GET"])
    @jwt_required()
    def getPosts():
        # get all posts from collection
        all_posts = posts_collection.find({})
        current_user = get_jwt_identity()
        following = users_collection.find_one(
            {"username": current_user})["following"]

        posts = []
        for post in all_posts:
            if post["author"] == current_user:
                posts.append(post)
            elif post["author"] in following:
                posts.append(post)

        posts.sort(key=lambda x: x['date'], reverse=True)

        return json.loads(JSONEncoder().encode({'result': posts})), 200

    @app.route("/api/v1/addComment", methods=["POST"])
    @jwt_required
    def addComment():
        comment_data = request.get_json()

        curr_post = users_collection.find_one(
            {'_id': ObjectId(comment_data['id'])})

        if curr_post['comments'] == None or curr_post['comments'] == []:
            curr_post['comments'] = []
        else:
            curr_post['comments'].append({
                'text': comment_data['text'],
                'author': comment_data['author'],
                'date': datetime.now().timestamp()*1000
            })

        posts_collection.find_one_and_update({'_id': ObjectId(comment_data['id'])}, {
                                             '$set': {"comments": curr_post['comments']}})

        return json.loads(JSONEncoder().encode({"result": "success"})), 200
