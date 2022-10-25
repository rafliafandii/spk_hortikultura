''' 

SPK Metode AHP Untuk Pemilihan Tanaman
Keterangan : Data yang dihasilkan hanya angka, tidak ada nama tanaman

'''

from flask import render_template, redirect, request
from app import app
from app.models.tanaman import Tanaman

class AHP_edge():
    def __init__(self, ph, suhu, curah_hujan, ketinggian_tanah):
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
    
    @app.route("/ahp_edge/do_proses_edge")
    def do_proses_edge(self):
        self.siapkan_alternatif_edge()
        self.transformasi_edge()
        self.matriks_kriteria_edge()
        self.matriks_alternatif_edge()
        self.hitung_ranking_edge()

        return self.hasil_edge()
    
    @app.route("/ahp_edge/siapkan_alternatif_edge", methods = ['GET'])
    def siapkan_alternatif_edge(self):
        a = {}

        len_data = len(Tanaman.query.all())
        len_data = len_data + 1

        for i in range(1,len_data):
            a["ke{0}".format(i)] = []

            data = Tanaman.query.filter_by(id=i).first()
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
            if(curah_hujan >= 100 and curah_hujan <= 124):
                curah_hujan = 1
            elif(curah_hujan >= 125 and curah_hujan <= 149):
                curah_hujan = 2
            elif(curah_hujan >= 150 and curah_hujan <= 200):
                curah_hujan = 3
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

            a["ke" + str(i)].append(ph)
            a["ke" + str(i)].append(suhu)
            a["ke" + str(i)].append(curah_hujan)
            a["ke" + str(i)].append(ketinggian_tanah)

            self.daftar_tanaman.append(a["ke" + str(i)])

        return True
    
    @app.route("/ahp_edge/transformasi_edge")
    def transformasi_edge(self):
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
        if (curah_hujan >= 100 and curah_hujan <= 124):
            self.curah_hujan = 1
        elif (curah_hujan >= 125 and curah_hujan <= 149):
            self.curah_hujan = 2
        elif (curah_hujan >= 150 and curah_hujan <= 200):
            self.curah_hujan = 3
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

        kriteria = self.kriteria
        kriteria.append(self.ph)
        kriteria.append(self.suhu)
        kriteria.append(self.curah_hujan)
        kriteria.append(self.ketinggian_tanah)

        return True

    @app.route("/ahp_edge/matriks_kriteria_edge")
    def matriks_kriteria_edge(self):
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
    
    @app.route("/ahp_edge/matriks_alternatif_edge")
    def matriks_alternatif_edge(self):
        kriteria = self.kriteria
        daftar_tanaman = self.daftar_tanaman

        # variabel untuk menyimpan data tpv kedalam list
        alternatif = self.alternatif
        list_alternatif = self.list_alternatif

        # buat variabel untuk hasil alternatif
        for no in range(len(daftar_tanaman)):
            alternatif["a{0}".format(no)] = []

        # melakukan matriks perbandingan antar alternatif terhadap kriteria
        for no_kriteria in range(len(kriteria)):

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
    
    @app.route("/ahp_edge/hitung_ranking_edge")
    def hitung_ranking_edge(self):
        kriteria = self.kriteria
        daftar_tanaman = self.daftar_tanaman
        tpv = self.tpv
        list_alternatif = self.list_alternatif
        ranking = self.ranking

        for p in range(len(daftar_tanaman)):
            ranking["a{0}".format(p)] = 0

            for q in range(len(kriteria)):
                rank = list_alternatif[p][q] * tpv["c" + str(q)]
                ranking["a" + str(p)] += rank
        
        return True
        
    @app.route("/ahp_edge/hasil_edge")
    def hasil_edge(self):
        tpv = self.tpv
        cr = self.cr
        list_alternatif = self.list_alternatif
        ranking = self.ranking

        return render_template('hasil_ahp_edge.html', tpv=tpv, cr=cr, list_alternatif=list_alternatif, ranking=ranking)


@app.route("/index_edge", methods = ['GET'])
def index_edge():
    return render_template('index.html')

@app.route("/proses_hitung_edge", methods = ['GET', 'POST'])
def proses_hitung_edge():
    if request.method == 'POST':
        ph                  = request.form['ph']
        suhu                = request.form['suhu']
        curah_hujan         = request.form['curah_hujan']
        ketinggian_tanah    = request.form['ketinggian_tanah']
    
    ahp_edge= AHP_edge(ph, suhu, curah_hujan, ketinggian_tanah)
    
    return ahp_edge.do_proses_edge()