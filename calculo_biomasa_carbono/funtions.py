import math
import pandas as pd
import numpy as np
from tqdm import tqdm

def str2function(function, equation_type):
    """
    Converts a string representation of an equation into a lambda function with the correct variables and mathematical expressions.

    ### Parameters:
    - **function** (`str`): The string representation of the equation.
    - **equation_type** (`str`): The type of equation, which can be "vol", "bio", or "car". This determines the specific variable replacements and list of variables used.

    ### Returns:
    - **function** (`lambda`): The generated lambda function based on the input string.
    - **filtered_list** (`list`): The list of variables used in the lambda function.

    ### Example Usage:
    ```python
    equation_str = "[d130] * [ht] + [p]"
    lambda_func, variables = str2function(equation_str, "bio")
    result = lambda_func(10, 5, 0.9)  # Example usage of the lambda function
    ```

    ### Notes:
    - The function performs necessary replacements (like `[d130]` to `d130`) and handles specific mathematical expressions like `Exp` and `LOG`.
    """

    # Replacements and variables based on the equation type
    replacements = {
        "vol": {
            "[d130]": "d130",
            "[ht]": "ht"
        },
        "bio": {
            "Exp": "math.exp",
            "[p]": "densi",
            "[v]": "v",
            "[d130]": "d130",
            "[ht]": "ht",
            "LOG": "math.log"
        },
        "car": {
            "[b]": "b",
            "[d130]": "d130",
            "[ht]": "ht"
        }
    }

    variable_sets = {
        "vol": ["d130", "ht"],
        "bio": ["densi", "v", "d130", "ht"],
        "car": ["b", "d130", "ht"]
    }

    # Validate equation_type
    if equation_type not in replacements or equation_type not in variable_sets:
        raise ValueError(f'{equation_type} is not known. The only available options are "vol", "bio", "car".')

    # Apply replacements based on the equation type
    for key, value in replacements[equation_type].items():
        function = function.replace(key, value)

    # Filter the variables based on which are used in the function
    variables = variable_sets[equation_type]
    filtered_list = [var for var in variables if var in function]

    # Generate the lambda function
    lambda_function = eval(f'lambda {", ".join(filtered_list)}: {function}')

    return lambda_function, filtered_list


def calculate_values(df, calculate=["volumen", "biomasa", "carbono"]):
    """
    Calculates volume, biomass, and carbon based on equations provided in the DataFrame.

    ### Parameters:
    - **df** (`pd.DataFrame`): DataFrame containing the data along with the equations for volume, biomass, and carbon.
    - **calculate** (`list` of `str`): List of strings indicating which values to calculate. 
      Options include "volumen", "biomasa", and "carbono". Default is to calculate all.

    ### Returns:
    - **df** (`pd.DataFrame`): The input DataFrame with additional columns for calculated volume, biomass, and carbon 
      based on the specified calculation.

    ### Notes:
    - The function uses the `str2function` helper to dynamically convert equation strings to lambda functions.
    - The function handles different variable combinations based on the equations and assigns the calculated values to the corresponding columns.
    """

    # Initialize the result columns if they are specified in the calculate list
    if "volumen" in calculate:
        df['volumen'] = np.nan
    if "biomasa" in calculate:
        df['biomasa'] = np.nan
    if "carbono" in calculate:
        df['carbono'] = np.nan

    if "volumen" in calculate:
        for row in tqdm(df.itertuples(), total=len(df)):
            index = row.Index
            try:
                if not pd.isnull(row.volumen_eq):
                    f, var = str2function(row.volumen_eq, "vol")
                    df.at[index, 'volumen'] = f(row.diametro, row.altura)
                else:
                    pass
            except Exception as e:
                print(f"Error calculating volume at index {index}: {e}")

    # Iterate over the DataFrame to calculate biomass if specified
    if "biomasa" in calculate:
        for row in tqdm(df.itertuples(), total=len(df)):
            index = row.Index
            try:
                f, var = str2function(row.biomasa_eq, "bio")
                #print(var)
                if var == ['densi', 'd130', 'ht']:
                    df.at[index, 'biomasa'] = f(float(row.densidad_eq), row.diametro, row.altura)
                elif var == ['d130', 'ht']:
                    df.at[index, 'biomasa'] = f(row.diametro, row.altura)
                elif var == ['densi', 'v']:
                    df.at[index, 'biomasa'] = f(float(row.densidad_eq), row.volumen)
                elif var == ['d130', 'ht', 'p']:
                    df.at[index, 'biomasa'] = f(float(row.densidad_eq), row.diametro, row.densidad_eq)
                else:
                    df.at[index, 'biomasa'] = f(row.diametro)
            except Exception as e:
                print(f"Error calculating biomass at index {index}: {e}")
                print(row.biomasa_eq)


    # Iterate over the DataFrame to calculate carbon if specified
    if "carbono" in calculate:
        for row in tqdm(df.itertuples(), total=len(df)):
            index = row.Index
            try:
                f, var = str2function(row.carbon_eq, "car")
                if var == ['b']:
                    df.at[index, 'carbono'] = f(row.biomasa)
                elif var == ['d130']:
                    df.at[index, 'carbono'] = f(row.diametro)
                else:
                    df.at[index, 'carbono'] = f(row.diametro, row.altura)
            except Exception as e:
                print(f"Error calculating carbon at index {index}: {e}")

    return df


