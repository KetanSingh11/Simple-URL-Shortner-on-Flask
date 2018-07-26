from flask import Flask
from flask_jwt import JWT
from flask_restful import Resource, Api
from security import authenticate, identity
from url import UrlResource
from user import UserResource
from users import UsersResource
from users_urls_xref import UsersUrlsXrefResource

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
api.add_resource(UrlResource, "/shorten")
api.add_resource(UsersUrlsXrefResource, "/uuxref")


if __name__ == "__main__":
    print("Starting MAIN()")
    app.run(debug=True)
