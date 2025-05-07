import sqlite3

marques = [
    "Peugeot", "Citroën", "Renault", "BMW", "Audi", "DS", "Volkswagen"
]

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

for marque in marques:
    cursor.execute("INSERT INTO marque (nom) VALUES (?)", (marque,))

conn.commit()
conn.close()

print("Marques insérées avec succès.")
