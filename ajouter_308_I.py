import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')  # Modifier le chemin si nécessaire
    conn.row_factory = sqlite3.Row
    return conn

marque_nom = "Peugeot"
modele_nom = "308 I"
annee_debut = 2007
annee_fin = 2013

motorisations = [
    ("essence", "1.4L vti", "95-98", "non-fiable"),
    ("essence", "1.6L vti", "110-120", "non-fiable"),
    ("essence", "1.6L thp", "110-200", "non-fiable"),
    ("diesel", "1.6L", "90-115", "fiable"),
    ("diesel", "2.0L hdi", "136-165", "fiable"),
]

finitions = [
    "acces", "active", "style", "allure",
    "premium pack", "sport", "sport pack", "sportium", "feline"
]

conn = get_db_connection()
cur = conn.cursor()

# Vérifier ou créer la marque
cur.execute("SELECT id FROM marque WHERE nom = ?", (marque_nom,))
marque = cur.fetchone()
if not marque:
    cur.execute("INSERT INTO marque (nom) VALUES (?)", (marque_nom,))
    marque_id = cur.lastrowid
else:
    marque_id = marque["id"]

# Vérifier ou créer le modèle
cur.execute("SELECT id FROM modele WHERE nom = ? AND marque_id = ?", (modele_nom, marque_id))
modele = cur.fetchone()
if not modele:
    cur.execute("INSERT INTO modele (nom, marque_id, annee_debut, annee_fin) VALUES (?, ?, ?, ?)", 
                (modele_nom, marque_id, annee_debut, annee_fin))
    modele_id = cur.lastrowid
else:
    modele_id = modele["id"]
    cur.execute("UPDATE modele SET annee_debut = ?, annee_fin = ? WHERE id = ?", 
                (annee_debut, annee_fin, modele_id))

# Ajouter les motorisations
for type_, nom, puissance, fiabilite in motorisations:
    cur.execute("""
        SELECT id FROM motorisation
        WHERE modele_id = ? AND type = ? AND nom = ? AND puissance = ?
    """, (modele_id, type_, nom, puissance))
    mot = cur.fetchone()
    if not mot:
        cur.execute("""
            INSERT INTO motorisation (modele_id, type, nom, puissance, fiabilite)
            VALUES (?, ?, ?, ?, ?)
        """, (modele_id, type_, nom, puissance, fiabilite))

# Ajouter les finitions
for finition in finitions:
    cur.execute("SELECT id FROM finition WHERE modele_id = ? AND nom = ?", (modele_id, finition))
    exists = cur.fetchone()
    if not exists:
        cur.execute("INSERT INTO finition (modele_id, nom) VALUES (?, ?)", (modele_id, finition))

conn.commit()
cur.close()
conn.close()
