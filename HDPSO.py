"""Program ini adalah program optimasi penjadwalan mata kuliah di STAIMA Al-Hikam Malang
menggunakan Hybrid Discrete PSO"""

import random
import numpy as np

class Penjadwalan:
    """Kelas untuk penjadwalan menggunakan HDPSO"""
    def __init__(self, bloc=1, bglob=0.5, brand=0.00001, size=5, n_posisi=577):
        self.populasi = [[]]
        self.bglob = bglob
        self.bloc = bloc
        self.brand = brand
        self.rglob = []
        self.rloc = []
        self.rrand = []
        self.size = size
        self.n_posisi = n_posisi

    def set_populasi(self, pop):
        """Ganti populasi"""
        self.populasi = pop

    def get_populasi(self):
        """Ambil populasi"""
        return self.populasi

    def get_size(self):
        """Ambil ukuran populasi"""
        return self.size

    def get_n_posisi(self):
        """Ambil banyak dimensi"""
        return self.n_posisi

    def populasi_awal(self):
        """Inisialisasi populasi awal"""
        size = self.get_size()
        n_posisi = self.get_n_posisi()
        partikel = []
        i = 0
        while i < size:
            partikel.append(random.sample(range(1, n_posisi + 1), n_posisi))
            i += 1
        self.set_populasi(np.array(partikel))

    def seluruh_hari(self):
        """Memasukkan posisi tiap solusi ke seluruh hari
        dengan memanfaatkan SKS tiap posisi (pengajaran)
        """
        populasi = self.get_populasi().tolist()
        size = self.get_size()
        i = 0
        while i < size:
            iline = 0
            while iline < len(populasi[i]):
                line = populasi[i][iline]
                if line < 54:
                    populasi[i].insert(iline, line)
                    iline += 1
                elif line < 67:
                    populasi[i].insert(iline, line)
                    populasi[i].insert(iline, line)
                    iline += 2
                elif line < 71:
                    populasi[i].insert(iline, line)
                    iline += 1
                iline += 1
            i += 1
        return np.array(populasi)

    def jadi_jadwal(self):
        """Jadikan tiap solusi menjadi jadwal layaknya jadwal sebenarnya."""
        return 0

    def c_dosen(self):
        """Constraint Dosen bentrok ngajar. Sama Jam & Hari."""
        populasi = self.get_populasi().tolist()
        # Pelajaran dari Dosen
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

        # Indeks pelajaran Dosen (D) dari partikel (P). Nilai P ada di indeks ke-x dari D
        nilaip_indeksd = []  # [Dosen ke, Pelajaran ke]
        # Dari partikel (P), Nilai yang di bawah 71 ada di indeks ke berapa saja?
        indeksp_bawah71 = []
        for i in populasi:
            row = []
            for k in i:
                if k < 71:
                    # Masukkan i dan indeks dari j yang isinya kurang dari 71 ke row
                    row.append([[i, j.index(k)] for i, j in enumerate(dosen) if k in j][0])
            nilaip_indeksd.append(row)
            # Masukkan i ke-x yang kurang dari 71 ke row71
            row71 = list(filter(lambda x: i[x] < 71, range(len(i))))
            indeksp_bawah71.append(row71)

        nilaid_selainp = []  # Nilai D selain nilai P
        for i in nilaip_indeksd:
            row = []
            for j in i:
                temp = dosen[j[0]][:]  # Salin Dosen j[0] ke C
                # Menghapus Dosen j[0] pelajaran j[1] tanpa menggangu variabel D asal
                del temp[j[1]]
                row.append(temp)  # Masukkan C ke row
            nilaid_selainp.append(row)

        batasan1 = []  # Batasan pertama: bentrok dosen
        for key, val in enumerate(nilaid_selainp):
            count = 0
            for i, j in enumerate(val):
                for k in j:
                    if (populasi[key].index(k) - indeksp_bawah71[key][i]) % 60 == 0:
                        count += 1
                    if (populasi[key].index(k) + 1 - indeksp_bawah71[key][i]) % 60 == 0:
                        count += 1
                    if 54 <= k < 67:
                        if (populasi[key].index(k) + 2 - indeksp_bawah71[key][i]) % 60 == 0:
                            count += 1
            batasan1.append(count)

        return batasan1

    def fitness(self):
        """Menghitung fitness"""
        # seluruh_hari = self.seluruh_hari()[0][10]
        # jadwal = self.jadi_jadwal(seluruh_hari)
        return self.c_dosen()

if __name__ == "__main__":
    JADWAL = Penjadwalan()
    JADWAL.populasi_awal()
    # print("Populasi Awal")
    # print(JADWAL.get_populasi())
    # JADWAL.fitness()
    # print()
    # print("Fitness")
    print(JADWAL.fitness())
