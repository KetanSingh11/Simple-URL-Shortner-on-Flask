import sqlite3

connection = sqlite3.connect("data.db")

cursor = connection.cursor()

# users
create_table = "CREATE TABLE IF NOT EXISTS users (" \
               "id INTEGER PRIMARY KEY, " \
               "first_name TEXT NOT NULL, " \
               "last_name TEXT, " \
               "username TEXT NOT NULL, " \
               "password TEXT NOT NULL);"

cursor.execute(create_table)

user = (1, 'john', 'dow', 'admin', 'asdf')
insert_query = "INSERT INTO users VALUES (?, ?, ?, ?, ?);"
cursor.execute(insert_query, user)

# urls
create_table = "CREATE TABLE IF NOT EXISTS urls (" \
               "id INTEGER PRIMARY KEY, " \
               "long_url TEXT NOT NULL, " \
               "short_url TEXT NOT NULL);"
cursor.execute(create_table)

# users_urls_xref
create_table = "CREATE TABLE IF NOT EXISTS users_urls_xref ( " \
               "user_id INTEGER, " \
               "url_id INTEGER," \
               "FOREIGN KEY (user_id) REFERENCES users(id)," \
               "FOREIGN KEY (url_id) REFERENCES urls(id) " \
               "PRIMARY KEY (user_id, url_id) );"
cursor.execute(create_table)

connection.commit()     # commit at the end only; no partial DB creation
connection.close()

print("~ Tables Created Successfully!")
print("Inserted one dummy user entry in DB.")
