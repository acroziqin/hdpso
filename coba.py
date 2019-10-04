import pandas as pd
import numpy as np
import random as rd

df_pelajaran = pd.read_excel('data.xlsx', 'Pelajaran')
df_hari = pd.read_excel('data.xlsx', 'Hari')
df_periode = pd.read_excel('data.xlsx', 'Periode')
df_ruangan = pd.read_excel('data.xlsx', 'Ruangan')
df_parameter = pd.read_excel('data.xlsx', 'Parameter')

#Jumlah Posisi (n_posisi)

# print(pelajaran['No.'].count()) = 68
# print(pelajaran.loc[(pelajaran['SKS'] > 3)]['SKS'].count()) = 2
# print(hari['No.'].count()) = 5
# print(periode['No.'].count()) = 12
# print(ruangan['No.'].count()) = 11
# print(pelajaran['SKS'].sum()) = 153

# 68 + 2 + 507 = 577
# 68 + 2 + (660 - 153) = 577
# 68 + 2 + ((5 * 12 * 11) - 153) = 577

df_tanpa_ganda = df_pelajaran.loc[(df_pelajaran['SKS'] < 4)]
df_ganda = df_pelajaran.loc[(df_pelajaran['SKS'] > 3)]
df_ganda = df_ganda.append(df_ganda).reset_index(drop=True)
df_ganda['No.'] = df_ganda.index + df_tanpa_ganda['No.'].count() + 1
df_ganda['SKS'] = df_ganda['SKS'] // 2
df_dgn_ganda = df_tanpa_ganda.append(df_ganda).reset_index(drop=True)

def split_list(a_list):
    half = len(a_list)//2
    return [a_list[:half], a_list[half:]]

A = split_list(df_ganda['No.'].tolist())
A = np.transpose(A).tolist()

x = "0"
if isinstance(x, int):
    print(True)
else:
    print(False)

# print(rd.sample(range(1, 10 + 1), 10))
# df = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))
# df2 = pd.DataFrame([[5, 6], [7, 8]], columns=list('AB'))
# df = df.append(df2)
# print(df_dgn_ganda)
# print(int(5/2))


# for index, row in df.iterrows():
#     print(index[0], index[1])

# print(pelajaran.sort_values('Dosen').iloc[0,3])
# kelas = []
# kel = []
# nama_kel = df_dgn_ganda.sort_values('Kelas').iloc[0,4]
# df_kel = df_dgn_ganda.groupby(['Kelas', 'No.'])
# for index in df_kel.groups.keys():
    # dos.append(index[1])
    # if index[0] == nama_kel:
    #     kel.append(index[1])
    #     if index[1] == df_dgn_ganda.sort_values('Kelas').iloc[-1,0]:
    #         kelas.append(kel)    
    # else:
    #     kelas.append(kel)
    #     kel = [index[1]]
    #     nama_kel = index[0]

# print(df_dgn_ganda.sort_values('Dosen').iloc[-1,0])

# df = pd.DataFrame({'group':[0,1,1,1,2,2,3,3,3], 'val':np.arange(9)})
# gp = df_dgn_ganda.groupby(['Dosen', 'No.'])
# gp.groups
# print(gp.groups.keys())

# for i in gp.groups.keys():
#     print(i)