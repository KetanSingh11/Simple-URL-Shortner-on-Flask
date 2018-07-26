import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from user import User

class Users_Urls_Xref(object):
    def __init__(self, user_id, url_id):
        self.user_id = user_id
        self.url_id = url_id

    def exists(self):
        """ check if a (user_id, url_id) pair already exists or not """
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT user_id, url_id FROM users_urls_xref where user_id = ?;"
        result = cursor.execute(query, (self.user_id,))

        row = result.fetchone()
        connection.close()
        if row:
            return True
        else:
            return False

    def insert(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "INSERT INTO users_urls_xref (user_id, url_id) VALUES (?, ?);"
        cursor.execute(query, (self.user_id, self.url_id))
        connection.commit()
        connection.close()

    @classmethod
    def get_all_urls_from_user_id(cls, user_id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT uuxref.url_id, u.long_url, u.short_url FROM users_urls_xref uuxref " \
                "INNER JOIN urls u ON uuxref.url_id = u.id WHERE uuxref.user_id = ?;"
        print(query)
        result = cursor.execute(query, (user_id,))

        rows = result.fetchall()
        urls = []
        for row in rows:
            urls.append({'long_url': row[1], 'short_url': row[2]})

        connection.close()
        return urls


class UsersUrlsXrefResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        help="Provide username to list all your urls")

    def get(self):
        data = UsersUrlsXrefResource.parser.parse_args()
        user_obj = User.find_user_by_username(data['username'])
        if user_obj:
            return {"username": user_obj.username,
                    "urls": Users_Urls_Xref.get_all_urls_from_user_id(user_obj.id)}, 200
        else:
            return {"message": "User with username '{}' not found!".format(data['username'])}, 404
