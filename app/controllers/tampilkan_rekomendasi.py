from flask import redirect, render_template, request, request_started
from app import app
from app.models.rekomendasi import Rekomendasi

class Tampilkan_rekomendasi:
    @app.route("/tampilkan_rekomendasi")
    def tampilkan_rekomendasi():
        rekomendasi = Rekomendasi.query.all()

        return render_template('tampilkan_rekomendasi.html', data=enumerate(rekomendasi,1))