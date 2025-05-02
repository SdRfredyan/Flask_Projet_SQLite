from flask import Flask, render_template
import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ma-cle-secrete'

models.db.init_app(app)

@app.route('/')
def accueil():
    with app.app_context():
        marques = models.Marque.query.all()
    return render_template('hello.html', marques=marques)
