import sqlite3

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
        query = "INSERT INTO users_urls_xref VALUES (?, ?);"
        cursor.execute(query, (self.user_id, self.url_id))
        connection.commit()
        connection.close()
