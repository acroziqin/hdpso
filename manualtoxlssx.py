"""Program ini adalah program optimasi penjadwalan mata kuliah di STAIMA Al-Hikam Malang
menggunakan Hybrid Discrete PSO"""
# pylint: disable=cell-var-from-loop, too-many-locals

from itertools import chain
from collections import Counter
# import random
import math
import operator
import copy
import numpy as np

class Penjadwalan:
    """Kelas untuk penjadwalan menggunakan HDPSO"""
    def __init__(self):
        self.bglob = 0
        self.bloc = 0
        self.brand = 0
        self.dosen = [[1, 2],           # dosen[0] mengajar pelajaran 1 dan 2
                      [4, 5, 6, 7],     # dosen[1] mengajar pelajaran 4, 5, 6, dan 7
                      [8, 9, 10],       # dosen[2] mengajar pelajaran 8, 9, dan 10
                      [11, 12, 13, 14], # dst.
                      [15, 16, 17],
                      [21, 22, 24],
                      [25, 26, 27],
                      [28, 29, 30],
                      [3, 18],
                      [19, 20],
                      [23, 31],
                      [32, 33, 34, 35]]
        self.fitness = []
        self.fitness_gbest = 0
        self.ganda = [[32, 34], # pelajaran 2 kali pertemuan
                      [33, 35]]
        self.gbest = []
        self.kelas = [[1, 4, 8, 11, 15, 21, 25, 29], # kelas[0] memiliki pelajaran 1, 4, 8, ..., 29
                      [2, 5, 9, 12, 16, 22, 26, 30], # kelas[1] memiliki pelajaran 2, 5, 9, ..., 30
                      [7, 14, 24, 28],               # kelas[2] memiliki pelajaran 7, 14, 24, & 28
                      [6, 10, 13, 17, 27],           # dst.
                      [3, 19, 23, 32, 34],
                      [18, 20, 31, 33, 35]]
        self.limit = 3
        self.n_posisi = 577
        self.pbest = [[]]
        self.prand = [[]]
        self.posisi = [[]]
        self.rglob = 0
        self.rloc = 0
        self.rrand = 0
        self.size = 3
        self.sks = [[1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 21, 22, 24, 25, 26,
                     27, 28, 29, 30, 32, 33, 34, 35], # sks[0] = pelajaran yang memiliki 2 sks
                    [3, 18, 19, 20, 23, 31]]          # sks[1] = pelajaran yang memiliki 3 sks

    def set_bglob(self, bglob):
        """Ubah bglob"""
        self.bglob = bglob

    def get_bglob(self):
        """Ambil bglob"""
        return self.bglob

    def set_bloc(self, bloc):
        """Ubah bloc"""
        self.bloc = bloc

    def get_bloc(self):
        """Ambil bloc"""
        return self.bloc

    def set_brand(self, brand):
        """Ubah brand"""
        self.brand = brand

    def get_brand(self):
        """Ambil brand"""
        return self.brand

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

    def get_ganda(self):
        """Ambil pelajaran ganda"""
        return self.ganda

    def set_gbest(self, gbest):
        """Ubah Gbest"""
        self.gbest = gbest

    def get_gbest(self):
        """Ambil Gbest"""
        return self.gbest

    def get_kelas(self):
        """Ambil data kelas"""
        return self.kelas

    def get_limit(self):
        """Ambil Limit"""
        return self.limit

    def get_n_posisi(self):
        """Ambil banyak dimensi"""
        return self.n_posisi

    def set_pbest(self, pbest):
        """Ganti Pbest"""
        self.pbest = pbest

    def get_pbest(self):
        """Ambil Pbset"""
        return self.pbest

    def set_prand(self, prand):
        """Ubah Prand"""
        self.prand = prand

    def get_prand(self):
        """Ambil Prand"""
        return self.prand

    def set_posisi(self, posisi):
        """Ganti posisi"""
        self.posisi = posisi

    def get_posisi(self):
        """Ambil posisi"""
        return self.posisi

    def set_rglob(self, rglob):
        """Ubah rglob"""
        self.rglob = rglob

    def get_rglob(self):
        """Ambil rglob"""
        return self.rglob

    def set_rloc(self, rloc):
        """Ubah rloc"""
        self.rloc = rloc

    def get_rloc(self):
        """Ambil rloc"""
        return self.rloc

    def set_rrand(self, rrand):
        """Ubah rrand"""
        self.rrand = rrand

    def get_rrand(self):
        """Ambil rrand"""
        return self.rrand

    def get_size(self):
        """Ambil ukuran populasi"""
        return self.size

    def get_sks(self):
        """Ambil sks masing" pelajaran"""
        return self.sks

    def posisi_awal(self):
        """Inisialisasi posisi awal"""

        partikel = [[53, 149, 90, 27, 99, 167, 26, 66, 94, 125, 56, 6, 55, 10, 75, 13, 46, 133,
                     159, 8, 12, 131, 142, 3, 33, 35, 62, 98, 42, 82, 88, 20, 134, 154, 119, 151,
                     114, 30, 9, 17, 165, 45, 24, 22, 128, 19, 34, 106, 84, 31, 81, 16, 161, 95,
                     59, 109, 63, 108, 123, 71, 61, 115, 38, 57, 152, 78, 102, 129, 175, 150, 122,
                     93, 137, 127, 124, 160, 40, 120, 173, 96, 141, 37, 49, 148, 41, 69, 130, 113,
                     85, 18, 25, 168, 29, 158, 15, 169, 111, 166, 87, 39, 91, 5, 172, 135, 54, 117,
                     101, 51, 140, 72, 163, 139, 67, 174, 4, 47, 76, 116, 70, 147, 107, 171, 138,
                     143, 44, 156, 145, 60, 144, 121, 58, 164, 112, 32, 21, 68, 1, 73, 74, 7, 28,
                     146, 155, 83, 100, 104, 162, 80, 103, 23, 89, 110, 48, 92, 157, 14, 43, 64,
                     77, 136, 11, 65, 126, 52, 2, 153, 97, 86, 132, 50, 36, 105, 170, 118, 79],
                    [24, 107, 32, 128, 131, 72, 54, 96, 3, 4, 80, 15, 136, 95, 62, 38, 108, 91,
                     127, 74, 156, 26, 57, 25, 129, 22, 43, 89, 126, 41, 100, 103, 138, 18, 29,
                     125, 132, 119, 166, 130, 118, 133, 84, 19, 21, 111, 85, 68, 148, 64, 158, 123,
                     163, 67, 157, 93, 37, 171, 90, 77, 142, 17, 47, 1, 13, 94, 115, 170, 46, 42,
                     82, 109, 11, 154, 99, 50, 114, 61, 27, 48, 78, 28, 2, 152, 143, 105, 66, 45,
                     159, 140, 98, 12, 120, 75, 121, 34, 55, 56, 14, 144, 174, 104, 145, 149, 88,
                     69, 117, 102, 112, 71, 97, 73, 161, 36, 165, 40, 59, 51, 101, 167, 151, 139,
                     168, 6, 169, 65, 124, 113, 160, 141, 9, 150, 175, 30, 81, 39, 137, 86, 92,
                     146, 5, 44, 35, 53, 162, 58, 147, 20, 33, 10, 79, 49, 116, 23, 87, 16, 83, 63,
                     134, 172, 52, 164, 110, 153, 76, 60, 7, 8, 70, 155, 31, 122, 173, 106, 135],
                    [175, 24, 120, 85, 62, 101, 60, 145, 146, 83, 5, 4, 167, 122, 75, 111, 31, 15,
                     103, 171, 37, 7, 86, 142, 34, 17, 43, 88, 102, 151, 96, 133, 173, 20, 131,
                     156, 53, 38, 121, 65, 6, 161, 117, 163, 70, 174, 137, 66, 59, 110, 71, 81, 39,
                     124, 12, 157, 22, 141, 147, 84, 91, 92, 1, 46, 74, 23, 29, 82, 73, 21, 143, 3,
                     107, 41, 54, 79, 48, 130, 169, 30, 97, 100, 57, 13, 164, 165, 42, 168, 125,
                     80, 68, 152, 113, 56, 134, 45, 58, 139, 93, 153, 8, 72, 123, 128, 127, 2, 11,
                     63, 77, 99, 28, 166, 16, 104, 132, 140, 170, 150, 50, 112, 44, 148, 69, 108,
                     149, 26, 87, 19, 138, 9, 10, 126, 105, 51, 49, 98, 32, 159, 106, 47, 172, 67,
                     89, 90, 129, 155, 52, 35, 55, 95, 160, 40, 118, 119, 14, 158, 61, 36, 114, 27,
                     154, 144, 25, 18, 33, 109, 78, 136, 94, 64, 116, 162, 135, 115, 76]]

        self.set_posisi(np.array(partikel))

    def hitung_fitness(self, posisi):
        """Menghitung fitness"""
        size = self.get_size()
        dosen = self.get_dosen()
        kelas = self.get_kelas()
        sks = self.get_sks()
        posisi = posisi.tolist()

        def perbaikan_partikel(posisi):
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

        posisi_baik = perbaikan_partikel(posisi)

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
            periode = 12  # Total periode dalam sehari
            ruang = []
            # ruang[:5]    = Ruang 101
            # ruang[5:10]  = Ruang 102
            # ruang[10:15] = Ruang 103
            # dst.
            for j in posisi_baik:
                ruang.append([j[i * periode:(i + 1) * periode] for i in range((len(j) + periode - 1
                                                                              ) // periode)])
            nhari = 3  # Jumlah hari aktif dalam seminggu
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
            # dino = np.array(days)
            halo = np.transpose(days, (1, 0, 2))
            # dino = dino.tolist()
            return halo

        def c_dosen_n_kelas(data):
            """Constraint Dosen / Kelas bentrok. Walaupun sama Jam & Hari."""
            nilaip_indeksd = []  # [Dosen ke, Pelajaran ke]
            # Dari partikel (P), Nilai yang di bawah 36 ada di indeks ke berapa saja?
            indeksp_bawah71 = []
            for i in posisi_baik:
                row = []
                for k in i:
                    if k < 36:
                        # Masukkan i dan indeks dari j yang isinya kurang dari 71 ke row
                        # Masukkan posisi ke daftar
                        row.append([[i, j.index(k)] for i, j in enumerate(data) if k in j][0])
                nilaip_indeksd.append(row)
                # Masukkan i ke-x yang kurang dari 71 ke row71
                row71 = list(filter(lambda x: i[x] < 36, range(len(i))))
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
                # banyak = 0
                for i, j in enumerate(val):
                    temp = 0
                    for k in j:
                        if (posisi[key].index(k) - indeksp_bawah71[key][i]) % 36 == 0:
                            # count += 1
                            temp += 1
                        if (posisi[key].index(k) + 1 - indeksp_bawah71[key][i]) % 36 == 0:
                            # count += 1
                            temp += 1
                        if k in sks[1]:
                            if (posisi[key].index(k) + 2 - indeksp_bawah71[key][i]) % 36 == 0:
                                # count += 1
                                temp += 1
                    if temp > 0:
                        count += 1
                # if banyak != 0:
                #     count /= banyak
                batasan.append(count)

            return batasan

        def c_ganda():
            """Bentrok pelajaran ganda pada hari yang sama"""
            days = hari()
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
            pelajaran = list(chain.from_iterable(kelas)) # Menggabungkan kelas mjd 1 list
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
            ishoma = [[j for i, j in enumerate(k) if i % 12 == 6 and i % 36 != 30] for k in
                      posisi_baik]

            # Jumatan dan setelahnya
            jumat = [[j for i, j in enumerate(k) if 28 < i % 36 < 36] for k in posisi_baik]

            # Senin sore
            senin = [[j for i, j in enumerate(k) if i > 114 if 6 < i % 36 < 12] for k in
                     posisi_baik]

            # Semua data (termasuk dummy) yang masuk di periode "tak tersedia"
            semua = [list(chain.from_iterable([ishoma[i], jumat[i], senin[i]])) for i in
                     range(len(posisi_baik))]

            # Data dummy dihapus, sehingga hanya data pelajaran
            pelajaran = [[i for i in j if i < 36] for j in semua]

            # Batasan 5
            batasan5 = [len(i) for i in pelajaran]

            return batasan5

        c_dosen = c_dosen_n_kelas(dosen) # C1
        c_kelas = c_dosen_n_kelas(kelas) # C2
        c_ganda = c_ganda() # C3
        c_terpotong = c_terpotong() # C4
        c_tak_tersedia = c_tak_tersedia() # C5

        fitness = [1 / (1 + c_dosen[i] + c_kelas[i] + c_ganda[i] + c_terpotong[i] +
                        c_tak_tersedia[i]) for i in range(size)]

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

    def update_posisi(self, pos, pbest, gbest, prand, ite):
        """Update Posisi (posisi sekarang, pbest, gbest)"""
        # rloc = self.get_rloc()
        rloc = [[0.259539410787605, 0.149068404576628, 0.165502473466925],
                [0.170517387442299, 0.780230930802896, 0.125010446443322]]
        bloc = [[0.872051213551414, 0.569974016183252, 0.802227905381299],
                [0.77819953623234, 0.355328990831211, 0.885743407321508]]
        rglob = [[0.847295675136998, 0.73543816348965, 0.007271099341014],
                 [0.544117127511935, 0.348450013866271, 0.307717212709986]]
        bglob = [[0.429433753214027, 0.872547463705991, 0.704466434134711],
                 [0.0262275752861789, 0.483402094683198, 0.430041848364539]]
        rrand = [[0.821871734779764, 0.362918677799237, 0.125115336968571],
                 [0.380722402559881, 0.325090748534211, 0.445040565688009]]
        brand = [[0.756961596158189, 0.722324158274813, 0.18062181600741],
                 [0.783176435919866, 0.121600406913761, 0.220043632953905]]

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

        posa = [] # posisi aksen (x')
        for i, j in enumerate(pos):
            ## DLOC
            # pbest = xdua[:]
            difloc = difference(pbest[i], j)
            mulloc = multiplication(difloc, rloc[ite][i], bloc[ite][i])
            dloc = move(j, mulloc)

            ## DGLOB
            # gbest = E[:]
            difglob = difference(gbest, j)
            mulglob = multiplication(difglob, rglob[ite][i], bglob[ite][i])
            dglob = move(j, mulglob)

            ## VRAND
            # prand = G[:]
            difrand = difference(prand, j)
            vrand = multiplication(difrand, rrand[ite][i], brand[ite][i])

            ## X
            difx = difference(dloc, dglob)
            mulx = multiplication(difx, csatu=0.5)
            movx = move(dglob, mulx)
            posx = move(movx, vrand)
            posa.append(posx)
            # posa.append(vrand)

        self.set_posisi(np.array(posa))

    def decoding(self, posisi):
        """Decoding GBEST_BAIK"""
        dosen = self.get_dosen()
        kelas = self.get_kelas()
        sks = self.get_sks()
        posisi = posisi.tolist()
        nperiode = 12
        nhari = 3
        nruangan = 6
        npelajaran = 35

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
            ruang = [data_pos[i * nperiode:(i + 1) * nperiode] for i in range((len(data_pos) + nperiode
                                                                             - 1) // nperiode)]
            nhari = 3  # Jumlah hari aktif dalam seminggu
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
        ishoma = [j for i, j in enumerate(posisi) if i % 12 == 6 and i % 36 != 30]
        # Jumatan dan setelahnya
        jumat = [j for i, j in enumerate(posisi) if 28 < i % 36 < 36]
        # Senin sore
        senin = [j for i, j in enumerate(posisi) if i > 114 if 6 < i % 36 < 12]
        # Semua data (termasuk dummy) yang masuk di periode "tak tersedia"
        semua = list(chain.from_iterable([ishoma, jumat, senin]))
        # Data dummy dihapus, sehingga hanya data pelajaran
        c_tak_tersedia = list(set([i for i in semua if i < 36]))

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

            mod = nperiode * nhari
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
                    temp = np.array(constraints[i])
                    if len(temp.shape) == 1:
                        temp2 = set(val) & set(constraints[i])
                        if temp2:
                            for j in temp2:
                                constraints[i].remove(j)
                    else:
                        for k in constraints[i]:
                            temp2 = set(val) & set(k)
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

        pelajaran = list(range(1, npelajaran + 1))

        halo = hari(pos_tabel)
        mtx_tabel = []
        for key, val in enumerate(halo):
            temp = []
            for j in range(nruangan):
                temp2 = {}
                temp2[j] = val[j * nperiode : (j + 1) * nperiode]
                if any(elem in temp2[j]  for elem in pelajaran):
                    temp.append(temp2)
            mtx_tabel.append(temp)

        for i in mtx_tabel:
            for j in i:
                for val in j.values():
                    pot = val[:len(val)-1]
                    ong = val[1:]
                    for key, k in enumerate(pot):
                        if k != 0 and k == ong[key]:
                            val.remove(k)

        return mtx_tabel


if __name__ == "__main__":
    JADWAL = Penjadwalan()

    JADWAL.posisi_awal() # Inisialisasi Posisi
    POSISI = JADWAL.get_posisi() # Posisi Awal

    JADWAL.hitung_fitness(POSISI)
    FITNESS_POSISI = JADWAL.get_fitness()

    JADWAL.set_pbest(POSISI) # Inisialisasi Pbest (Pbest Awal = Posisi Awal)
    PBEST = JADWAL.get_pbest()

    JADWAL.hitung_fitness(PBEST)
    FITNESS_PBEST = JADWAL.get_fitness()

    JADWAL.cari_gbest(PBEST, FITNESS_PBEST)
    GBEST = JADWAL.get_gbest()

    # print(f'Inisialisasi\n')
    # print(f'Posisi  :\n{POSISI}\n')
    # print(f'Pbest  :\n{PBEST}\n')

    PRAND = [[80, 175, 78, 111, 97, 43, 145, 158, 81, 84, 52, 29, 114, 155, 20, 53, 64, 76, 126,
              98, 156, 142, 60, 26, 174, 65, 157, 147, 51, 44, 37, 110, 46, 9, 140, 162, 71, 150,
              42, 149, 139, 164, 96, 3, 131, 100, 133, 130, 159, 66, 113, 19, 119, 117, 93, 105,
              109, 17, 40, 69, 168, 31, 95, 30, 11, 33, 138, 166, 91, 148, 22, 89, 55, 143, 172, 49,
              12, 127, 135, 152, 36, 8, 47, 21, 48, 106, 75, 112, 54, 90, 18, 25, 171, 34, 5, 123,
              94, 116, 136, 27, 125, 35, 41, 67, 14, 134, 38, 170, 173, 73, 101, 72, 161, 28, 128,
              50, 70, 7, 1, 103, 59, 15, 132, 58, 77, 74, 79, 104, 92, 144, 57, 32, 102, 86, 39, 82,
              141, 121, 151, 154, 118, 83, 45, 61, 2, 88, 68, 167, 169, 56, 160, 153, 163, 13, 24,
              4, 99, 62, 85, 16, 23, 129, 107, 87, 108, 115, 137, 10, 146, 6, 63, 122, 165, 124,
              120],
             [122, 45, 158, 118, 111, 162, 36, 83, 12, 41, 142, 74, 31, 112, 110, 23, 161, 119, 121,
              134, 106, 108, 136, 8, 2, 21, 126, 57, 143, 86, 167, 150, 9, 120, 14, 91, 43, 114,
              131, 135, 16, 102, 125, 15, 130, 61, 163, 37, 35, 171, 149, 89, 172, 38, 10, 80, 51,
              153, 170, 39, 24, 32, 169, 63, 62, 72, 100, 64, 160, 124, 27, 168, 46, 17, 58, 159,
              103, 104, 28, 79, 148, 5, 67, 146, 65, 173, 18, 132, 69, 151, 33, 59, 99, 87, 174,
              138, 52, 19, 42, 1, 109, 140, 26, 49, 48, 44, 30, 154, 13, 66, 107, 73, 157, 155, 71,
              127, 85, 145, 90, 113, 11, 144, 139, 34, 129, 78, 76, 6, 68, 156, 123, 133, 54, 152,
              82, 22, 53, 105, 55, 77, 128, 20, 7, 84, 147, 93, 60, 165, 115, 98, 88, 4, 117, 94,
              116, 29, 97, 47, 175, 81, 40, 92, 137, 70, 95, 96, 101, 56, 50, 25, 3, 166, 75, 141,
              164]]

    # LIMIT = JADWAL.get_limit()
    LIMIT = 1
    ITERASI = 0
    FITNESS_TERBAIK = []
    while ITERASI <= LIMIT:
        # print(f'Iterasi ke-{ITERASI+1}\n')
        # if ITERASI == 0:
        #     print(f'Inisialisasi\n')


        JADWAL.update_posisi(POSISI, PBEST, GBEST, PRAND[ITERASI], ITERASI)
        POSISI = JADWAL.get_posisi()
        # print(POSISI)
        # print(f'Posisi :\n{POSISI}\n')

        JADWAL.hitung_fitness(POSISI)
        FITNESS_POSISI = JADWAL.get_fitness()

        JADWAL.update_pbest(PBEST, FITNESS_PBEST, FITNESS_POSISI)
        PBEST = JADWAL.get_pbest()
        # print(f'Pbest :\n{PBEST}\n')

        JADWAL.hitung_fitness(PBEST)
        FITNESS_PBEST = JADWAL.get_fitness()

        JADWAL.cari_gbest(PBEST, FITNESS_PBEST)
        GBEST = JADWAL.get_gbest()

        # FITNESS = JADWAL.get_fitness()
        # JADWAL.cari_gbest(PBEST, FITNESS_PBEST)
        # GBEST = JADWAL.get_gbest()
        # print(GBEST)
        POSISI = JADWAL.get_posisi() # Posisi Awal

        # print(f'Posisi  :\n{POSISI}\n')
        # print(f'FITNESS :\n{FITNESS}\n')
        # print(f'PBEST :\n{PBEST}\n')

        # if ITERASI != LIMIT:
            # print(f'Iterasi ke-{ITERASI+1}\n')

        # JADWAL.update_posisi(POSISI, PBEST, GBEST, PRAND[ITERASI])
        # POSISI = JADWAL.get_posisi()
        # JADWAL.set_pbest(POSISI)
        # print(JADWAL.get_posisi())
        # print([item for item, count in C4jj7Ma:VFtk_vVCounter(PRAND).items() if count > 1])
        FITNESS_GBEST = JADWAL.get_fitness_gbest()
        FITNESS_TERBAIK.append(FITNESS_GBEST)
        ITERASI += 1
    # print(f'GBEST :\n{GBEST}')
    # GBEST_BAIK = JADWAL.perbaikan_partikel(GBEST.tolist())
    # JADWAL.hitung_fitness(GBEST_BAIK)
    # print(len(GBEST.shape))
    # print(len(POSISI.shape))
    # print(f'GBEST_BAIK :\n{GBEST_BAIK}\n')
    # print(f'FITNESS_TERBAIK :\n{FITNESS_TERBAIK[-1]}')
    print(JADWAL.decoding(GBEST))


    # print(PBEST)
