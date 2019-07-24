"""Program ini adalah program optimasi penjadwalan mata kuliah di STAIMA Al-Hikam Malang
menggunakan Hybrid Discrete PSO"""
# pylint: disable=cell-var-from-loop

import random
from itertools import chain
from collections import Counter
import numpy as np

class Penjadwalan:
    """Kelas untuk penjadwalan menggunakan HDPSO"""
    def __init__(self, bloc=1, bglob=0.5, brand=0.00001, size=5, n_posisi=577, limit=1):
        self.posisi = [[]]
        self.bglob = bglob
        self.bloc = bloc
        self.brand = brand
        self.rglob = []
        self.rloc = []
        self.rrand = []
        self.size = size
        self.n_posisi = n_posisi
        self.pbest = [[]]
        self.limit = limit

    def get_limit(self):
        """Ambil Limit"""
        return self.limit

    def set_posisi(self, posisi):
        """Ganti posisi"""
        self.posisi = posisi

    def get_posisi(self):
        """Ambil posisi"""
        return self.posisi

    def set_pbest(self, pbest):
        """Ganti Pbest"""
        self.pbest = pbest

    def get_pbest(self):
        """Ambil Pbset"""
        return self.pbest

    def get_size(self):
        """Ambil ukuran populasi"""
        return self.size

    def get_n_posisi(self):
        """Ambil banyak dimensi"""
        return self.n_posisi

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

    def perbaikan_partikel(self):
        """Memasukkan posisi tiap solusi ke seluruh hari
        dengan memanfaatkan SKS tiap posisi (pengajaran)
        """
        posisi = self.get_posisi().tolist()
        size = self.get_size()
        i = 0
        while i < size:
            iline = 0
            while iline < len(posisi[i]):
                line = posisi[i][iline]
                if line < 54:
                    posisi[i].insert(iline, line)
                    iline += 1
                elif line < 67:
                    posisi[i].insert(iline, line)
                    posisi[i].insert(iline, line)
                    iline += 2
                elif line < 71:
                    posisi[i].insert(iline, line)
                    iline += 1
                iline += 1
            i += 1
        return np.array(posisi)

    def days(self):
        """3 Dimensi (Partikel x Hari x Posisi/Partikel/Hari)
        days[0] = Partikel 1
        days[1] = Partikel 2
        days[2] = Partikel 3
        dst.
        days[i][0] = Senin
        days[i][1] = Selasa
        days[i][2] = Rabu
        dst."""
        posisi = self.perbaikan_partikel().tolist()
        periode = 12  # Total periode dalam sehari
        ruang = []
        # ruang[:5]    = Ruang 101
        # ruang[5:10]  = Ruang 102
        # ruang[10:15] = Ruang 103
        # dst.
        for j in posisi:
            ruang.append([j[i * periode:(i + 1) * periode] for i in range((len(j) + periode - 1) //
                                                                          periode)])

        nhari = 5  # Jumlah hari aktif dalam seminggu
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

    def c_dosen_n_kelas(self, data):
        """Constraint Dosen / Kelas bentrok. Walaupun sama Jam & Hari."""
        posisi = self.perbaikan_partikel().tolist()
        nilaip_indeksd = []  # [Dosen ke, Pelajaran ke]
        # Dari partikel (P), Nilai yang di bawah 71 ada di indeks ke berapa saja?
        indeksp_bawah71 = []
        for i in posisi:
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

        batasan = []  # Batasan pertama: bentrok dosen
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

    def c_ganda(self):
        """Bentrok pelajaran ganda pada hari yang sama"""
        days = self.days()

        # Pelajaran yang mempunyai waktu dua pertemuan seminggu
        ganda = [[67, 68],
                 [69, 70]]

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

    def c_terpotong(self, data):
        """Pelajaran yang waktunya terpotong (berada di 2 hari)"""
        days = self.days()
        pelajaran = list(chain.from_iterable(data))
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

    def c_tak_tersedia(self):
        """Data pelajaran yang masuk di periode 'tak tersedia'"""
        posisi = self.perbaikan_partikel().tolist()
        # Jam ishoma selain Jumat
        ishoma = [[j for i, j in enumerate(k) if i % 12 == 6 and i % 60 != 54] for k in posisi]

        # Jumatan dan setelahnya
        jumat = [[j for i, j in enumerate(k) if 52 < i % 60 < 60] for k in posisi]

        # Senin & selasa sore
        seninselasa = [[j for i, j in enumerate(k) if i > 246 if 6 < i % 60 < 12 or 18 < i % 60 <
                        24] for k in posisi]

        # Semua data (termasuk dummy) yang masuk di periode "tak tersedia"
        semua = [list(chain.from_iterable([ishoma[i], jumat[i], seninselasa[i]])) for i in
                 range(len(posisi))]

        # Data dummy dihapus, sehingga hanya data pelajaran
        pelajaran = [[i for i in j if i < 71] for j in semua]

        # Batasan 5
        batasan5 = [len(i) for i in pelajaran]

        return batasan5

    def fitness(self):
        """Menghitung fitness"""
        size = self.get_size()
        dosen = [[54, 55],   # Dosen D[0] mengajar pelajaran 54 dan 55
                 [3, 51],    # Dosen D[1] mengajar pelajaran 3 dan 51
                 [1, 2, 53], # Dosen D[2] mengajar pelajaran 1, 2, dan 53
                 [66],       # dst.
                 [67, 68, 69, 70],
                 [52],
                 [4, 5, 6, 7],
                 [15, 16, 17, 18],
                 [8, 9, 10, 64],
                 [36, 37, 41, 45],
                 [28, 29, 30, 46],
                 [23, 33, 50, 62],
                 [63],
                 [21, 22, 24],
                 [47],
                 [11, 12, 13, 14],
                 [58, 59],
                 [19, 20],
                 [38, 39],
                 [34, 35],
                 [49],
                 [31, 65],
                 [25, 26, 27],
                 [60, 61],
                 [44, 56, 57],
                 [42, 48],
                 [32, 40, 43]]
        kelas = [[6, 10, 13, 17, 23, 27, 42, 43],   # kelas[0] memiliki pelajaran 6, 10, ..., & 43
                 [45, 46, 47, 48, 49, 50, 51, 52],  # kelas[1] memiliki pelajaran 45, 46, ..., & 52
                 [1, 4, 8, 11, 15, 19, 21, 25, 29], # kelas[2] memiliki pelajaran 1, 4, ..., & 29
                 [2, 5, 9, 12, 16, 20, 22, 26, 30], # dst.
                 [32, 34, 36, 38, 54, 56, 58, 60, 67, 69],
                 [33, 35, 37, 39, 55, 57, 59, 61, 68, 70],
                 [40, 41, 62, 63, 64, 65, 66],
                 [3, 7, 14, 18, 24, 28, 31, 44, 53]]
        c_dosen = self.c_dosen_n_kelas(dosen)
        c_kelas = self.c_dosen_n_kelas(kelas)
        c_ganda = self.c_ganda()
        c_tak_tersedia = self.c_tak_tersedia()
        c_terpotong = self.c_terpotong(kelas)
        fitness = [1 / (1 + c_dosen[i] + c_kelas[i] + c_ganda[i] + c_tak_tersedia[i] +
                        c_terpotong[i]) for i in range(size)]
        return fitness

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

    def cari_gbest(self):
        """
        Cari partikel terbaik global
        """
        pbest = self.get_pbest()
        idxgbest, value = max(enumerate(self.get_fitness()), key=operator.itemgetter(1)) # pylint: disable=W0612
        gbest = pbest[idxgbest]
        self.set_gbest(gbest)

    def update_posisi(self):
        """Perbaiki posisi"""
        
        dloc = 0
        dglob = 0
        vrand = 0
        return 0

if __name__ == "__main__":
    JADWAL = Penjadwalan()

    JADWAL.posisi_awal()
    POSISI_AWAL = JADWAL.get_posisi()

    JADWAL.set_pbest(POSISI_AWAL)
    PBEST_AWAL = JADWAL.get_pbest()

    LIMIT = JADWAL.get_limit()
    ITERASI = 0
    while ITERASI < LIMIT:
        # print(f'Iterasi ke-{ITERASI+1}')
        ITERASI += 1

    print(POSISI_AWAL)
