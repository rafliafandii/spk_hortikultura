from cmath import phase
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

class Tanaman(db.Model):
    id                  = db.Column(db.Integer, unique=True, primary_key=True)
    nama_tanaman        = db.Column(db.String(50))
    ph                  = db.Column(db.Float)
    suhu                = db.Column(db.Integer)
    curah_hujan         = db.Column(db.Integer)
    ketinggian_tanah    = db.Column(db.Integer)