"""Program ini adalah program optimasi penjadwalan mata kuliah di STAIMA Al-Hikam Malang
menggunakan Hybrid Discrete PSO"""

import random
import numpy as np

class Penjadwalan:
    """Kelas untuk penjadwalan menggunakan HDPSO"""
    def __init__(self, bloc=1, bglob=0.5, brand=0.00001, size=5):
        self.populasi = [[]]
        self.bglob = bglob
        self.bloc = bloc
        self.brand = brand
        self.rglob = []
        self.rloc = []
        self.rrand = []
        self.size = size

    def set_populasi(self, pop):
        """Ganti populasi"""
        self.populasi = pop

    def get_populasi(self):
        """Ambil populasi"""
        return self.populasi

    def get_size(self):
        """Ambil ukuran populasi"""
        return self.size

    # def r(self, m, n, o):
        # m, n are the number of rows, cols of output
        # return np.random.rand(m, n).argsort(axis=axis)
        # for i in range(len(o)):
        #     pass
        # o = np.array(np.arange(m, n))
        # np.random.shuffle(o)
        # p = np.concatenate(o, o)
        # p = np.array([np.array(o), np.array(o))
        # return p

if __name__ == "__main__":
    JADWAL = Penjadwalan()
    # POPULASI_AWAL = np.random.randint(1, 14, size=(JADWAL.get_size(), 20))
    POPULASI_AWAL = random.sample(range(1, 11), 10)
    POPULASI_DUA = random.sample(range(1, 11), 10)
    # POPULASI_AWAL = JADWAL.r(1, 11, 1)
    # POPULASI_AWAL = np.arange(1, 11)

    # np.random.shuffle(POPULASI_AWAL)
    X = list(zip(POPULASI_AWAL, POPULASI_DUA))
    JADWAL.set_populasi(np.transpose(X))
    print(JADWAL.get_populasi())
