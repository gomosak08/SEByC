import pandas as pd
import numpy as np
from conditions import assign_equations, volumen

df_original = pd.read_csv("out_tocones.csv", low_memory=False)
modelos = pd.read_excel("csvs/modelos.xlsx")
df_regression = pd.read_csv("csvs/arboles_2015.csv",low_memory=False)

n = len(df_original)
is_predicted = np.zeros(n)
df_original.insert(15, 'is_predicted', is_predicted)


index = df_regression.index
df_original.loc[index] = df_regression


df_original.loc[(df_original.condicion == "Tocón") & (df_original.altura <= 0) , "altura"] = .3
df_original.loc[(df_original.condicion == "Tocón") & (df_original.altura.isnull()), "altura"] = .3

df_original.loc[(df_original.condicion == "Tocón") & (df_original.diametro <= 0), "diametro"] = 7.5
df_original.loc[(df_original.condicion == "Tocón") & (df_original.diametro.isnull()), "diametro"] = .3


df_original.loc[(df_original.condicion != "Tocón") & (df_original.diametro.isnull()), "diametro"] = 7.5
df_original.loc[(df_original.condicion != "Tocón") & (df_original.altura.isnull()), "altura"] = 1.3

b_eq = np.empty(n, dtype=object)
c_eq = np.empty(n, dtype=object)
p_eq = np.empty(n, dtype=object)
v_eq = np.empty(n, dtype=object)

b_eq = assign_equations(df_original, modelos, variable_resultado="p", conditions="biomasa")
c_eq = assign_equations(df_original, modelos, variable_resultado="p", conditions="carbono")
p_eq = assign_equations(df_original, modelos, variable_resultado="p", conditions="densidad")

df_original_muerto = df_original[df_original.condicion == "Muertos"]
df_original_tocon = df_original[df_original.condicion == "Tocón"]

v_eq = volumen(df_original_muerto, df_original_tocon, modelos)


np.save('b_eq.npy', b_eq)
np.save('c_eq.npy', c_eq)
np.save('p_eq.npy', p_eq)
np.save('v_eq.npy', v_eq)

zeros = np.empty(n, dtype=object) 
df_original_tocon["volumen_eq"] = zeros
df_original_tocon["biomasa_eq"] = zeros
df_original_tocon["densidad_eq"] = zeros

df_original_tocon["volumen"] = zeros
df_original_tocon["biomasa"] = zeros
df_original_tocon["carbono"] = zeros