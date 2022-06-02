import datetime
from flask import Flask
from flask_jwt_extended import JWTManager
from pymongo import MongoClient
import os
from routes.home import home_route
from routes.auth import auth_route
from routes.user import user_route

app = Flask(__name__)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = os.urandom(32)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)

# connection string
client = MongoClient(
    "mongodb+srv://enes:gyirFid2l7DOS0OM@cluster0.tjzk4.mongodb.net/?retryWrites=true&w=majority")
db = client["mydb"]
users_collection = db["users"]

home_route(app)  # home route "/"
auth_route(app, users_collection)  # "/api/v1/users" , "/api/v1/login"
user_route(app, users_collection)  # "/api/v1/user"


@jwt.invalid_token_loader
def missing_token_callback(error):
    return {'result': False}, 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return {'result': False}, 401


if __name__ == '__main__':
    app.run(debug=True)