def area_basal(df, n):
    """
    Calculate the basal area for each row in a DataFrame.

    Parameters:
    ----------
    df : pandas.DataFrame
        A DataFrame containing the column `diametro` (diameter in centimeters).
        Each row represents an individual observation.
    n : int
        The total number of rows or entries in the DataFrame.

    Returns:
    -------
    numpy.ndarray
        An array of length `n` where each element corresponds to the basal area 
        calculated for the respective row in the DataFrame. The basal area is 
        computed using the formula: 
            π * ( (diameter / 100) / 2 )²

    Notes:
    -----
    - The function assumes the `diametro` column exists in the input DataFrame `df`.
    - The returned values are in square meters.
    - The `tqdm` library is used to display a progress bar during iteration.
    - The `math` and `numpy` libraries are required for the computations.
    - Indexes in `df` must align with the range of `n`.

    Example:
    -------
    >>> import pandas as pd
    >>> import numpy as np
    >>> from tqdm import tqdm
    >>> import math

    >>> data = {'diametro': [30, 40, 50]}
    >>> df = pd.DataFrame(data)
    >>> n = len(df)
    >>> basal_areas = area_basal(df, n)
    >>> print(basal_areas)
    [0.07068583470577035, 0.12566370614359174, 0.19634954084936207]
    """
    print("Calculating area basal")
    v_eq = np.empty(n, dtype=object)

    for row in tqdm(df.itertuples(), total=len(df)):
        index = row.Index
        v_eq[index] = math.pi * ((((row.diametro) / 100) / 2) ** 2)
    return v_eq

def status(df, n):
    """
    Validate the status of biomass and carbon data for each row in a DataFrame.

    Parameters:
    ----------
    df : pandas.DataFrame
        A DataFrame containing the columns `biomasa` and `carbon`. Each row represents
        an individual observation.
    n : int
        The total number of rows or entries in the DataFrame.

    Returns:
    -------
    numpy.ndarray
        An array of length `n` where each element contains the status for the 
        corresponding row in the DataFrame. The status is determined as follows:
        - "Calculated" if both `biomasa` and `carbon` are NaN.
        - "Error" otherwise.

    Notes:
    -----
    - The function assumes the `biomasa` and `carbon` columns exist in the input DataFrame `df`.
    - The `tqdm` library is used to display a progress bar during iteration.
    - The `math.isnan()` function is used to check for NaN values.
    - The `numpy` library is required for creating the output array.

    Example:
    -------
    >>> import pandas as pd
    >>> import numpy as np
    >>> from tqdm import tqdm
    >>> import math

    >>> data = {'biomasa': [float('nan'), 20.5, float('nan')],
    ...         'carbon': [float('nan'), 10.5, 15.0]}
    >>> df = pd.DataFrame(data)
    >>> n = len(df)
    >>> status_array = status(df, n)
    >>> print(status_array)
    ['Calculated', 'Error', 'Error']
    """
    v_eq = np.empty(n, dtype=object)
    print("Validating status")
    for row in tqdm(df.itertuples(), total=len(df)):
        index = row.Index
        if math.isnan(row.biomasa) and math.isnan(row.carbon):
            v_eq[index] = "Calculated"
        else:
            v_eq[index] = "Error"
    return v_eq
