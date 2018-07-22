from flask_restful import Resource
import sqlite3

class UsersResource(Resource):
    def get(self):
        ''' CAUTION: do not return/expose Passwords! '''
        ''' gets ALL the users in users DB table '''

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT username, first_name, last_name FROM users;"
        result = cursor.execute(query)

        users = []
        for row in result:
            users.append({'username': row[0],
                          'first_name': row[1],
                          'last_name': row[2]})

        return {'users': users}, 200

