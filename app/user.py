from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
import sqlite3

class User(object):
    def __init__(self, _id, first_name, last_name, username, password):
        self.id = _id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='{}', username='{}')".format(self.id, self.username)

    @classmethod
    def find_user_by_username(cls, username):
        print("calling find_user_by_username()")
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username = ?;"
        result = cursor.execute(query, (username,))

        row = result.fetchone()
        if row:
            user = cls(row[0], row[1], row[2], row[3], row[4])
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_user_by_id(cls, id):
        print("calling find_user_by_id()")
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE id = ?;"
        result = cursor.execute(query, (id,))

        row = result.fetchone()
        if row:
            user = cls(row[0], row[1], row[2], row[3], row[4])
        else:
            user = None

        connection.close()
        return user


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                       type=str,
                       required=True,
                       help="This field is required."
                       )
    parser.add_argument("password",
                        type=str,
                        required=True,
                        help="This field is required."
                        )
    parser.add_argument("first_name",
                        type=str,
                        required=False,
                        help="First Name."
                        )
    parser.add_argument("last_name",
                        type=str,
                        required=False,
                        help="Last Name."
                        )

    @jwt_required()
    def get(self):
        return {"user": str(current_identity)}

    def post(self):
        data = UserResource.parser.parse_args()

        if User.find_user_by_username(data['username']):
            return {"message": "That Username already exists!"}, 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (Null, ?, ?, ?, ?);"
        cursor.execute(query, (data['first_name'], data['last_name'],
                                        data['username'], data['password'],))
        connection.commit()
        connection.close()

        return {"message": "User created Successfully"}, 201

    @jwt_required()
    def put(self):
        ''' jwt is required in-order to update self '''
        put_parser = UserResource.parser.copy()
        put_parser.remove_argument('password')  # password cannot be updated like this, so removing.
                                                # if provided in payload, silently ignore.

        # updates first_name, last_name
        data = put_parser.parse_args()
        if not User.find_user_by_username(data['username']):
            return {"message": "The username does not exist"}, 400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        base_query = "UPDATE users SET"
        if data['first_name']:
            query = "{} first_name=? WHERE username=?;".format(base_query)
            cursor.execute(query, (data['first_name'], data['username']))
        if data['last_name']:
            query = "{} last_name=? WHERE username=?;".format(base_query)
            cursor.execute(query, (data['last_name'], data['username']))

        connection.commit()
        connection.close()

        return {"message": "User updated Successfully"}, 200

    @jwt_required()
    def delete(self):
        ''' jwt is required in-order to delete self
            password is also required to delete self
        '''
        data = UserResource.parser.parse_args()

        if not User.find_user_by_username(data['username']):
            return {"message": "The username does not exist"}, 404

        if User.find_user_by_username(data['username']).password != data['password']:
            return {"message": "Incorrect password!"}

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "DELETE FROM users WHERE username=?"
        cursor.execute(query, (data['username'],))

        connection.commit()
        connection.close()

        return {"message": "User Deleted Successfully", "user": data['username']}, 200

