from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessionm

# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')

def est_utilisateur_authentifie():
    return session.get('utilisateur_authentifie')

@app.route('/')
def accueil():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom FROM marque")
    marques = cursor.fetchall()
    conn.close()
    return render_template('hello.html', marques=marques)

@app.route("/marque/<int:id>")
def afficher_modele_par_marque(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT nom FROM marque WHERE id = ?", (id,))
    marque = cursor.fetchone()

    if not marque:
        return "<h2>Marque introuvable.</h2>"

    cursor.execute("SELECT id, nom FROM modele WHERE marque_id = ?", (id,))
    modeles = cursor.fetchall()
    conn.close()
    return render_template("modeles.html", marque=marque[0], modeles=modeles)

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

@app.route('/ajouter', methods=['GET', 'POST'])
def ajouter_modele():
    if request.method == 'POST':
        nom = request.form['nom']
        annee = request.form['annee']
        motorisation = request.form['motorisation']
        consommation = request.form['consommation']
        fiabilite = request.form['fiabilite']
        description = request.form['description']
        marque_id = request.form['marque_id']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO modele 
            (nom, annee, motorisation, consommation, fiabilite, description, marque_id) 
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (nom, annee, motorisation, consommation, fiabilite, description, marque_id)
        )
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, nom FROM marque")
        marques = cursor.fetchall()
        conn.close()
        return render_template("formulaire.html", marques=marques)


                                                                                                                                       
if __name__ == "__main__":
  app.run(debug=True)




