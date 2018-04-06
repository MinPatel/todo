import sqlite3

connection = sqlite3.connect("todo.db")
cursor = connection.cursor()

query = "CREATE TABLE IF NOT EXISTS Tasks(Desc text, Detail text)"

cursor.execute(query)
connection.commit()
connection.close()