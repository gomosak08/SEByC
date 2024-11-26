import pandas as pd
import numpy as np
import argparse
from regresion import regression_speices, regression_all

def main(args):
    """
    Main function to process tree data for regression analysis.

    This function reads input data from a CSV file, filters out unrealistic values, 
    and fills missing data through species-specific and general regression models.
    The results are saved to specified output files.

    Args:
        args: Command line arguments containing paths to input CSV files, 
              thresholds for filtering, and paths for output files.
    """

    # Load data
    df = pd.read_csv(args.file_path, low_memory=False, index_col=False)
    print(len(df))
    # Initialize 'is_predicted' column to mark if data is predicted
    is_predicted = np.zeros(len(df))
    df.insert(16, 'is_predicted', is_predicted)

    # Make a copy of DataFrame to work with
    df_not_nulls = df.copy()
    #print(df.iloc[0])

    # Filter out unrealistic 'altura' (height) and 'diametro' (diameter) values
    df_not_nulls.loc[(df_not_nulls['altura'] < args.min_altura) & (df_not_nulls.condicion != "Tocón"), 'altura'] = np.nan
    df_not_nulls.loc[(df_not_nulls['altura'] > args.max_altura) & (df_not_nulls.condicion != "Tocón"), 'altura'] = np.nan

    # Apply height filters specific to 'Tocón' condition
    df_not_nulls.loc[(df_not_nulls['altura'] < args.min_altura_tocon) & (df_not_nulls.condicion == "Tocón"), 'altura'] = np.nan
    df_not_nulls.loc[(df_not_nulls['altura'] > args.max_altura_tocon) & (df_not_nulls.condicion == "Tocón"), 'altura'] = np.nan

    # Filter diameter by min and max thresholds
    df_not_nulls.loc[(df_not_nulls['diametro'] < args.min_diametro), 'diametro'] = np.nan
    df_not_nulls.loc[(df_not_nulls['diametro'] > args.max_diametro), 'diametro'] = np.nan

    # Remove rows where both 'altura' and 'diametro' are NaN
    df_not_nulls = df_not_nulls[~(df_not_nulls['altura'].isnull() & df_not_nulls['diametro'].isnull())]
    #print(df_not_nulls.iloc[0])

    # Define conditions to process: 'Vivo' and 'Muerto'
    conditions = ["Vivo", "Muerto"]

    # Apply species-specific regression for each condition to estimate missing values
    for condition in conditions:
        print(f'Calculating missing data by species for {condition}')
        df_not_nulls = regression_speices(df_not_nulls, condition)

    # Identify rows with remaining NaN values in 'altura' or 'diametro'
    idex_null = df_not_nulls[(df_not_nulls.altura.isnull()) | (df_not_nulls.diametro.isnull())].index

    # Apply general regression for each condition to further estimate missing values
    for condition in conditions:
        print(f'Calculating general missing data for {condition}')
        try:
            df_not_nulls_general = regression_all(df_not_nulls.loc[idex_null], condition)
        except ValueError as e:
            print(f"An error occurred with item {condition}: {e}")
    # Update the original dataframe with filled values
    index = df_not_nulls.index
    df.loc[index] = df_not_nulls
    try:
        index = df_not_nulls_general.index
        df.loc[index] = df_not_nulls_general
    except:
        pass
    # Save processed dataframes to CSV
    df.to_csv(args.output_file, index=False)
    df_not_nulls.to_csv("regression_drop_nps.csv")
    
    print(f"The dataframe was saved in {args.output_file}")

if __name__ == "__main__":
    # Argument parser setup for command-line usage
    parser = argparse.ArgumentParser(description="Process tree data for regression.")
    
    # Define input file path and filter thresholds for height and diameter
    parser.add_argument('--file_path', type=str, default="csvs/arboles_2015.csv", help="Path to the CSV file")
    parser.add_argument('--min_altura', type=float, default=1.3, help="Minimum altura to keep")
    parser.add_argument('--max_altura', type=float, default=100.0, help="Maximum altura to keep")
    parser.add_argument('--min_diametro', type=float, default=7.5, help="Minimum diametro to keep")
    parser.add_argument('--max_diametro', type=float, default=200.0, help="Maximum diametro to keep")

    # Define height thresholds specific to 'Tocón' condition
    parser.add_argument('--min_altura_tocon', type=float, default=.3, help="Minimum altura to keep in 'Tocón' condition")
    parser.add_argument('--max_altura_tocon', type=float, default=1.29, help="Maximum altura to keep in 'Tocón' condition")

    # Define output file path
    parser.add_argument('--output_file', type=str, default="out.csv", help="Path for output CSV file")

    # Parse arguments and execute the main function
    args = parser.parse_args()
    main(args)




    #python3 linear_regression/calculate.py --file_path /home/gomosak/conafor/SEByc/labs/arboles_1000_head.csv --output_file "regression__head.csv"