from flask import redirect, render_template, request, request_started
from app import app
from app.models.tanaman import db, Tanaman

class Kelola_data:
    @app.route('/kelola_data/tambah_data', methods=['GET', 'POST'])
    def tambah_data():
        if request.method == 'POST':
            nama_tanaman        = request.form['nama_tanaman']
            ph                  = request.form['ph']
            suhu                = request.form['suhu']
            curah_hujan         = request.form['curah_hujan']
            ketinggian_tanah    = request.form['ketinggian_tanah']

            try:
                tanaman = Tanaman(nama_tanaman=nama_tanaman, ph=ph, suhu=suhu, curah_hujan=curah_hujan, ketinggian_tanah=ketinggian_tanah)
                db.session.add(tanaman)
                db.session.commit()
                
                return redirect("/kelola_data/tambah_data")
            except:
                return redirect("/kelola_data/tambah_data")

        daftar_tanaman = Tanaman.query.all()
        print(daftar_tanaman)

        return render_template('tambah_data.html', data=enumerate(daftar_tanaman,1))
    
    @app.route('/kelola_data/ubah_data/<int:id>')
    def ubah_data(id):
        tanaman = Tanaman.query.filter_by(id=id).first()

        return render_template("ubah_data.html", tanaman=tanaman)
    
    @app.route('/kelola_data/aksi_ubah_data', methods=['POST'])
    def aksi_ubah_data():
        if request.method == 'POST':
            id = request.form['id']
            nama_tanaman = request.form['nama_tanaman']
            ph = request.form['ph']
            suhu = request.form['suhu']
            curah_hujan = request.form['curah_hujan']
            ketinggian_tanah = request.form['ketinggian_tanah']

            try:
                tanaman = Tanaman.query.filter_by(id=id).first()
                tanaman.nama_tanaman = nama_tanaman
                tanaman.ph = ph
                tanaman.suhu = suhu
                tanaman.curah_hujan = curah_hujan
                tanaman.ketinggian_tanah = ketinggian_tanah
            
                db.session.commit()

                return redirect("/kelola_data/tambah_data")
            except:
                return redirect("/kelola_data/tambah_data")
    
    @app.route('/kelola_data/hapus_data/<int:id>')
    def hapus_data(id):
        try:
            tanaman = Tanaman.query.filter_by(id=id).first()

            db.session.delete(tanaman)
            db.session.commit()

            return redirect("/kelola_data/tambah_data")
        except:
            return redirect("/kelola_data/tambah_data")