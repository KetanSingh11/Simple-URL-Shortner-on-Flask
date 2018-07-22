from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity
from user import UserResource
from users import UsersResource

app = Flask(__name__)
app.secret_key = "k101011"
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth


class IndexResource(Resource):
    def get(self):
        return "Hello, World!", 200




api.add_resource(IndexResource, "/")
api.add_resource(UserResource, "/user")
api.add_resource(UsersResource, "/users")

if __name__ == "__main__":
    print("Starting MAIN()")
    app.run(debug=True)
