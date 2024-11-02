import pandas as pd
import numpy as np
import argparse
from regresion import regression_speices,regression_all

def main(args):
    # Read CSV file
    df = pd.read_csv(args.file_path, low_memory=False, index_col = False)

    # Create a copy of the DataFrame
    is_predicted = np.zeros(len(df))
    df.insert(16, 'is_predicted', is_predicted)
    df_not_nulls = df.copy()


    print(df.iloc[0])
    # Filter out unrealistic height and diameter values by setting them to NaN
    df_not_nulls.loc[(df_not_nulls['altura'] <= args.min_altura) & (df_not_nulls.condicion != "Tocón"), 'altura'] = np.nan
    df_not_nulls.loc[(df_not_nulls['altura'] >= args.max_altura) & (df_not_nulls.condicion != "Tocón"), 'altura'] = np.nan

    df_not_nulls.loc[(df_not_nulls['altura'] <= args.min_altura_tocon) & (df_not_nulls.condicion == "Tocón"), 'altura'] = np.nan
    df_not_nulls.loc[(df_not_nulls['altura'] >= args.max_altura_tocon) & (df_not_nulls.condicion == "Tocón"), 'altura'] = np.nan


    df_not_nulls.loc[(df_not_nulls['diametro'] <= args.min_diametro), 'diametro'] = np.nan
    df_not_nulls.loc[(df_not_nulls['diametro'] >= args.max_diametro), 'diametro'] = np.nan

    #print(df_not_nulls.loc[75817])

    # Remove rows where both 'altura' and 'diametro' are NaN
    #dropped_indices = df_not_nulls[(df_not_nulls['altura'].isnull()) & (df_not_nulls['diametro'].isnull())].index
    df_not_nulls = df_not_nulls[~(df_not_nulls['altura'].isnull() & df_not_nulls['diametro'].isnull())]
    #print(df_not_nulls.loc[75817])
    print(df_not_nulls.iloc[0])

    # Add 'is_predicted' column with all zeros

    # Apply regression for each condition and save to CSV
    conditions = ["Vivo","Muerto"]

    for condition in conditions:
        print(f'calculating missing data by specie for {condition}')
        df_not_nulls = regression_speices(df_not_nulls, condition)
    #print(len(df_not_nulls))
    #print(f'this is after calculate  data by specie \n {df_not_nulls.loc[75817]}')

    idex_null = df_not_nulls[(df_not_nulls.altura.isnull()) | (df_not_nulls.diametro.isnull())].index
    #print(len(idex_null))
    for condition in conditions:
        print(f'calculating missing data general data for {condition}')
        df_not_nulls_general = regression_all(df_not_nulls.loc[idex_null], condition)
    #print(len(df_not_nulls), 'lllll')

    #print(f'this is after calculating general data \n {df_not_nulls.loc[75818]}')
    
    #print(df_not_nulls.loc[75818])
    #print(df_not_nulls[df_not_nulls.id == 75818].index)
    print(df_not_nulls.iloc[0])
    
    index = df_not_nulls.index
    df.loc[index] = df_not_nulls
    print(df.iloc[0])
    index = df_not_nulls_general.index
    #print(index[0])
    df.loc[index] = df_not_nulls_general

    #print(df_not_nulls[df_not_nulls.id == 75818].index)

    print(df.iloc[0])
    
    df.to_csv(args.output_file, index = False)
    df_not_nulls.to_csv("regression_drop_nps.csv")
    
    print(f"The dataframe was saved in {args.output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process tree data for regression.")
    parser.add_argument('--file_path', type=str, default="csvs/arboles_2015.csv", help="Path to the CSV file")
    parser.add_argument('--min_altura', type=float, default=1.3, help="Minimum altura to keep")
    parser.add_argument('--max_altura', type=float, default=100.0, help="Maximum altura to keep")

    parser.add_argument('--min_diametro', type=float, default=7.5, help="Minimum diametro to keep")
    parser.add_argument('--max_diametro', type=float, default=200.0, help="Maximum diametro to keep")

    parser.add_argument('--min_altura_tocon', type=float, default=.3, help="Minimum altura to keep in tocon condition")
    parser.add_argument('--max_altura_tocon', type=float, default=1.29, help="Maximum altura to keep in tocon condition")
    parser.add_argument('--output_file', type=str, default="out.csv", help="Base path for output CSV files")

    args = parser.parse_args()
    main(args)



    #python3 linear_regression/calculate.py --file_path /home/gomosak/conafor/SEByc/labs/arboles_1000_head.csv --output_file "regression__head.csv"