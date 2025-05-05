import sqlite3
import os

os.makedirs("instance", exist_ok=True)
conn = sqlite3.connect("database.db")

with open("schema.sql", "r") as f:
    conn.executescript(f.read())

conn.commit()
conn.close()
print("✅ Base de données créée.")
