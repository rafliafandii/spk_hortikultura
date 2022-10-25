from cmath import phase
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from app import app

db = SQLAlchemy(app)

class Rekomendasi(db.Model):
    id                  = db.Column(db.Integer, unique=True, primary_key=True)
    bulan               = db.Column(db.String(50))
    ph                  = db.Column(db.Float)
    ketinggian_tanah    = db.Column(db.Integer)
    tanaman_1           = db.Column(db.String(50))
    tanaman_2           = db.Column(db.String(50))
    tanaman_3           = db.Column(db.String(50))