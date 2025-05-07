import sqlite3

with open("schema.sql") as f:
    sql = f.read()

conn = sqlite3.connect("database.db")
cursor = conn.cursor()
cursor.executescript(sql)
conn.commit()
conn.close()

print("Base de données créée avec succès.")
