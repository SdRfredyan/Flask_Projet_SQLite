import sqlite3

# Connexion à la base
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Marques à conserver
marques_a_conserver = ('Peugeot', 'Citroën', 'Renault', 'BMW', 'Audi', 'DS', 'Volkswagen')

# Récupérer les IDs des marques à conserver
cursor.execute("SELECT id FROM marque WHERE nom IN (?, ?, ?, ?, ?, ?, ?)", marques_a_conserver)
ids_a_conserver = [row[0] for row in cursor.fetchall()]

# Supprimer les modèles qui appartiennent à des marques à supprimer
cursor.execute("DELETE FROM modele WHERE marque_id NOT IN ({})".format(
    ','.join('?' for _ in ids_a_conserver)), ids_a_conserver)

# Supprimer les marques à exclure
cursor.execute("DELETE FROM marque WHERE nom NOT IN ({})".format(
    ','.join('?' for _ in marques_a_conserver)), marques_a_conserver)

# Commit & close
conn.commit()
conn.close()

print("Nettoyage terminé. Marques conservées :", ', '.join(marques_a_conserver))
