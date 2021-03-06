"""Program ini adalah program optimasi penjadwalan mata kuliah di STAIMA Al-Hikam Malang
menggunakan Hybrid Discrete PSO
    IMPORT EXCEL"""
# pylint: disable=cell-var-from-loop, too-many-locals

from itertools import chain
from collections import Counter
import random
import math
import operator
import copy
import numpy as np
import pandas as pd
import time

start_time = time.time()

class Penjadwalan:
    """Kelas untuk penjadwalan menggunakan HDPSO"""
    def __init__(self):
        self.bglob = 0
        self.bloc = 0
        self.brand = 0
        self.dosen = [[]]
        self.fitness = []
        self.fitness_gbest = 0
        self.ganda = [[]]
        self.gbest = []
        self.hari = []
        self.kelas = [[]]
        self.limit = 0
        self.n_posisi = 0
        self.pbest = [[]]
        self.pelajaran = [[]]
        self.periode = 0
        self.posisi = [[]]
        self.rglob = 0
        self.rloc = 0
        self.rrand = 0
        self.ruangan = []
        self.size = 0
        self.sks = [[]]

    def set_bglob(self, bglob):
        """Ganti bglob"""
        self.bglob = bglob

    def set_bloc(self, bloc):
        """Ganti bloc"""
        self.bloc = bloc

    def set_brand(self, brand):
        """Ganti brand"""
        self.brand = brand

    def get_bglob(self):
        """Ambil bglob"""
        return self.bglob

    def get_bloc(self):
        """Ambil bloc"""
        return self.bloc

    def get_brand(self):
        """Ambil brand"""
        return self.brand

    def set_dosen(self, dosen):
        """Ganti Dosen"""
        self.dosen = dosen

    def get_dosen(self):
        """Ambil data dosen"""
        return self.dosen

    def set_fitness(self, fitness):
        """Ubah Fitness"""
        self.fitness = fitness

    def get_fitness(self):
        """Ambil Fitness"""
        return self.fitness

    def set_fitness_gbest(self, fitness_gbest):
        """Ubah Fitness Gbest"""
        self.fitness_gbest = fitness_gbest

    def get_fitness_gbest(self):
        """Ambil Fitness Gbest"""
        return self.fitness_gbest

    def set_ganda(self, ganda):
        """Ubah Ganda"""
        self.ganda = ganda

    def get_ganda(self):
        """Ambil pelajaran yang 2 kali pertemuan"""
        return self.ganda

    def set_gbest(self, gbest):
        """Ubah Gbest"""
        self.gbest = gbest

    def get_gbest(self):
        """Ambil Gbest"""
        return self.gbest

    def set_hari(self, hari):
        """Ubah Hari"""
        self.hari = hari

    def get_hari(self):
        """Ambil Hari"""
        return self.hari

    def set_kelas(self, kelas):
        """Ubah Kelas"""
        self.kelas = kelas

    def get_kelas(self):
        """Ambil data kelas"""
        return self.kelas

    def set_limit(self, limit):
        """Ganti Batas Iterasi"""
        self.limit = limit

    def get_limit(self):
        """Ambil Limit"""
        return self.limit

    def set_n_posisi(self, n_posisi):
        """Ubah Jumlah Posisi"""
        self.n_posisi = n_posisi

    def get_n_posisi(self):
        """Ambil banyak dimensi"""
        return self.n_posisi

    def set_pbest(self, pbest):
        """Ganti Pbest"""
        self.pbest = pbest

    def get_pbest(self):
        """Ambil Pbest"""
        return self.pbest

    def set_pelajaran(self, pelajaran):
        """Ganti Pelajaran"""
        self.pelajaran = pelajaran

    def get_pelajaran(self):
        """Ambil Pelajaran"""
        return self.pelajaran

    def set_periode(self, periode):
        """Ganti Periode"""
        self.periode = periode

    def get_periode(self):
        """Ambil Periode"""
        return self.periode

    def set_posisi(self, posisi):
        """Ganti posisi"""
        self.posisi = posisi

    def get_posisi(self):
        """Ambil posisi"""
        return self.posisi

    def set_rglob(self, rglob):
        """Ganti rglob"""
        self.rglob = rglob

    def get_rglob(self):
        """Ambil rglob"""
        return self.rglob

    def set_rloc(self, rloc):
        """Ganti rloc"""
        self.rloc = rloc

    def get_rloc(self):
        """Ambil rloc"""
        return self.rloc

    def set_rrand(self, rrand):
        """Ganti rrand"""
        self.rrand = rrand

    def get_rrand(self):
        """Ambil rrand"""
        return self.rrand

    def set_ruangan(self, ruangan):
        """Ganti Ruangan"""
        self.ruangan = ruangan

    def get_ruangan(self):
        """Ambil Ruangan"""
        return self.ruangan

    def set_size(self, size):
        """Ganti ukuran populasi"""
        self.size = size

    def get_size(self):
        """Ambil ukuran populasi"""
        return self.size

    def set_sks(self, sks):
        """Ganti sks masing" pelajaran"""
        self.sks = sks

    def get_sks(self):
        """Ambil sks masing" pelajaran"""
        return self.sks

    def impor_data(self):
        """Impor data sumber"""
        df_pelajaran = pd.read_excel('data.xlsx', 'Pelajaran')
        df_hari = pd.read_excel('data.xlsx', 'Hari')
        df_periode = pd.read_excel('data.xlsx', 'Periode')
        df_ruangan = pd.read_excel('data.xlsx', 'Ruangan')
        df_parameter = pd.read_excel('data.xlsx', 'Parameter')

        # Dataframe Pelajaran yang SKS eksklusifnya telah dibagi
        df_tanpa_ganda = df_pelajaran.loc[(df_pelajaran['SKS'] < 4)]
        df_ganda = df_pelajaran.loc[(df_pelajaran['SKS'] > 3)]
        df_ganda = df_ganda.append(df_ganda).reset_index(drop=True)
        df_ganda['No.'] = df_ganda.index + df_tanpa_ganda['No.'].count() + 1
        df_ganda['SKS'] = df_ganda['SKS'] // 2
        df_dgn_ganda = df_tanpa_ganda.append(df_ganda).reset_index(drop=True)

        def dosen_kelas(kolom):
            """Data Dosen dan Kelas"""
            dosen = []
            dos = []
            dfr = df_dgn_ganda.groupby([kolom, 'No.'])
            kol = 2 if kolom == "SKS" else 3 if kolom == "Dosen" else 4
            idx = df_dgn_ganda.sort_values(kolom).iloc[0, kol]
            for index in dfr.groups.keys():
                if index[0] == idx:
                    dos.append(index[1])
                    if index[1] == df_dgn_ganda.sort_values(kolom).iloc[-1, 0]:
                        dosen.append(dos)
                else:
                    dosen.append(dos)
                    dos = [index[1]]
                    idx = index[0]
            return dosen

        def split_list(a_list):
            """Membagi list jadi 2 persis (setengah)"""
            half = len(a_list)//2
            return [a_list[:half], a_list[half:]]

        ganda = split_list(df_ganda['No.'].tolist())
        ganda = np.transpose(ganda).tolist()

        self.set_bglob(df_parameter.iloc[0]['Bglob'])
        self.set_bloc(df_parameter.iloc[0]['Bloc'])
        self.set_brand(df_parameter.iloc[0]['Brand'])
        self.set_dosen(dosen_kelas("Dosen"))
        self.set_ganda(ganda)
        self.set_hari(df_hari['Nama'].tolist())
        self.set_kelas(dosen_kelas("Kelas"))
        self.set_limit(df_parameter.iloc[0]['Limit'])
        self.set_n_posisi(df_pelajaran['No.'].count() +
                          df_pelajaran.loc[(df_pelajaran['SKS'] > 3)]['SKS'].count() +
                          df_hari['No.'].count() * df_periode['No.'].count() *
                          df_ruangan['No.'].count() - df_pelajaran['SKS'].sum())
        self.set_pelajaran(df_dgn_ganda.values.tolist())
        self.set_periode(df_periode.values.tolist())
        self.set_ruangan(df_ruangan['Nama'].tolist())
        self.set_size(df_parameter.iloc[0]['Size'])
        self.set_sks(dosen_kelas("SKS"))

    def posisi_awal(self):
        """Inisialisasi posisi awal"""
        size = self.get_size()
        n_posisi = self.get_n_posisi()
        partikel = []
        i = 0
        while i < size:
            partikel.append(random.sample(range(1, n_posisi + 1), n_posisi))
            i += 1
        self.set_posisi(np.array(partikel))

    def hitung_fitness(self, posisi):
        """Menghitung fitness"""
        size = int(self.get_size())
        dosen = self.get_dosen()
        kelas = self.get_kelas()
        sks = self.get_sks()
        posisi = posisi.tolist()

        def perbaikan_partikel():
            """Memasukkan posisi tiap solusi ke seluruh hari
            dengan memanfaatkan SKS tiap posisi (pengajaran)
            """
            i = 0
            while i < size:
                iline = 0
                while iline < len(posisi[i]):
                    line = posisi[i][iline]
                    if line in sks[0]:
                        posisi[i].insert(iline, line)
                        iline += 1
                    elif line in sks[1]:
                        posisi[i].insert(iline, line)
                        posisi[i].insert(iline, line)
                        iline += 2
                    iline += 1
                i += 1

            return np.array(posisi)

        posisi_baik = perbaikan_partikel()

        def hari():
            """3 Dimensi (Partikel x Hari x Posisi/Partikel/Hari)
            days[0] = Partikel 1
            days[1] = Partikel 2
            days[2] = Partikel 3
            dst.
            days[i][0] = Senin
            days[i][1] = Selasa
            days[i][2] = Rabu
            dst."""
            periode = len(self.get_periode())  # Total periode dalam sehari
            ruang = []
            # ruang[:5]    = Ruang 101
            # ruang[5:10]  = Ruang 102
            # ruang[10:15] = Ruang 103
            # dst.
            for j in posisi_baik:
                ruang.append([j[i * periode:(i + 1) * periode] for i in range((len(j) + periode - 1
                                                                              ) // periode)])

            nhari = len(self.get_hari())  # Jumlah hari aktif dalam seminggu
            days = []  # 3 Dimensi (Partikel x Hari x Posisi/Partikel/Hari)
            # days[0] = Partikel 1
            # days[1] = Partikel 2
            # days[2] = Partikel 3
            # dst.
            # days[i][0] = Senin
            # days[i][1] = Selasa
            # days[i][2] = Rabu
            # dst.
            for j in range(nhari):
                hari = []
                for k in ruang:
                    day = [k[i * nhari + j] for i in range(len(k) // nhari)]
                    hari.append(list(chain.from_iterable(day)))
                days.append(hari)

            return np.transpose(days, (1, 0, 2))

        def c_dosen_n_kelas(data):
            """Constraint Dosen / Kelas bentrok. Walaupun sama Jam & Hari."""
            nilaip_indeksd = []  # [Dosen ke, Pelajaran ke]
            # Dari partikel (P), Nilai yang di bawah 71 ada di indeks ke berapa saja?
            indeksp_bawah71 = []
            for i in posisi_baik:
                row = []
                for k in i:
                    if k < 71:
                        # Masukkan i dan indeks dari j yang isinya kurang dari 71 ke row
                        # Masukkan posisi ke daftar
                        row.append([[i, j.index(k)] for i, j in enumerate(data) if k in j][0])
                nilaip_indeksd.append(row)
                # Masukkan i ke-x yang kurang dari 71 ke row71
                row71 = list(filter(lambda x: i[x] < 71, range(len(i))))
                indeksp_bawah71.append(row71)

            nilaid_selainp = []  # Nilai D selain nilai P
            for i in nilaip_indeksd:
                row = []
                for j in i:
                    temp = data[j[0]][:]  # Salin Dosen j[0] ke C
                    # Menghapus Dosen j[0] pelajaran j[1] tanpa menggangu variabel D asal
                    del temp[j[1]]
                    row.append(temp)  # Masukkan C ke row
                nilaid_selainp.append(row)

            batasan = []  # Batasan pertama atau kedua: bentrok dosen atau kelas
            for key, val in enumerate(nilaid_selainp):
                count = 0
                for i, j in enumerate(val):
                    for k in j:
                        if (posisi[key].index(k) - indeksp_bawah71[key][i]) % 60 == 0:
                            count += 1
                        if (posisi[key].index(k) + 1 - indeksp_bawah71[key][i]) % 60 == 0:
                            count += 1
                        if 54 <= k < 67:
                            if (posisi[key].index(k) + 2 - indeksp_bawah71[key][i]) % 60 == 0:
                                count += 1
                batasan.append(count)

            return batasan

        def c_ganda():
            """Bentrok pelajaran ganda pada hari yang sama"""
            days = hari()

            # Pelajaran yang mempunyai waktu dua pertemuan seminggu
            ganda = self.get_ganda()

            gandahari = []  # ganda[i][j] ada di hari apa saja?
            for valdays in days:
                temp1 = []
                for j in ganda:
                    temp2 = []
                    for valj in j:
                        temp2.append([i for i, el in enumerate(valdays) if valj in el])
                    temp1.append(list(chain.from_iterable(temp2)))
                gandahari.append(temp1)

            harisama = []  # Jumlah hari yang sama per pelajaran
            for i in gandahari:
                temp1 = []
                for j in i:
                    temp1.append(list(Counter(j).values()))
                harisama.append(list(chain.from_iterable(temp1)))  # Jumlah hari yang sama

            batasan3 = []  # Batasan 3 (Bentrok pelajaran pada hari yang sama)
            for i in harisama:
                count = 0    # Total hari yang sama
                for j in i:
                    if j > 1:
                        count += 1
                batasan3.append(count)

            return batasan3

        def c_terpotong():
            """Pelajaran yang waktunya terpotong (berada di 2 hari)"""
            days = hari()
            pelajaran = list(chain.from_iterable(kelas))
            pelajaranhari = [] # pelajaran[i][j] ada di hari apa saja?
            for valdays in days:
                k = []
                for i, j in enumerate(pelajaran):
                    k.append([i for i, el in enumerate(valdays) if j in el])
                pelajaranhari.append(k)

            batasan4 = []  # Batasan 4 (Pelajaran yang waktunya terpotong (berada di 2 hari))
            for i in pelajaranhari:
                count = 0
                for j in i:
                    if len(j) > 1:
                        count += 1
                batasan4.append(count)

            return batasan4

        def c_tak_tersedia():
            """Data pelajaran yang masuk di periode 'tak tersedia'"""
            # Jam ishoma selain Jumat
            ishoma = [[j for i, j in enumerate(k) if i % 12 == 6 and i % 60 != 54] for k in
                      posisi_baik]

            # Jumatan dan setelahnya
            jumat = [[j for i, j in enumerate(k) if 52 < i % 60 < 60] for k in posisi_baik]

            # Senin & selasa sore
            seninselasa = [[j for i, j in enumerate(k) if i > 246 if 6 < i % 60 < 12 or 18 < i % 60
                            < 24] for k in posisi_baik]

            # Semua data (termasuk dummy) yang masuk di periode "tak tersedia"
            semua = [list(chain.from_iterable([ishoma[i], jumat[i], seninselasa[i]])) for i in
                     range(len(posisi_baik))]

            # Data dummy dihapus, sehingga hanya data pelajaran
            pelajaran = [[i for i in j if i < 71] for j in semua]

            # Batasan 5
            batasan5 = [len(i) for i in pelajaran]

            return batasan5

        c_dosen = c_dosen_n_kelas(dosen)
        c_kelas = c_dosen_n_kelas(kelas)
        c_ganda = c_ganda()
        c_tak_tersedia = c_tak_tersedia()
        c_terpotong = c_terpotong()

        fitness = [1 / (1 + c_dosen[i] + c_kelas[i] + c_ganda[i] + c_tak_tersedia[i] +
                        c_terpotong[i]) for i in range(size)]

        self.set_fitness(fitness)

    def update_pbest(self, pbest, fitness_pbest, fitness_posisi):
        """
        Update Pbest
        """
        posisi = self.get_posisi()
        kur = [x1 - x2 for (x1, x2) in zip(fitness_pbest, fitness_posisi)]
        for indeks, isi in enumerate(kur):
            if isi < 0:
                pbest[indeks] = posisi[indeks]
        self.set_pbest(pbest)

    def cari_gbest(self, pbest, fitness):
        """
        Cari partikel terbaik global
        """
        idxgbest, value = max(enumerate(fitness), key=operator.itemgetter(1)) # pylint: disable=W0612
        gbest = pbest[idxgbest]
        self.set_gbest(gbest)
        self.set_fitness_gbest(value)

    def update_posisi(self, pos, pbest, gbest):
        """Update Posisi (posisi sekarang, pbest, gbest)"""
        rloc = self.get_rloc()
        bloc = self.get_bloc()
        rglob = self.get_rglob()
        bglob = self.get_bglob()
        rrand = self.get_rrand()
        brand = self.get_brand()
        n_posisi = self.get_n_posisi()

        def difference(pos1, pos2):
            """Algoritma DIFFERENCE (SUBSTRACTIONS) = position minum position"""
            temp = pos2[:].tolist()
            vel = []
            for key, j in enumerate(pos1):
                if j != temp[key]:
                    tukar1, tukar2 = key, temp.index(j)
                    vel.append((tukar1 + 1, tukar2 + 1))
                    temp[tukar1], temp[tukar2] = temp[tukar2], temp[tukar1]
            return vel

        def multiplication(vel, csatu, cdua=1):
            """Algoritma MULTIPLICATION = coefficient times velocity"""
            con = csatu * cdua
            if con == 0:
                vel = []
            elif 0 < con <= 1:
                pvel = math.ceil(con * len(vel))
                vel = vel[:pvel]
            elif con > 1:
                k = math.floor(con)
                cona = con - k
                pvel = math.ceil(len(vel) * cona)
                vel = vel * k + vel[:pvel]
            else:
                vel = vel[::-1]
                pvel = math.ceil(abs(con) * len(vel))
                vel = vel[:pvel]
            return vel

        def move(pos, vel):
            """Algoritma MOVE (ADDITION) = velocity plus velocity"""
            temp = copy.deepcopy(pos)
            for i in vel:
                tukar1, tukar2 = i[0] - 1, i[1] - 1
                temp[tukar1], temp[tukar2] = temp[tukar2], temp[tukar1]
            return temp

        posa = []
        for i, j in enumerate(pos):
            prand = random.sample(range(1, n_posisi + 1), n_posisi)

            ## DLOC
            difloc = difference(pbest[i], j)
            mulloc = multiplication(difloc, rloc, bloc)
            dloc = move(j, mulloc)

            ## DGLOB
            difglob = difference(gbest, j)
            muloglob = multiplication(difglob, rglob, bglob)
            dglob = move(j, muloglob)

            ## VRAND
            difrand = difference(prand, j)
            vrand = multiplication(difrand, rrand, brand)

            ## X
            difx = difference(dloc, dglob)
            mulx = multiplication(difx, csatu=0.5)
            movx = move(dglob, mulx)
            posx = move(movx, vrand)

            posa.append(posx)

        self.set_posisi(np.array(posa))

    def pengujian_parameter(self):
        """Pengujian Parameter HDPSO"""
        return 0

    def pengujian_iterasi(self, limit, fitness):
        """Pengujian Jumlah Iterasi"""

        # plt.title('Grafik Konvergensi')
        # plt.plot(np.arange(limit), fitness)
        # plt.xlabel('Jumlah Iterasi')
        # plt.ylabel('Fitness Terbaik')
        # plt.grid(True)
        # plt.axis([0, limit, fitness[0], fitness[-1]])
        # plt.show()

    def pengujian_partikel(self):
        """Pengujian Jumlah Partikel"""
        return 0

    def decoding(self, posisi):
        """Decoding GBEST_BAIK"""
        dosen = self.get_dosen()
        kelas = self.get_kelas()
        sks = self.get_sks()
        day = self.get_hari()
        nhari = len(day)
        ruangan = self.get_ruangan()
        posisi = posisi.tolist()
        nperiode = len(self.get_periode())

        iline = 0
        while iline < len(posisi):
            line = posisi[iline]
            if line in sks[0]:
                posisi.insert(iline, line)
                iline += 1
            elif line in sks[1]:
                posisi.insert(iline, line)
                posisi.insert(iline, line)
                iline += 2
            iline += 1

        ### HARI ###
        def hari(data_pos):
            """2 Dimensi (Hari x Posisi/Partikel/Hari)
            days[0] = Senin
            days[1] = Selasa
            days[2] = Rabu
            dst."""
            # ruang[:5]    = Ruang 101
            # ruang[5:10]  = Ruang 102
            # ruang[10:15] = Ruang 103
            # dst.
            ruang = [data_pos[i * nperiode:(i + 1) * nperiode] for i in
                     range((len(data_pos) + nperiode - 1) // nperiode)]
            days = []  # 2 Dimensi (Hari x Posisi/Partikel/Hari)
            # days[0] = Senin
            # days[1] = Selassa
            # days[2] = Rabu
            # dst.
            for j in range(nhari):
                day = [ruang[i * nhari + j] for i in range(len(ruang) // nhari)]
                days.append(list(chain.from_iterable(day)))

            return days

        days = hari(posisi)

        ### C_GANDA ###
        ganda = self.get_ganda()
        gandahari = []  # ganda[i][j] ada di hari apa saja?
        for j in ganda:
            temp2 = []
            for valj in j:
                temp2.append([i for i, el in enumerate(days) if valj in el])
            gandahari.append(list(chain.from_iterable(temp2)))

        harisama = []
        for j in gandahari:
            harisama.append(list(Counter(j).values()))  # Jumlah hari yang sama

        c_ganda = []  # Batasan 3 (Bentrok pelajaran pada hari yang sama)
        for i in harisama:
            count = 0    # Total hari yang sama
            for j in i:
                if j > 1:
                    c_ganda.append(ganda[count])

        ### C_TERPOTONG ###
        pelajaran = list(chain.from_iterable(kelas)) # Menggabungkan kelas mjd 1 list
        pelajaran.sort()
        pelajaranhari = [] # pelajaran[i][j] ada di hari apa saja?
        for i, j in enumerate(pelajaran):
            pelajaranhari.append([i for i, el in enumerate(days) if j in el])

        c_terpotong = []  # Batasan 4 (Pelajaran yang waktunya terpotong (berada di 2 hari))
        for key, i in enumerate(pelajaranhari):
            if len(i) > 1:
                c_terpotong.append(key + 1)
                # count += 1

        ### C_TAK_TERSEDIA ###
        ishoma = [j for i, j in enumerate(posisi) if i % 12 == 6 and i % 60 != 54]
        # Jumatan dan setelahnya
        jumat = [j for i, j in enumerate(posisi) if 52 < i % 60 < 60]
        # Senin sore
        senin = [j for i, j in enumerate(posisi) if i > 246 if 6 < i % 60 < 12 or 18 < i % 60 < 24]
        # Semua data (termasuk dummy) yang masuk di periode "tak tersedia"
        semua = list(chain.from_iterable([ishoma, jumat, senin]))
        # Data dummy dihapus, sehingga hanya data pelajaran
        c_tak_tersedia = list(set([i for i in semua if i < 71]))

        def c_dosen_n_kelas(data):
            """Constraint Dosen / Kelas bentrok. Walaupun sama Jam & Hari."""
            nilaip_indeksd = []  # [Dosen ke, Pelajaran ke]
            # Dari partikel (P), Nilai yang di bawah 36 ada di indeks ke berapa saja?
            indeksp_bawah71 = []

            for k in posisi:
                if k < 36:
                    # Masukkan i dan indeks dari j yang isinya kurang dari 71 ke row
                    # Masukkan posisi ke daftar
                    nilaip_indeksd.append([[i, j.index(k)] for i, j in enumerate(data) if k in j]
                                          [0])
            # Masukkan i ke-x yang kurang dari 71 ke row71
            indeksp_bawah71 = list(filter(lambda x: posisi[x] < 36, range(len(posisi))))

            nilaid_selainp = []  # Nilai D selain nilai P

            for j in nilaip_indeksd:
                temp = data[j[0]][:]  # Salin Dosen j[0] ke C
                # Menghapus Dosen j[0] pelajaran j[1] tanpa menggangu variabel D asal
                del temp[j[1]]
                nilaid_selainp.append(temp)  # Masukkan C ke row

            mod = nperiode * len(day)
            c_dosen_kelas = []  # Batasan pertama atau kedua: bentrok dosen atau kelas
            for i, j in enumerate(nilaid_selainp):
                temp = []
                for k in j:
                    if (posisi.index(k) - indeksp_bawah71[i]) % mod == 0:
                        temp.append(posisi[indeksp_bawah71[i]])
                        temp.append(k)
                    if (posisi.index(k) + 1 - indeksp_bawah71[i]) % mod == 0:
                        temp.append(posisi[indeksp_bawah71[i]])
                        temp.append(k)
                    if k in sks[1]:
                        if (posisi.index(k) + 2 - indeksp_bawah71[i]) % mod == 0:
                            temp.append(posisi[indeksp_bawah71[i]])
                            temp.append(k)
                if temp:
                    temp.sort()
                    c_dosen_kelas.append(temp)
            # Unique
            c_dosen_kelas = [list(y) for y in set([tuple(x) for x in c_dosen_kelas])]

            return c_dosen_kelas

        c_kelas = c_dosen_n_kelas(kelas)
        c_dosen = c_dosen_n_kelas(dosen)

        # Filter constraints
        constraints = []
        constraints.append(c_tak_tersedia) # c_tak_tersedia
        constraints.append(c_terpotong) # c_terpotong
        constraints.append(c_ganda) # c_ganda
        constraints.append(c_kelas) # c_kelas
        constraints.append(c_dosen) # c_dosen

        for key, val in enumerate(constraints):
            if key != len(constraints) - 2:
                for i in range(key+1, len(constraints)):
                    if len(np.array(constraints[i]).shape) == 1:
                        temp2 = [i for i in val for j in constraints[i] if i == j]
                        if temp2:
                            for j in temp2:
                                constraints[i].remove(j)
                    else:
                        for k in constraints[i]:
                            temp2 = [tmp for tmp in val for tmp2 in k if tmp == tmp2]
                            if temp2:
                                constraints[i].remove(k)

        all_constraints = list(chain.from_iterable(constraints))

        for i in all_constraints:
            if isinstance(i, list):
                for key, val in enumerate(i):
                    if key > 0:
                        all_constraints.append(val)
                all_constraints.remove(i)

        pos_tabel = posisi[:]
        for i in all_constraints:
            for key, val in enumerate(pos_tabel):
                if val == i:
                    pos_tabel[key] = 0

        pelajaran = list(range(1, len(pelajaran) + 1))

        halo = hari(pos_tabel)
        mtx_tabel = []
        for key, val in enumerate(halo):
            temp = []
            for j in range(len(ruangan)):
                temp2 = []
                temp2 = val[j * nperiode : (j + 1) * nperiode]
                if any(elem in temp2 for elem in pelajaran):
                    temp.append((ruangan[j], temp2))
            mtx_tabel.append((day[key], temp))

        for hari in mtx_tabel:
            for ruangan in hari[1]:
                pot = ruangan[1][:len(ruangan[1])-1]
                ong = ruangan[1][1:]
                for key, k in enumerate(pot):
                    if k != 0 and k == ong[key]:
                        ruangan[1].remove(k)

        pelajaran = self.get_pelajaran()
        for i in pelajaran:
            for key, val in enumerate(i):
                if key == len(i) - 1:
                    kelas = val.split("-")
                    i.append(kelas[0])
                    i.append(kelas[2])
                    i.remove(val)
                    break

        for hari in mtx_tabel:
            for all_no_pelajaran in hari[1]:
                panjang = len(all_no_pelajaran[1])
                for no_pelajaran in all_no_pelajaran[1]:
                    if not isinstance(no_pelajaran, list):
                        if no_pelajaran in range(1, len(pelajaran)+1):
                            for data_pelajaran in pelajaran:
                                if no_pelajaran == data_pelajaran[0]:
                                    del data_pelajaran[0]
                                    all_no_pelajaran[1].append(data_pelajaran)
                        else:
                            kosong = ['', 1, '', '', '']
                            all_no_pelajaran[1].append(kosong)
                    else:
                        break
                del all_no_pelajaran[1][:panjang]

        return mtx_tabel

if __name__ == "__main__":
    JADWAL = Penjadwalan()

    JADWAL.impor_data()
    JADWAL.posisi_awal() # Inisialisasi Posisi
    POSISI = JADWAL.get_posisi() # Posisi Awal

    JADWAL.hitung_fitness(POSISI)

    JADWAL.set_pbest(POSISI) # Inisialisasi Pbest (Pbest Awal = Posisi Awal)
    PBEST = JADWAL.get_pbest()

    JADWAL.hitung_fitness(PBEST)
    FITNESS_PBEST = JADWAL.get_fitness()

    JADWAL.cari_gbest(PBEST, FITNESS_PBEST)
    GBEST = JADWAL.get_gbest()

    JADWAL.set_rloc(random.random())
    JADWAL.set_rglob(random.random())
    JADWAL.set_rrand(random.random())

    LIMIT = JADWAL.get_limit()
    ITERASI = 0
    FITNESS_TERBAIK = []
    while ITERASI < LIMIT:
        # print(f'Iterasi ke-{ITERASI+1}')
        JADWAL.update_posisi(POSISI, PBEST, GBEST)
        POSISI = JADWAL.get_posisi()

        JADWAL.hitung_fitness(POSISI)
        FITNESS_POSISI = JADWAL.get_fitness()

        JADWAL.update_pbest(PBEST, FITNESS_PBEST, FITNESS_POSISI)
        PBEST = JADWAL.get_pbest()

        JADWAL.hitung_fitness(PBEST)
        FITNESS_PBEST = JADWAL.get_fitness()

        JADWAL.cari_gbest(PBEST, FITNESS_PBEST)
        GBEST = JADWAL.get_gbest()

        FITNESS_GBEST = JADWAL.get_fitness_gbest()

        # print(f'FITNESS GBEST : {FITNESS_GBEST}\n')
        FITNESS_TERBAIK.append(FITNESS_GBEST)
        POSISI = JADWAL.get_posisi()
        ITERASI += 1

    # print(f'Bloc : {JADWAL.get_bloc()}\n')
    # print(f'Bglob : {JADWAL.get_bglob()}\n')
    # print(f'Brand : {JADWAL.get_brand()}\n')
    print(f'FITNESS TERBAIK : \n{FITNESS_TERBAIK}\n')

    JADWAL.decoding(GBEST)
    # plt.title('Grafik Konvergensi')
    # plt.plot(np.arange(LIMIT), FITNESS_TERBAIK)
    # plt.xlabel('Jumlah Iterasi')
    # plt.ylabel('Fitness Terbaik')
    # plt.grid(True)
    # plt.axis([0, LIMIT, FITNESS_TERBAIK[0], FITNESS_TERBAIK[-1]])
    # plt.show()

    # JADWAL.pengujian_iterasi(LIMIT, FITNESS_TERBAIK)
print("--- %s seconds ---" % (time.time() - start_time))
      