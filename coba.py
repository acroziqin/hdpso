import pandas as pd
import numpy as np
import random as rd

df_pelajaran = pd.read_excel('data.xlsx', 'Pelajaran')
df_hari = pd.read_excel('data.xlsx', 'Hari')
df_periode = pd.read_excel('data.xlsx', 'Periode')
df_ruangan = pd.read_excel('data.xlsx', 'Ruangan')
df_parameter = pd.read_excel('data.xlsx', 'Parameter')

print(df_hari['No.'].count())