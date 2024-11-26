import pandas as pd
import numpy as np
import argparse
from conditions import assign_equations, volumen, assign_den
from tqdm import tqdm

def main(args):
    """
    Main function to process tree data for regression analysis.

    This function reads input data from CSV files, applies various data processing steps,
    fills missing values, and assigns equations for biomass, carbon, density, and volume 
    based on predefined models. Finally, it outputs the processed data to a CSV file.

    Args:
        args: Command line arguments containing paths to input CSV files and output directory.
    """

    # Load data
    df_original = pd.read_csv(args.origina_path, low_memory=False)
    modelos = pd.read_csv(args.modelo_path)
    print("All the files were opened correctly")
    
    # Total number of rows in the data
    n = args.len_df

    # Data Cleaning: Filling missing or invalid values based on conditions
    # Set height to 0.3 for 'Tocón' condition if height is <= 0 or NaN
    df_original.loc[(df_original.condicion == "Tocón") & (df_original.altura < .3), "altura"] = .3
    df_original.loc[(df_original.condicion == "Tocón") & (df_original.altura.isnull()), "altura"] = .3

    # Set diameter to 7.5 for 'Tocón' condition if diameter is <= 0 or NaN
    df_original.loc[(df_original.condicion == "Tocón") & (df_original.diametro < 7.5), "diametro"] = 7.5
    df_original.loc[(df_original.condicion == "Tocón") & (df_original.diametro.isnull()), "diametro"] = 7.5

    # Repeat similar logic for 'Muerto' and 'Vivo' conditions with different default values
    df_original.loc[(df_original.condicion == "Muerto") & (df_original.diametro < 7.5), "diametro"] = 7.5
    df_original.loc[(df_original.condicion == "Muerto") & (df_original.diametro.isnull()), "diametro"] = 7.5
    df_original.loc[(df_original.condicion == "Muerto") & (df_original.altura < 1.3), "altura"] = 1.3
    df_original.loc[(df_original.condicion == "Muerto") & (df_original.altura.isnull()), "altura"] = 1.3

    df_original.loc[(df_original.condicion == "Vivo") & (df_original.diametro < 7.5), "diametro"] = 7.5
    df_original.loc[(df_original.condicion == "Vivo") & (df_original.diametro.isnull()), "diametro"] = 7.5
    df_original.loc[(df_original.condicion == "Vivo") & (df_original.altura <= 1.3), "altura"] = 1.3
    df_original.loc[(df_original.condicion == "Vivo") & (df_original.altura.isnull()), "altura"] = 1.3

    # Initialize equation vectors to store computed values
    b_eq = np.empty(n, dtype=object)
    c_eq = np.empty(n, dtype=object)
    p_eq = np.empty(n, dtype=object)
    v_eq = np.empty(n, dtype=object)

    # Separate data based on 'condicion' type for volume calculations
    df_original_muerto = df_original[df_original.condicion == "Muerto"]
    df_original_tocon = df_original[df_original.condicion == "Tocón"]
    v_eq = volumen(df_original_muerto, df_original_tocon, modelos, n)

    #print(v_eq)
    # Process biomass equations for 'Vivo' data
    data = df_original[df_original.condicion == "Vivo"]
    eq = modelos[(modelos["variable_resultado"] == "b") & (modelos["activo"] == 1)]
    print(len(data))
    b_eq = assign_equations(data, eq, vector=b_eq, conditions="biomasa")

    # Assign biomass equations for 'Muerto' and 'Tocón' conditions using custom logic
    for row in tqdm(df_original_muerto.itertuples(), total=len(df_original_muerto)):
        index = row.Index
        b_eq[index] = modelos.iloc[2883, 6]

    for row in tqdm(df_original_tocon.itertuples(), total=len(df_original_tocon)):
        index = row.Index
        if not np.isnan(row.grado_putrefaccion):
            eq = modelos.iloc[2884, 6]
            eq += f"/{row.grado_putrefaccion} * [p]"
            b_eq[index] = eq
        else:
            b_eq[index] = modelos.iloc[2884, 6]
    print("done biomasa")

    # Assign carbon equations based on specific conditions
    eq = modelos[(modelos["variable_resultado"] == "c") & (modelos["activo"] == 1) & (modelos["Funciones"] == "fraciones de carbono")]
    c_eq = assign_equations(df_original, eq, vector=c_eq, conditions="carbono")
    
    # Assign density equations
    eq = modelos[(modelos["variable_resultado"] == "p") & (modelos["activo"] == 1)]
    p_eq = assign_den(df_original, eq, vector=p_eq)

    print(p_eq[-10:])

    # Add computed equations to the original dataframe
    df_original.loc[:,"carbon_eq"] = c_eq
    df_original.loc[:,"biomasa_eq"] = b_eq
    df_original.loc[:,"densidad_eq"] = p_eq
    df_original.loc[:,"volumen_eq"] = v_eq


    # Save the processed dataframe to CSV
    df_original.to_csv(args.output_file, index=False)
    print(f"The dataframe was saved in {args.output_file}")

if __name__ == "__main__":
    # Argument parser setup for command-line usage
    parser = argparse.ArgumentParser(description="Process tree data for regression.")

    # Define arguments
    parser.add_argument('--modelo_path',    type=str, help="Path to the CSV file containing the model equations.")
    parser.add_argument('--origina_path', type=str, help="Path to the CSV file containing the regression data.")
    parser.add_argument('--output_file', type=str, default="out.csv", help="Path for the output CSV file.")
    parser.add_argument('--len_df', type=int, help ="The len of the df" )
    #parser.add_argument('--output_dir', type=str, help="Directory for output .npy files (if applicable).")

    # Parse arguments and execute the main function
    args = parser.parse_args()
    main(args)

    #python3 normalization/asignation.py --original_path labs/arboles_1000_head.csv  --modelo_path csvs/modelo2.csv --regresion_path labs/norm_1000_head.csv