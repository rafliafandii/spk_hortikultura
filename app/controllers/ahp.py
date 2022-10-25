''' 

SPK Metode AHP Untuk Pemilihan Tanaman
Keterangan : Data yang dihasilkan lengkap dengan nama tanaman

'''

from flask import render_template, redirect, request
from app import app
from app.models.tanaman import Tanaman
from app.models.rekomendasi import db, Rekomendasi

class AHP():
    def __init__(self, bulan, ph, suhu, curah_hujan, ketinggian_tanah):
        self.bulan = bulan
        self.ph = float(ph)
        self.suhu = int(suhu)
        self.curah_hujan = int(curah_hujan)
        self.ketinggian_tanah = int(ketinggian_tanah)
        self.daftar_tanaman = []

        self.kriteria = []
        self.tpv = {}
        self.cr = 0
        self.alternatif = {}
        self.list_alternatif = []
        self.ranking = {}

        # untuk disimpan kedalam tabel rekomendasi
        self.untuk_ph = float(ph)
        self.untuk_ketinggian_tanah = int(ketinggian_tanah)
        self.rekomendasi = []
    
    @app.route("/ahp/do_proses")
    def do_proses(self):
        self.siapkan_alternatif()
        self.transformasi()
        self.matriks_kriteria()
        self.matriks_alternatif()
        self.hitung_ranking()
        self.hasil()

        return redirect("/kelola_rekomendasi")
    
    @app.route("/ahp/siapkan_alternatif", methods = ['GET'])
    def siapkan_alternatif(self):
        a = {}

        len_data = len(Tanaman.query.all())
        len_data = len_data + 1

        for i in range(1,len_data):
            a["ke{0}".format(i)] = []

            data = Tanaman.query.filter_by(id=i).first()
            nama_tanaman = data.nama_tanaman
            ph = data.ph
            suhu = data.suhu
            curah_hujan = data.curah_hujan
            ketinggian_tanah = data.ketinggian_tanah

            # merubah nilai ph
            if(ph >= 5.5 and ph <= 5.9):
                ph = 1
            elif(ph >= 6.0 and ph <= 6.4):
                ph = 2
            elif(ph >= 6.5 and ph <= 7.0):
                ph = 3
            else:
                ph = 0
            
            # merubah nilai suhu
            if(suhu >= 15 and suhu <= 19):
                suhu = 1
            elif(suhu >= 20 and suhu <= 24):
                suhu = 2
            elif(suhu >= 25 and suhu <= 29):
                suhu = 3
            elif(suhu >= 30 and suhu <=35):
                suhu = 4
            else:
                suhu = 0
            
            # merubah nilai curah hujan
            if(curah_hujan >= 0 and curah_hujan <= 99):
                curah_hujan = 1
            elif(curah_hujan >= 100 and curah_hujan <= 199):
                curah_hujan = 2
            elif(curah_hujan >= 200 and curah_hujan <= 299):
                curah_hujan = 3
            elif(curah_hujan >= 300 and curah_hujan <= 399):
                curah_hujan = 4
            elif(curah_hujan >= 400 and curah_hujan <= 499):
                curah_hujan = 5
            elif(curah_hujan >= 500 and curah_hujan <= 599):
                curah_hujan = 6
            else:
                curah_hujan = 0
            
            # merubah nilai ketinggian tanah
            if(ketinggian_tanah >= 400 and ketinggian_tanah <= 799):
                ketinggian_tanah = 1
            elif(ketinggian_tanah >= 800 and ketinggian_tanah <= 1199):
                ketinggian_tanah = 2
            elif(ketinggian_tanah >= 1200 and ketinggian_tanah <= 1600):
                ketinggian_tanah = 3
            else:
                ketinggian_tanah = 0

            # masukan data kedalam list
            a["ke" + str(i)].append(nama_tanaman)
            a["ke" + str(i)].append(ph)
            a["ke" + str(i)].append(suhu)
            a["ke" + str(i)].append(curah_hujan)
            a["ke" + str(i)].append(ketinggian_tanah)

            self.daftar_tanaman.append(a["ke" + str(i)])

        return True
    
    @app.route("/ahp/transformasi")
    def transformasi(self):
        ph = self.ph
        suhu = self.suhu
        curah_hujan = self.curah_hujan
        ketinggian_tanah = self.ketinggian_tanah

        # merubah nilai pH
        if (ph >= 5.5 and ph <= 5.9):
            self.ph = 1
        elif (ph >= 6.0 and ph <= 6.4):
            self.ph = 2
        elif (ph >= 6.5 and ph <= 7.0):
            self.ph = 3
        else:
            self.ph = 0

        # merubah nilai suhu
        if (suhu >= 15 and suhu <= 19):
            self.suhu = 1
        elif (suhu >= 20 and suhu <= 24):
            self.suhu = 2
        elif (suhu >= 25 and suhu <= 29):
            self.suhu = 3
        elif (suhu >= 30 and suhu <= 35):
            self.suhu = 4
        else:
            self.suhu = 0

        # merubah nilai curah hujan
        if (curah_hujan >= 0 and curah_hujan <= 99):
            self.curah_hujan = 1
        elif (curah_hujan >= 100 and curah_hujan <= 199):
            self.curah_hujan = 2
        elif (curah_hujan >= 200 and curah_hujan <= 299):
            self.curah_hujan = 3
        elif (curah_hujan >= 300 and curah_hujan <= 399):
            self.curah_hujan = 4
        elif (curah_hujan >= 400 and curah_hujan <= 499):
            self.curah_hujan = 5
        elif (curah_hujan >= 500 and curah_hujan <= 599):
            self.curah_hujan = 6
        else:
            self.curah_hujan = 0

        # merubah nilai ketinggian tanah
        if (ketinggian_tanah >= 400 and ketinggian_tanah <= 799):
            self.ketinggian_tanah = 1
        elif (ketinggian_tanah >= 800 and ketinggian_tanah <= 1199):
            self.ketinggian_tanah = 2
        elif (ketinggian_tanah >= 1200 and ketinggian_tanah <= 1600):
            self.ketinggian_tanah = 3
        else:
            self.ketinggian_tanah = 0

        # masukan data kedalam list
        kriteria = self.kriteria
        kriteria.append(self.ph)
        kriteria.append(self.suhu)
        kriteria.append(self.curah_hujan)
        kriteria.append(self.ketinggian_tanah)

        return True

    @app.route("/ahp/matriks_kriteria")
    def matriks_kriteria(self):
        kriteria = self.kriteria

        # melakukan matriks perbandingan antar kriteria
        c = {}
        hasil_banding = []

        for i in range(len(kriteria)):
            # buat variabel baru (c[c0], c[c1], c[c2], c[c3])
            c["c{0}".format(i)] = []

            for j in range(len(kriteria)):
                a = kriteria[i] / kriteria[j]
                c["c" + str(i)].append(a)

            hasil_banding.append(c["c" + str(i)])

        # menjumlahkan tiap kolom hasil matriks perbandingan
        kolom = {}

        for k in range(len(c)):
            kolom["c{0}".format(k)] = 0

            for l in range(len(c)):
                b = hasil_banding[l][k]
                kolom["c" + str(k)] += b

        # normalisasi
        cn = {}
        hasil_normalisasi = []

        for m in range(len(kriteria)):
            # buat variabel baru (cn[c0], c[c1], c[c2], c[c3])
            cn["c{0}".format(m)] = []

            for n in range(len(kriteria)):
                d = hasil_banding[m][n] / kolom["c" + str(n)]
                cn["c" + str(m)].append(d)

            hasil_normalisasi.append(cn["c" + str(m)])

        # menjumlahkan baris hasil normalisasi
        baris = {}

        for x in range(len(cn)):
            baris["c{0}".format(x)] = 0

            for y in range(len(cn)):
                e = hasil_normalisasi[x][y]
                baris["c" + str(x)] += e

        # mencari nilai TPV masing-masing kriteria
        tpv = self.tpv

        for n in range(len(baris)):
            tpv["c{0}".format(n)] = 0
            tpv["c" + str(n)] = baris["c" + str(n)] / len(kriteria)

        # matriks perbandingan berpasangan untuk consistency ratio
        ccr = {}
        hasil_banding_tpv = []

        for i in range(len(kriteria)):
            # buat variabel baru (ccr[c0], ccr[c1], ccr[c2], ccr[c3])
            ccr["c{0}".format(i)] = []

            for j in range(len(kriteria)):
                f = hasil_normalisasi[i][j] * tpv["c" + str(j)]
                ccr["c" + str(i)].append(f)

            hasil_banding_tpv.append(ccr["c" + str(i)])

        # penjumlahan baris matriks perbandingan
        baris_ccr = {}

        for k in range(len(ccr)):
            baris_ccr["c{0}".format(k)] = 0

            for l in range(len(ccr)):
                g = hasil_banding_tpv[k][l]
                baris_ccr["c" + str(k)] += g

        # mencari nilai lambda max
        hasil = {}
        total_hasil = 0

        for m in range(len(baris_ccr)):
            hasil["c{0}".format(m)] = 0
            hasil["c" + str(m)] = baris_ccr["c" + str(m)] + tpv["c" + str(m)]
            total_hasil += hasil["c" + str(m)]

        lambda_max = total_hasil / len(kriteria)

        # mencari nilai consistency index
        ci = (lambda_max - len(kriteria)) / len(kriteria)

        # mencari nilai consistency ratio
        ir = 0
        if (len(kriteria) == 1 and len(kriteria) <= 2):
            ir = 0
        elif (len(kriteria) == 3):
            ir = 0.58
        elif (len(kriteria) == 4):
            ir = 0.90
        elif (len(kriteria) == 5):
            ir = 1.12
        elif (len(kriteria) == 6):
            ir = 1.24
        elif (len(kriteria) == 7):
            ir = 1.32
        elif (len(kriteria) == 8):
            ir = 1.41
        elif (len(kriteria) == 9):
            ir = 1.45
        else:
            1.49

        cr = ci / ir
        self.cr = cr

        return True
    
    @app.route("/ahp/matriks_alternatif")
    def matriks_alternatif(self):
        kriteria = self.kriteria
        daftar_tanaman = self.daftar_tanaman
        len_kriteria = len(kriteria) + 1

        # variabel untuk menyimpan data tpv kedalam list
        alternatif = self.alternatif
        list_alternatif = self.list_alternatif

        # buat variabel untuk hasil alternatif dan masukan nama tanaman
        for no in range(len(daftar_tanaman)):
            alternatif["a{0}".format(no)] = []
            alternatif["a" + str(no)].append(daftar_tanaman[no][0])

        # melakukan matriks perbandingan antar alternatif terhadap kriteria
        for no_kriteria in range(1, len_kriteria):

            matriks_a = {}
            hasil_banding_a = []

            # melakukan matriks perbandingan
            for i in range(len(daftar_tanaman)):
                matriks_a["a{0}".format(i)] = []

                for j in range(len(daftar_tanaman)):
                    m_a = daftar_tanaman[i][no_kriteria] / daftar_tanaman[j][no_kriteria]
                    matriks_a["a" + str(i)].append(m_a)

                hasil_banding_a.append(matriks_a["a" + str(i)])

            # menjumlahkan tiap kolom hasil matriks perbandingan
            kolom_a = {}

            for k in range(len(daftar_tanaman)):
                kolom_a["a{0}".format(k)] = 0

                for l in range(len(daftar_tanaman)):
                    kol = hasil_banding_a[l][k]
                    kolom_a["a" + str(k)] += kol

            # normalisasi matriks perbandingan
            matriks_n = {}
            hasil_normalisasi_a = []

            for m in range(len(daftar_tanaman)):
                matriks_n["a{0}".format(m)] = []

                for n in range(len(daftar_tanaman)):
                    n_m = hasil_banding_a[m][n] / kolom_a["a" + str(n)]
                    matriks_n["a" + str(m)].append(n_m)

                hasil_normalisasi_a.append(matriks_n["a" + str(m)])

            # menjumlahkan baris hasil normalisasi
            baris_n = {}

            for x in range(len(daftar_tanaman)):
                baris_n["a{0}".format(x)] = 0

                for y in range(len(daftar_tanaman)):
                    b_n = hasil_normalisasi_a[x][y]
                    baris_n["a" + str(x)] += b_n

            # mencari nilai tpv masing-masing alternatif
            for n in range(len(baris_n)):
                tpv_a = baris_n["a" + str(n)] / len(daftar_tanaman)
                alternatif["a" + str(n)].append(tpv_a)

        # masukan hasil alternatif kedalam list
        for j in range(len(daftar_tanaman)):
            list_alternatif.append(alternatif["a" + str(j)])
        
        return True

    @app.route("/ahp/hitung_ranking")
    def hitung_ranking(self):
        kriteria = self.kriteria
        daftar_tanaman = self.daftar_tanaman
        tpv = self.tpv
        list_alternatif = self.list_alternatif
        ranking = self.ranking

        for p in range(len(daftar_tanaman)):
            ranking["a{0}".format(p)] = ['nama_tanaman', 0]
            ranking["a" + str(p)][0] = daftar_tanaman[p][0]

            for q in range(len(kriteria)):
                rank = list_alternatif[p][q + 1] * tpv["c" + str(q)]
                ranking["a" + str(p)][1] += rank

        return True

    @app.route("/ahp/hasil")
    def hasil(self):
        tpv = self.tpv
        cr = self.cr
        list_alternatif = self.list_alternatif

        bulan = self.bulan
        ranking = self.ranking
        list_ranking = []
        
        for x in range(len(ranking)):
            list_ranking.append(ranking["a" + str(x)])

        sorted_ranking = sorted(list_ranking, key=lambda x: x[1], reverse=True)

        rekomendasi = self.rekomendasi

        for y in range(3):
            rekomendasi.append(sorted_ranking[y][0])
        
        # masukan data ke tabel ranking
        try:
            rekomendasi = Rekomendasi(bulan=bulan, ph=self.untuk_ph, ketinggian_tanah=self.untuk_ketinggian_tanah, tanaman_1=rekomendasi[0], tanaman_2=rekomendasi[1], tanaman_3=rekomendasi[2])
            db.session.add(rekomendasi)
            db.session.commit()

            return True
        except:
            return False
        
        # return render_template('hasil.html', tpv=tpv, cr=cr, list_alternatif=list_alternatif, ranking=sorted_ranking, rekomendasi=rekomendasi)
        

@app.route("/spk", methods = ['GET'])
def spk():
    daftar_tanaman = Tanaman.query.all()
    print(daftar_tanaman)
    return render_template('spk.html', daftar_tanaman=enumerate(daftar_tanaman,1))

@app.route("/proses_hitung", methods = ['GET', 'POST'])
def proses_hitung():
    if request.method == 'POST':
        bulan               = request.form['bulan']
        ph                  = request.form['ph']
        suhu                = request.form['suhu']
        curah_hujan         = request.form['curah_hujan']
        ketinggian_tanah    = request.form['ketinggian_tanah']
    
    ahp = AHP(bulan, ph, suhu, curah_hujan, ketinggian_tanah)
    
    return ahp.do_proses()