import sqlite3

modeles_peugeot = [
    "206", "308 II", "308 III", "508 I", "208 II", "208 I", "307", "207",
    "3008 III", "5008 III", "408", "306", "406", "508 II", "407", "2008 I", "3008 II"
]

# 🔁 Modifier le chemin si besoin (selon ton projet)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

for modele in modeles_peugeot:
    cursor.execute("SELECT 1 FROM modele WHERE nom = ? AND marque_id = ?", (modele, 1))
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO modele (nom, marque_id) VALUES (?, ?)", (modele, 1))

conn.commit()
conn.close()
print("✅ Modèles Peugeot ajoutés sans doublons.")
