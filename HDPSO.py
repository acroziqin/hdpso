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
        dosen = [[54, 55],   # dosen[0] mengajar pelajaran 54 & 55
                 [3, 51],    # dosen[1] mengajar pelajaran 3 & 51
                 [1, 2, 53], # dosen[2] mengajar pelajaran 1, 2, & 53
                 [67, 68, 69, 70],
                 [4, 5, 6, 7],
                 [15, 16, 17, 18],
                 [8, 9, 10, 64],
                 [36, 37, 41, 45],
                 [28, 29, 30, 46],
                 [23, 33, 50, 62],
                 [21, 22, 24],
                 [11, 12, 13, 14],
                 [58, 59],
                 [19, 20],
                 [38, 39],
                 [34, 35],
                 [31, 65],
                 [25, 26, 37],
                 [60, 61],
                 [44, 56, 57],
                 [42, 48],
                 [32, 40, 43]]
        return populasi[0].index(dosen[0][0])

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
