"""Program ini adalah program optimasi penjadwalan mata kuliah di STAIMA Al-Hikam Malang
menggunakan Hybrid Discrete PSO"""

import numpy as np

class Penjadwalan:
    """
    Kelas untuk penjadwalan menggunakan HDPSO
    """
    def __init__(self, bloc=1, bglob=0.5, brand=0.00001):
        self.populasi = [[]]
        self.bglob = bglob
        self.bloc = bloc
        self.brand = brand
        self.rglob = []
        self.rloc = []
        self.rrand = []

    def set_populasi(self, pop):
        """
        Ganti populasi
        """
        self.populasi = pop

    def get_populasi(self):
        """
        Ambil populasi
        """
        return self.populasi

if __name__ == "__main__":
    JADWAL = Penjadwalan()
    POPULASI_AWAL = np.random.randint(1, 14, size=(JADWAL.get_size(), 20))
    print(JADWAL.get_populasi())
