from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    favoris = db.relationship('Favori', backref='user', lazy=True)

class Marque(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)
    modeles = db.relationship('Modele', backref='marque', lazy=True)

class Modele(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    annee = db.Column(db.String(10))
    motorisation = db.Column(db.String(100))
    consommation = db.Column(db.String(50))
    fiabilite = db.Column(db.String(100))
    description = db.Column(db.Text)
    marque_id = db.Column(db.Integer, db.ForeignKey('marque.id'), nullable=False)
    favoris = db.relationship('Favori', backref='modele', lazy=True)

class Favori(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    modele_id = db.Column(db.Integer, db.ForeignKey('modele.id'), nullable=False)
