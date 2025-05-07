import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Insérer ou récupérer l'id de la marque Peugeot
cursor.execute("SELECT id FROM marque WHERE nom = ?", ("Peugeot",))
row = cursor.fetchone()
if row:
    marque_id = row[0]
else:
    cursor.execute("INSERT INTO marque (nom) VALUES (?)", ("Peugeot",))
    marque_id = cursor.lastrowid

# Insérer ou récupérer le modèle 206
cursor.execute("SELECT id FROM modele WHERE nom = ? AND marque_id = ?", ("206", marque_id))
row = cursor.fetchone()
if row:
    modele_id = row[0]
else:
    cursor.execute("""
        INSERT INTO modele (nom, annee_debut, annee_fin, description, marque_id)
        VALUES (?, ?, ?, ?, ?)
    """, ("206", 1998, 2006, "Citadine emblématique de Peugeot", marque_id))
    modele_id = cursor.lastrowid

# Liste des motorisations
motorisations = [
    ("essence", "1.1L", "60", "fiable"),
    ("essence", "1.4L", "75", "fiable"),
    ("essence", "1.4L 16v", "90", "fiable"),
    ("essence", "1.6L", "90", "fiable"),
    ("essence", "1.6L 16v", "110", "fiable"),
    ("essence", "2.0L S16", "135-165", "fiable"),
    ("diesel", "1.9L D", "70", "fiable"),
    ("diesel", "1.4L HDi", "70", "fiable"),
    ("diesel", "2.0L HDi", "90", "fiable"),
    ("diesel", "1.6L HDi", "110", "fiable")
]

for type_, nom, puissance, fiabilite in motorisations:
    cursor.execute("""
        SELECT id FROM motorisation
        WHERE modele_id = ? AND type = ? AND nom = ?
    """, (modele_id, type_, nom))
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO motorisation (modele_id, type, nom, puissance, fiabilite)
            VALUES (?, ?, ?, ?, ?)
        """, (modele_id, type_, nom, puissance, fiabilite))

# Liste des finitions
finitions = [
    "CC", "RC", "S16", "Roland Garros", "XR", "XT",
    "X-Line", "QuickSilver", "Pop Art", "Urbain", "Trendy"
]

for nom in finitions:
    cursor.execute("SELECT id FROM finition WHERE modele_id = ? AND nom = ?", (modele_id, nom))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO finition (modele_id, nom) VALUES (?, ?)", (modele_id, nom))

conn.commit()
conn.close()
print("✅ Modèle 206, motorisations et finitions insérés sans doublons.")
