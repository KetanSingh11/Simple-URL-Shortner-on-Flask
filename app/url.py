import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from users_urls_xref import Users_Urls_Xref

class Url(object):
    def __init__(self, _id, long_url, short_url):
        self.id = _id
        self.long_url = long_url
        self.short_url = short_url

    @classmethod
    def get_url_set_by_id(cls, _id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT id, long_url, short_url FROM urls WHERE id = ?;"
        result = cursor.execute(query, (_id,))

        row = result.fetchone()
        if row:
            url = cls(row[0], row[1], row[2])
        else:
            url = None

        connection.close()
        return url

    @classmethod
    def get_url_set_by_long_url(cls, long_url):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "SELECT id, long_url, short_url FROM urls WHERE long_url = ?;"
        result = cursor.execute(query, (long_url,))

        row = result.fetchone()
        if row:
            url = cls(row[0], row[1], row[2])
        else:
            url = None

        connection.close()
        return url


class UrlResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("long_url",
                        type=str,
                        required=True,
                        help="This field is required."
    )

    @jwt_required()
    def get(self):
        data = UrlResource.parser.parse_args()
        url = Url.get_url_set_by_long_url(data['long_url'])

        if url:
            return {"long_url": url.long_url, "short_url": url.short_url}, 200
        else:
            return {"message": "No long url found!"}, 404

    @jwt_required()
    def post(self):
        data = UrlResource.parser.parse_args()
        existing_url = Url.get_url_set_by_long_url(data['long_url'])
        if existing_url:
            # re-use already shortened value
            # insert into xref table, check if its a repeated set as well
            new_uuxref = Users_Urls_Xref(current_identity.id, existing_url.id)
            if not new_uuxref.exists():
                new_uuxref.insert()
                return {"message": "URL already shortened previously, using that old value."}, 201
            else:
                return {"message": "This User already has shortened this URL."}, 200


    def delete(self):
        pass
