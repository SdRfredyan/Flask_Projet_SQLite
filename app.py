import os
from flask import Flask
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URI", "sqlite:///database.db")
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "dev-key")
db.init_app(app)
