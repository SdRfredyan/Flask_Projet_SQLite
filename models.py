from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Marque(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)
