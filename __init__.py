from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3


app = Flask(__name__)

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

@app.route("/modele/<int:id>")
def detail_modele(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Récupérer les infos du modèle
    cursor.execute("SELECT nom, annee_debut, annee_fin FROM modele WHERE id = ?", (id,))
    modele = cursor.fetchone()
    if not modele:
        return "<h2>Modèle introuvable.</h2>"

    nom, annee_debut, annee_fin = modele

    # Récupérer les motorisations (séparées par type)
    cursor.execute("""
        SELECT type, nom, puissance, fiabilite 
        FROM motorisation 
        WHERE modele_id = ?
    """, (id,))
    motorisations = cursor.fetchall()
    moteurs = {"essence": [], "diesel": [], "hybride": []}
    for m in motorisations:
        moteurs[m[0]].append({
            "nom": m[1],
            "puissance": m[2],
            "fiabilite": m[3]
        })

    # Récupérer les finitions
    cursor.execute("SELECT nom FROM finition WHERE modele_id = ?", (id,))
    finitions = [row[0] for row in cursor.fetchall()]

    conn.close()

    return render_template("modele_detail.html", nom=nom,annee_debut=annee_debut, annee_fin=annee_fin,moteurs=moteurs,finitions=finitions)

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




