from flask import redirect, render_template, request, request_started
from app import app
from app.models.rekomendasi import db, Rekomendasi

class Kelola_rekomendasi:
    @app.route("/kelola_rekomendasi")
    def kelola_rekomendasi():
        rekomendasi = Rekomendasi.query.all()

        return render_template('kelola_rekomendasi.html', data=enumerate(rekomendasi,1))
    
    @app.route('/kelola_rekomendasi/hapus_data_rekomendasi/<int:id>')
    def hapus_data_rekomendasi(id):
        try:
            rekomendasi = Rekomendasi.query.filter_by(id=id).first()

            db.session.delete(rekomendasi)
            db.session.commit()

            return redirect("/kelola_rekomendasi")
        except:
            return redirect("/kelola_rekomendasi")