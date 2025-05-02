from flask import Flask, render_template
from models import db, Marque

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'votre-cle-secrete'

db.init_app(app)

@app.route('/')
def accueil():
    marques = Marque.query.all()
    return render_template('hello.html', marques=marques)
