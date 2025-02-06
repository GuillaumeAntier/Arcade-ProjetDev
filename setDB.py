from database import Database

db = Database('database.sqlite')

db.create_table("test", "id INTEGER PRIMARY KEY, name TEXT, age INTEGER")