from app import get_db_connection

marque_nom = "Peugeot"
modele_nom = "308 I"
annee_debut = 2007
annee_fin = 2013

motorisations = [
    ("essence", "1.4L vti", "95-98", "non-fiable"),
    ("essence", "1.6L vti", "110-120", "non-fiable"),
    ("essence", "1.6L thp", "90", "non-fiable"),
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
cur.execute("SELECT id FROM marques WHERE nom = ?", (marque_nom,))
marque = cur.fetchone()
if not marque:
    cur.execute("INSERT INTO marques (nom) VALUES (?)", (marque_nom,))
    marque_id = cur.lastrowid
else:
    marque_id = marque["id"]

# Vérifier ou créer le modèle
cur.execute("SELECT id FROM modeles WHERE nom = ? AND marque_id = ?", (modele_nom, marque_id))
modele = cur.fetchone()
if not modele:
    cur.execute("INSERT INTO modeles (nom, marque_id, annee_debut, annee_fin) VALUES (?, ?, ?, ?)", 
                (modele_nom, marque_id, annee_debut, annee_fin))
    modele_id = cur.lastrowid
else:
    modele_id = modele["id"]
    # Mettre à jour les années si nécessaire
    cur.execute("UPDATE modeles SET annee_debut = ?, annee_fin = ? WHERE id = ?", 
                (annee_debut, annee_fin, modele_id))

# Ajouter les motorisations
for carburant, nom, puissance, fiabilite in motorisations:
    cur.execute("""
        SELECT id FROM motorisations
        WHERE modele_id = ? AND carburant = ? AND nom = ? AND puissance = ?
    """, (modele_id, carburant, nom, puissance))
    mot = cur.fetchone()
    if not mot:
        cur.execute("""
            INSERT INTO motorisations (modele_id, carburant, nom, puissance, fiabilite)
            VALUES (?, ?, ?, ?, ?)
        """, (modele_id, carburant, nom, puissance, fiabilite))

# Ajouter les finitions
for finition in finitions:
    cur.execute("SELECT id FROM finitions WHERE modele_id = ? AND nom = ?", (modele_id, finition))
    exists = cur.fetchone()
    if not exists:
        cur.execute("INSERT INTO finitions (modele_id, nom) VALUES (?, ?)", (modele_id, finition))

conn.commit()
cur.close()
conn.close()
