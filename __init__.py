from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import sqlite3
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')

def est_utilisateur_authentifie():
    return session.get('utilisateur_authentifie')

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        return redirect(url_for('authentification'))
    return "<h2>Bravo, vous êtes authentifié</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'password':
            session['authentifie'] = True
            return redirect(url_for('lecture'))
        elif request.form['username'] == 'user' and request.form['password'] == '12345':
            session['utilisateur_authentifie'] = True
            return redirect(url_for('hello_world'))
        else:
            return render_template('formulaire_authentification.html', error=True)
    
    return render_template('formulaire_authentification.html', error=False)

@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/fiche_nom/<nom>')
def search_by_name(nom):
    if not est_utilisateur_authentifie():
        return redirect(url_for('authentification'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE UPPER(nom) = UPPER(?)', (nom,))
    data = cursor.fetchall()
    conn.close()
    if data:
        return render_template('read_data.html', data=data)
    else:
        return "<h2>Aucun client trouvé avec ce nom.</h2>"

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')

@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')

# --------------------------------
# NOUVELLES ROUTES POUR LES LIVRES
# --------------------------------
@app.route('/livres', methods=['GET'])
def afficher_livres():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/livres', methods=['POST'])
def ajouter_livre():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    titre = request.form['titre']
    auteur = request.form['auteur']
    disponibilite = True

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO livres (titre, auteur, disponible) VALUES (?, ?, ?)', 
                   (titre, auteur, disponibilite))
    conn.commit()
    conn.close()
    return redirect('/livres')

@app.route('/livres/<int:id>', methods=['DELETE'])
def supprimer_livre(id):
    if not est_authentifie():
        return redirect(url_for('authentification'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM livres WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Livre supprimé avec succès'})

@app.route('/emprunter_livre/<int:id>', methods=['POST'])
def emprunter_livre(id):
    if not est_utilisateur_authentifie():
        return redirect(url_for('authentification'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT disponible FROM livres WHERE id = ?', (id,))
    livre = cursor.fetchone()

    if livre and livre[0]:  # Si le livre est disponible
        cursor.execute('UPDATE livres SET disponible = 0 WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Livre emprunté avec succès'})
    else:
        conn.close()
        return jsonify({'error': 'Le livre n\'est pas disponible ou inexistant'}), 404

@app.route('/rendre_livre/<int:id>', methods=['POST'])
def rendre_livre(id):
    if not est_utilisateur_authentifie():
        return redirect(url_for('authentification'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE livres SET disponible = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Livre rendu avec succès'})

if __name__ == "__main__":
    app.run(debug=True)
