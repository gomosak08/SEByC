import pandas as pd

def filter_and_save_csv(input_path: str, output_path: str, start_year: int, end_year: int) -> None:
    """
    Filters rows in a CSV file based on a specified year range and saves the filtered data to a new CSV file.

    Args:
        input_path (str): Path to the input CSV file.
        output_path (str): Path to save the filtered CSV file.
        start_year (int): The start year of the filtering range (inclusive).
        end_year (int): The end year of the filtering range (inclusive).

    Returns:
        None
    """
    # Read the input CSV file
    df = pd.read_csv(input_path)
    
    # Filter rows where the 'anio_levantamiento' is within the specified range
    filtered_df = df[(df['anio_levantamiento'] >= start_year) & (df['anio_levantamiento'] <= end_year)]
    
    # Save the filtered DataFrame to the output path
    filtered_df.to_csv(output_path, index=False)

# Example usage
if __name__ == "__main__":
    filter_and_save_csv("../csvs/arboles.csv", "arboles_1000_head.csv", 2015, 2020)
