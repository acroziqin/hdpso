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

    def masukkan_ke_seluruh_hari(self):
        """Mencari sks tiap posisi (jadwal)

        < 54 : 2 ; < 67 : 3 ; < 71 : 2 ; 1
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
                    place_where_skip_happened = iline
                    iline += 1
                elif line < 67:
                    populasi[i].insert(iline, line)
                    populasi[i].insert(iline, line)
                    place_where_skip_happened = iline
                    iline += 2
                elif line < 71:
                    populasi[i].insert(iline, line)
                    place_where_skip_happened = iline
                    iline += 1
                iline += 1
            i += 1
        return np.array(populasi)

    def fitness(self):
        """Menghitung fitness"""
        seluruh_hari = self.masukkan_ke_seluruh_hari()
        return seluruh_hari

if __name__ == "__main__":
    JADWAL = Penjadwalan()
    JADWAL.populasi_awal()
    print("Populasi Awal")
    print(JADWAL.get_populasi())
    JADWAL.fitness()
    print()
    print("Fitness")
    print(JADWAL.fitness())
