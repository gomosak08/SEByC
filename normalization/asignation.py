import pandas as pd
import numpy as np
import argparse
from conditions import assign_equations, volumen

def main(args):

    df_original = pd.read_csv(args.original_path, low_memory=False)
    modelos = pd.read_excel(args.modelo_path)
    df_regression = pd.read_csv(args.regresion_path,low_memory=False)


    print("All the files where opened correctly")
    n = len(df_original)
    is_predicted = np.zeros(n)
    df_original.insert(16, 'is_predicted', is_predicted)


    index = df_regression.index
    df_original.loc[index] = df_regression


    df_original.loc[(df_original.condicion == "Tocón") & (df_original.altura <= 0) , "altura"] = .3
    df_original.loc[(df_original.condicion == "Tocón") & (df_original.altura.isnull()), "altura"] = .3

    df_original.loc[(df_original.condicion == "Tocón") & (df_original.diametro <= 0), "diametro"] = 7.5
    df_original.loc[(df_original.condicion == "Tocón") & (df_original.diametro.isnull()), "diametro"] = .3


    df_original.loc[(df_original.condicion != "Muerto") & (df_original.diametro.isnull()), "diametro"] = 7.5
    df_original.loc[(df_original.condicion != "Muerto") & (df_original.altura.isnull()), "altura"] = 1.3

    b_eq = np.empty(n, dtype=object)
    c_eq = np.empty(n, dtype=object)
    p_eq = np.empty(n, dtype=object)
    v_eq = np.empty(n, dtype=object)

    b_eq = assign_equations(df_original, modelos, variable_resultado="b", conditions="biomasa")
    c_eq = assign_equations(df_original, modelos, variable_resultado="c", conditions="carbono")
    p_eq = assign_equations(df_original, modelos, variable_resultado="p", conditions="densidad")

    np.save(f'{args.output_dir}/b_eq.npy', b_eq)
    np.save(f'{args.output_dir}/c_eq.npy', c_eq)
    np.save(f'{args.output_dir}/p_eq.npy', p_eq)

    df_original_muerto = df_original[df_original.condicion == "Muertos"]
    df_original_tocon = df_original[df_original.condicion == "Tocón"]

    v_eq = volumen(df_original_muerto, df_original_tocon, modelos,n)

    np.save(f'{args.output_dir}/v_eq.npy', v_eq)

    zeros = np.empty(n, dtype=object) 
    df_original["carbon_eq"] = c_eq
    df_original["biomasa_eq"] = b_eq
    df_original["densidad_eq"] = p_eq
    df_original["volumen_eq"] = v_eq
    # 
    df_original.to_csv(args.output_file,index=False)
    #
    print(f"The dataframe was saved in {args.output_file}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process tree data for regression.")

    

    parser.add_argument('--original_path',   type=str, help="Path to the CSV file of the original data in the cicle")
    parser.add_argument('--modelo_path',    type=str, help="Path to the CSV file of the model to take the equations")
    parser.add_argument('--regresion_path', type=str, help="Path to the CSV of the regression csv")

    parser.add_argument('--output_file', type=str, default="out.csv", help="Base path for output CSV files")
    parser.add_argument('--output_dir', type=str, help="Base path for output npy files")


    args = parser.parse_args()
    main(args)

    #python3 normalization.py --original_path ../csvs/ciclo_1.csv  --modelo_path ../csvs/modelos.xlsx --regresion_path ../linear_regression/ciclo1_out.csv 