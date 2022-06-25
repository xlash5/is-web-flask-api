import datetime
from flask import Flask
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
import os
from routes.home import home_route
from routes.auth import auth_route
from routes.user import user_route
from flask_cors import CORS
from utils.blacklist import BLACKLIST
from routes.posts import posts_route


app = Flask(__name__)
CORS(app)
jwt = JWTManager(app)
app.config['SECRET_KEY'] = os.urandom(32)
app.config['JWT_SECRET_KEY'] = os.urandom(32)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
app.config['JWT_BLACKLIST_ENABLED'] = True

# connection string
client = MongoClient(
    "mongodb+srv://enes:gyirFid2l7DOS0OM@cluster0.tjzk4.mongodb.net/?retryWrites=true&w=majority")
db = client["mydb"]
users_collection = db["users"]
posts_collection = db["posts"]

# home route "/"
home_route(app)

# "/api/v1/register" , "/api/v1/login", "/api/v1/is-authenticated", "/api/v1/logout"
auth_route(app, users_collection)

# "/api/v1/user"
user_route(app, users_collection)

posts_route(app, posts_collection, users_collection)


@jwt.invalid_token_loader
def missing_token_callback(error):
    return {'result': False}, 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return {'result': False}, 401


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in BLACKLIST


if __name__ == '__main__':
    app.run(port=8000, debug=True)
