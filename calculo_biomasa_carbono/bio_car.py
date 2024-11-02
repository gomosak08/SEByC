import pandas as pd
import numpy as np
import argparse
from funtions import calculate_values

def main(args):
    """
    Main function to process tree data for regression analysis.

    This function reads input data from CSV files, applies calculations on specific
    variables like biomass, volume, and carbon, and then saves the processed data 
    to an output file.

    Args:
        args: Command line arguments containing paths to input CSV files and the output directory.
    """

    # Load the original data and the model equations
    df = pd.read_csv(args.origina_path, low_memory=False)
    modelos = pd.read_csv(args.modelo_path)


    # Apply calculations for biomass, volume, and carbon based on model equations
    df = calculate_values(df, ["biomasa", "volumen", "carbono"])

    # Save the processed DataFrame to CSV
    df.to_csv(args.output_file, index=False)
    print(f"The dataframe was saved in {args.output_file}")

if __name__ == "__main__":
    # Argument parser setup for command-line usage
    parser = argparse.ArgumentParser(description="Process tree data for regression.")
    
    # Define arguments for file paths and output directory
    parser.add_argument('--origina_path', type=str, help="Path to the CSV file of the original data in the cycle")
    parser.add_argument('--modelo_path', type=str, help="Path to the CSV file containing model equations")
    parser.add_argument('--output_file', type=str, default="out.csv", help="Path for the output CSV file")
    parser.add_argument('--output_dir', type=str, help="Path for output .npy files if needed")

    # Parse arguments and execute the main function
    args = parser.parse_args()
    main(args)



#python3 calculo_biomasa_carbono/bio_car.py --origina_path runs/run_34/normalizaded_34_head.csv  --modelo_path csvs/modelos.xlsx \
#--output_file runs/run_34/calculo_bio_car_34_head.csv --output_dir runs/run_34/npy/

