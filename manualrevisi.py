"""Program ini adalah program optimasi penjadwalan mata kuliah di STAIMA Al-Hikam Malang
menggunakan Hybrid Discrete PSO"""
# pylint: disable=cell-var-from-loop, too-many-locals, too-many-instance-attributes, too-many-public-methods

from itertools import chain
from collections import Counter
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
        self.hari = ['Senin', 'Rabu', 'Jumat']
        self.kelas = [[1, 4, 8, 11, 15, 21, 25, 29], # kelas[0] memiliki pelajaran 1, 4, 8, ..., 29
                      [2, 5, 9, 12, 16, 22, 26, 30], # kelas[1] memiliki pelajaran 2, 5, 9, ..., 30
                      [7, 14, 24, 28],               # kelas[2] memiliki pelajaran 7, 14, 24, & 28
                      [6, 10, 13, 17, 27],           # dst.
                      [3, 19, 23, 32, 34],
                      [18, 20, 31, 33, 35]]
        self.limit = 3
        self.n_posisi = 577
        self.pbest = [[]]
        self.pelajaran = [
            [1, 'Pancasila', 2, 'Ali Rifan', 'PAI-1-A'],
            [2, 'Pancasila', 2, 'Ali Rifan', 'PAI-1-B'],
            [3, 'Ilmu Pendidikan', 3, 'A. Qomarudin', 'PAI-3-A'],
            [4, 'Bahasa Indonesia', 2, 'Handoko', 'PAI-1-A'],
            [5, 'Bahasa Indonesia', 2, 'Handoko', 'PAI-1-B'],
            [6, 'Bahasa Indonesia', 2, 'Handoko', 'MPI-1-A'],
            [7, 'Bahasa Indonesia', 2, 'Handoko', 'PGMI-1-A'],
            [8, 'Ushul Fiqih', 2, 'Kasuwi Saiban', 'PAI-1-A'],
            [9, 'Ushul Fiqih', 2, 'Kasuwi Saiban', 'PAI-1-B'],
            [10, 'Ushul Fiqih', 2, 'Kasuwi Saiban', 'MPI-1-A'],
            [11, 'Studi Al-Quran', 2, 'Mokhamat Nafi', 'PAI-1-A'],
            [12, 'Studi Al-Quran', 2, 'Mokhamat Nafi', 'PAI-1-B'],
            [13, 'Studi Al-Quran', 2, 'Mokhamat Nafi', 'MPI-1-A'],
            [14, 'Studi Al-Quran', 2, 'Mokhamat Nafi', 'PGMI-1-A'],
            [15, 'Bahasa Inggris', 2, 'Hilman Wajdi', 'PAI-1-A'],
            [16, 'Bahasa Inggris', 2, 'Hilman Wajdi', 'PAI-1-B'],
            [17, 'Bahasa Inggris', 2, 'Hilman Wajdi', 'MPI-1-A'],
            [18, 'Ilmu Pendidikan', 3, 'A. Qomarudin', 'PAI-3-B'],
            [19, 'Qowaidul Fiqih', 3, 'Zaenu Zuhdi', 'PAI-3-A'],
            [20, 'Qowaidul Fiqih', 3, 'Zaenu Zuhdi', 'PAI-3-B'],
            [21, 'Bahasa Arab', 2, 'Moh. Nadhif', 'PAI-1-A'],
            [22, 'Bahasa Arab', 2, 'Moh. Nadhif', 'PAI-1-B'],
            [23, 'Media Pembelajaran PAI', 3, 'Muh. Rodhi Zamzami', 'PAI-3-A'],
            [24, 'Bahasa Arab', 2, 'Moh. Nadhif', 'PGMI-1-A'],
            [25, 'Pengantar Studi Islam', 2, 'Umi Salamah', 'PAI-1-A'],
            [26, 'Pengantar Studi Islam', 2, 'Umi Salamah', 'PAI-1-B'],
            [27, 'Pengantar Studi Islam', 2, 'Umi Salamah', 'MPI-1-A'],
            [28, 'Pengantar Studi Islam', 2, 'Misbahul Munir', 'PGMI-1-A'],
            [29, 'IAD & IBD', 2, 'Misbahul Munir', 'PAI-1-A'],
            [30, 'IAD & IBD', 2, 'Misbahul Munir', 'PAI-1-B'],
            [31, 'Media Pembelajaran PAI', 3, 'Muh. Rodhi Zamzami', 'PAI-3-B'],
            [32, 'Takhrijul Hadits', 2, 'Damanhuri', 'PAI-3-A'],
            [33, 'Takhrijul Hadits', 2, 'Damanhuri', 'PAI-3-B'],
            [34, 'Takhrijul Hadits', 2, 'Damanhuri', 'PAI-3-A'],
            [35, 'Takhrijul Hadits', 2, 'Damanhuri', 'PAI-3-B']]
        self.prand = [[]]
        self.posisi = [[]]
        self.rglob = 0
        self.rloc = 0
        self.rrand = 0
        self.ruangan = ['101', '102', '103', '304', '305', '306']
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

    def get_hari(self):
        """Ambil Hari"""
        return self.hari

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

    def get_pelajaran(self):
        """Ambil Pelajaran"""
        return self.pelajaran

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

    def get_ruangan(self):
        """Ambil Ruangan"""
        return self.ruangan

    def get_size(self):
        """Ambil ukuran populasi"""
        return self.size

    def get_sks(self):
        """Ambil sks masing" pelajaran"""
        return self.sks

    def posisi_awal(self):
        """Inisialisasi posisi awal"""

        partikel = [[8, 52, 56, 17, 85, 15, 63, 62, 2, 45, 46, 53, 71, 14, 79, 90, 69, 32, 11, 91,
                     55, 7, 3, 96, 59, 44, 6, 23, 37, 43, 9, 106, 49, 98, 24, 61, 81, 1, 10, 36,
                     77, 89, 13, 34, 104, 86, 39, 78, 50, 4, 41, 93, 105, 88, 72, 100, 42, 66, 26,
                     94, 28, 84, 48, 64, 80, 51, 76, 35, 40, 73, 87, 30, 103, 29, 25, 99, 97, 54,
                     70, 22, 95, 83, 101, 47, 92, 20, 5, 58, 21, 31, 75, 19, 18, 74, 67, 60, 57,
                     12, 27, 33, 16, 68, 38, 102, 82, 65],
                    [92, 37, 101, 2, 89, 90, 82, 43, 85, 29, 84, 20, 56, 10, 98, 66, 70, 75, 25,
                     104, 12, 40, 65, 86, 76, 13, 51, 68, 30, 60, 33, 71, 103, 28, 3, 58, 79, 32,
                     24, 77, 48, 34, 27, 45, 7, 96, 106, 6, 47, 4, 42, 35, 81, 21, 11, 83, 8, 46,
                     38, 31, 72, 17, 78, 59, 80, 94, 57, 14, 105, 9, 87, 91, 23, 67, 26, 102, 74,
                     44, 49, 1, 97, 22, 50, 54, 41, 93, 99, 53, 55, 63, 18, 61, 88, 15, 62, 39, 5,
                     16, 69, 95, 19, 64, 100, 73, 52, 36],
                    [21, 86, 47, 15, 99, 97, 36, 92, 103, 35, 87, 61, 59, 7, 89, 95, 80, 81, 24,
                     58, 105, 73, 2, 22, 94, 66, 63, 91, 104, 38, 53, 60, 42, 32, 27, 96, 88, 62,
                     51, 26, 9, 18, 30, 68, 48, 71, 84, 93, 76, 13, 74, 5, 44, 28, 56, 67, 40, 69,
                     41, 52, 19, 31, 100, 43, 10, 83, 6, 70, 29, 25, 14, 77, 16, 106, 78, 90, 17,
                     12, 55, 39, 75, 54, 49, 65, 1, 45, 23, 57, 82, 3, 20, 11, 46, 37, 34, 64, 4,
                     50, 98, 33, 8, 79, 85, 72, 102, 101]]

        self.set_posisi(np.array(partikel))

    def hitung_fitness(self, posisi):
        """Menghitung fitness"""
        size = self.get_size()
        dosen = self.get_dosen()
        kelas = self.get_kelas()
        sks = self.get_sks()
        posisi = posisi.tolist()
        nperiode = 12

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
            i = 0
            while i < size:
                iline = 0
                while iline < len(posisi[i]):
                    line = posisi[i][iline]
                    # Jam ishoma selain Jumat
                    if iline % nperiode == 6:
                        if iline % (nperiode * size) != ((nperiode * size) - 6):
                            posisi[i].insert(iline, 0)
                    # Jumatan dan setelahnya
                    if ((nperiode * size) - 8) < iline % (nperiode * size) < (nperiode * size):
                        posisi[i].insert(iline, 0)
                    # Senin sore
                    if iline > 114:
                        if 6 < iline % (nperiode * size) < nperiode:
                            posisi[i].insert(iline, 0)
                    iline += 1
                posisi[i] += [0]*7
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
            days[i][1] = Rabu
            days[i][2] = Jumat
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
            indeksp_bawah71 = [] # ∑(SKS * perulangan) = 76 jam pelajaran
            for i in posisi_baik:
                row = []
                for k in i:
                    if 0 < k < 36:
                        # Masukkan i dan indeks dari j yang isinya kurang dari 71 ke row
                        # Masukkan posisi ke daftar
                        row.append([[i, j.index(k)] for i, j in enumerate(data) if k in j][0])
                nilaip_indeksd.append(row)
                # Masukkan i ke-x yang kurang dari 71 ke row71
                row71 = list(filter(lambda x: 0 < i[x] < 36, range(len(i))))
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

            potong = []  # Batasan 4 (Pelajaran yang waktunya terpotong (berada di 2 hari))
            for i in pelajaranhari:
                count = 0
                for j in i:
                    if len(j) > 1:
                        count += 1
                potong.append(count)

            # Periode 6 & 8 kecuali Jumat
            periode6_dgnnol = [[j for i, j in enumerate(k) if i % nperiode == 5] for k in posisi_baik]
            periode6_tnpnol = []
            for i in periode6_dgnnol:
                i = [j for j in i if j != 0]
                periode6_tnpnol.append(i)
            periode8_dgnnol = [[j for i, j in enumerate(k) if i % nperiode == 7] for k in posisi_baik]
            periode8_tnpnol = []
            for i in periode8_dgnnol:
                i = [j for j in i if j != 0]
                periode8_tnpnol.append(i)
            periode6dan8 = []
            countlist = []
            for i, j in enumerate(periode8_tnpnol):
                periode6dan8.append(periode6_tnpnol[i] + j)
                temp = dict(Counter(periode6dan8[i]))
                count = 0
                for k in temp.values():
                    if k > 1:
                        count += 1
                countlist.append(count)
            batasan4 = []
            for i, j in enumerate(potong):
                batasan4.append(j + countlist[i])
            return batasan4

        c_dosen = c_dosen_n_kelas(dosen) # C1
        c_kelas = c_dosen_n_kelas(kelas) # C2
        c_ganda = c_ganda() # C3
        c_terpotong = c_terpotong() # C4

        fitness = [1 / (1 + c_dosen[i] + c_kelas[i] + c_ganda[i] + c_terpotong[i]) for i in range(size)]

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
        day = self.get_hari()
        ruangan = self.get_ruangan()
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
            ruang = [data_pos[i * nperiode:(i + 1) * nperiode] for i in
                     range((len(data_pos) + nperiode - 1) // nperiode)]
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
                    if len(np.array(constraints[i]).shape) == 1:
                        temp2 = [tmp for tmp in val for tmp2 in constraints[i] if tmp == tmp2]
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

        pelajaran = list(range(1, npelajaran + 1))
        halo = hari(pos_tabel)
        mtx_tabel = []
        for key, val in enumerate(halo):
            temp = []
            for j in range(nruangan):
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

    PRAND = [[19, 35, 56, 6, 32, 87, 25, 67, 102, 40, 5, 101, 83, 66, 26, 51, 52, 57, 24, 78, 27,
              58, 34, 90, 77, 10, 14, 22, 36, 93, 55, 105, 4, 71, 45, 92, 42, 47, 99, 28, 13, 38,
              80, 68, 30, 11, 85, 79, 37, 94, 98, 48, 2, 95, 60, 82, 104, 75, 15, 103, 7, 61, 54,
              50, 1, 29, 81, 9, 23, 49, 16, 8, 62, 100, 12, 53, 33, 39, 72, 106, 97, 65, 43, 84, 3,
              89, 91, 44, 96, 70, 20, 76, 41, 21, 64, 86, 46, 31, 17, 63, 88, 18, 59],
             [26, 40, 43, 49, 21, 6, 57, 52, 70, 17, 22, 106, 2, 4, 104, 30, 90, 99, 36, 19, 53,
              65, 101, 32, 33, 64, 54, 73, 66, 77, 35, 96, 69, 39, 61, 86, 97, 23, 55, 15, 41, 67,
              10, 48, 1, 102, 84, 58, 92, 60, 68, 12, 80, 31, 98, 20, 93, 95, 79, 91, 103, 51, 11,
              82, 8, 94, 87, 89, 88, 59, 47, 74, 34, 62, 78, 75, 63, 16, 27, 85, 44, 18, 37, 29,
              76, 13, 50, 81, 56, 71, 9, 100, 3, 83, 105, 24, 45, 72, 28, 46, 25, 7, 5, 14, 38,
              42]]

    # LIMIT = JADWAL.get_limit()
    LIMIT = 1
    ITERASI = 0
    FITNESS_TERBAIK = []
    while ITERASI <= LIMIT:
        print(f'Iterasi ke-{ITERASI+1}\n')
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
    # print(len(POSISI.shape))C
    # print(f'GBEST_BAIK :\n{GBEST_BAIK}\n')
    # print(f'FITNESS_TERBAIK :\n{FITNESS_TERBAIK[-1]}')
    # print(JADWAL.decoding(GBEST))


    # print(PBEST)
