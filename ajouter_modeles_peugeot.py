import sqlite3

modeles = [
    "206", "308 I", "308 II", "308 III", "508 I", "208 II", "208 I",
    "307", "207", "3008 III", "5008 III", "408", "306", "406",
    "508 II", "407", "2008 I", "3008 II"
]

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Récupère l'ID de la marque Peugeot
cursor.execute("SELECT id FROM marque WHERE nom = ?", ("Peugeot",))
result = cursor.fetchone()

if result:
    marque_id = result[0]

    # Supprimer les doublons (mêmes noms pour la même marque, garder le plus petit id)
    cursor.execute("""
        DELETE FROM modele
        WHERE id NOT IN (
            SELECT MIN(id)
            FROM modele
            WHERE marque_id = ?
            GROUP BY nom
        ) AND marque_id = ?
    """, (marque_id, marque_id))
    print("Doublons supprimés pour Peugeot.")

    # Ajouter les modèles s'ils n'existent pas déjà
    for nom in modeles:
        cursor.execute("SELECT id FROM modele WHERE nom = ? AND marque_id = ?", (nom, marque_id))
        if cursor.fetchone() is None:
            cursor.execute(
                "INSERT INTO modele (nom, marque_id) VALUES (?, ?)",
                (nom, marque_id)
            )

    conn.commit()
    print("Modèles Peugeot ajoutés sans doublons.")
else:
    print("Erreur : Marque Peugeot introuvable.")

conn.close()
