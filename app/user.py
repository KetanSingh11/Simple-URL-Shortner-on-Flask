from flask_restful import Resource
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
        return "User(id='%s', username='%s')" % (self.id, self.username)

    @classmethod
    def find_user_by_username(cls, username):
        print("calling find_user_by_username()")
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE username = ?"
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
        query = "SELECT * FROM users WHERE id = ?"
        result = cursor.execute(query, (id,))

        row = result.fetchone()
        if row:
            user = cls(row[0], row[1], row[2], row[3], row[4])
        else:
            user = None

        connection.close()
        return user


class UserResource(Resource):
    @jwt_required()
    def get(self):
        return {"message": str(current_identity)}
