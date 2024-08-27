import pandas as pd
import numpy as np
import math
from collections import Counter
from funtions import calculate_values

df = pd.read_csv("out_fixed_v2_2.csv", low_memory=False)
modelos = pd.read_excel("csvs/modelos.xlsx")

#carbon_eq = np.load("c_eq.npy", allow_pickle=True)
biomasa_eq = np.load("b_eq.npy", allow_pickle=True)
densidad_eq = np.load("p_eq.npy", allow_pickle=True)
volumen_eq = np.load("v_eq.npy", allow_pickle=True)

df['volumen_eq'] = volumen_eq
df['biomasa_eq'] = biomasa_eq
df['densidad_eq'] = densidad_eq

df = calculate_values(df)

df.to_csv("ciclo_1_bio_car.csv",index=False)
    
print(f"The dataframe was saved in ciclo_1_bio_car.csv")