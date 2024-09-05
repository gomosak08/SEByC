import pandas as pd
import numpy as np
import argparse
from funtions import calculate_values

def main(args):
    df = pd.read_csv(args.origina_path, low_memory=False)
    modelos = pd.read_excel(args.modelo_path)

    #carbon_eq = np.load("c_eq.npy", allow_pickle=True)
    biomasa_eq  = np.load(f'{args.output_dir}/b_eq.npy', allow_pickle=True)
    densidad_eq = np.load(f'{args.output_dir}/p_eq.npy', allow_pickle=True)
    volumen_eq  = np.load(f'{args.output_dir}/v_eq.npy', allow_pickle=True)
    volumen_eq  = np.load(f'{args.output_dir}/c_eq.npy', allow_pickle=True)

    #print(len(biomasa_eq),len(df), df.columns)
    


    df = calculate_values(df, ["biomasa","volumen","carbono"])

    df.to_csv(args.output_file,index=False)
        
    print(f"The dataframe was saved in {args.output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process tree data for regression.")
    parser.add_argument('--origina_path',   type=str, help="Path to the CSV file of the original data in the cicle")
    parser.add_argument('--modelo_path',    type=str, help="Path to the CSV file of the model to take the equations")

    parser.add_argument('--output_file', type=str, default="out.csv", help="Base path for output CSV files")
    parser.add_argument('--output_dir', type=str, help="Base path for output npy files")


    args = parser.parse_args()
    main(args)
    #python3 bio_car.py --origina_path ../csvs/ciclo_1.csv --modelo_path ../csvs/modelos.xlsx --output_file calculo_biomasa.csv