import sqlite3

modeles = [
    "206","308 I" "308 II", "308 III", "508 I", "208 II", "208 I", "307", "207",
    "3008 III", "5008 III", "408", "306", "406", "508 II", "407", "2008 I", "3008 II"
]

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Récupérer l'ID de la marque Peugeot
cursor.execute("SELECT id FROM marque WHERE nom = ?", ("Peugeot",))
result = cursor.fetchone()

if result:
    marque_id = result[0]
    for nom in modeles:
        cursor.execute(
            "INSERT INTO modele (nom, marque_id) VALUES (?, ?)",
            (nom, marque_id)
        )
    conn.commit()
    print("Modèles Peugeot ajoutés.")
else:
    print("Erreur : Marque Peugeot introuvable.")

conn.close()
