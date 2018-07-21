import sqlite3

connection = sqlite3.connect("data.db")

cursor = connection.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (" \
               "id INTEGER PRIMARY KEY, " \
               "first_name TEXT NOT NULL, " \
               "last_name TEXT, " \
               "username TEXT NOT NULL, " \
               "password TEXT NOT NULL)"

cursor.execute(create_table)

user = (1, 'tom', 'hardy', 'tommy', 'asdf')
insert_query = "INSERT INTO users VALUES (?, ?, ?, ?, ?)"
cursor.execute(insert_query, user)

connection.commit()
connection.close()

print("~ Tables Created Successfully!")
print("Inserted one dummy user entry in DB.")
