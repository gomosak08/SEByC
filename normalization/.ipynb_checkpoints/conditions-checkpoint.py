import numpy as np
import pandas as pd
from tqdm import tqdm


def assign_equations(df, modelos, variable_resultado="p", conditions=None):
    """
    Assigns equations based on specific conditions and fills in a result array.

    ### Parameters:
    - **df** (`pd.DataFrame`): The DataFrame containing the main dataset.
    - **modelos** (`pd.DataFrame`): The DataFrame containing the equation models.
    - **variable_resultado** (`str`): The variable to filter in the models DataFrame. Default is "p".
    - **conditions** (`list of functions`): A list of functions that define the conditions to filter models. Each function should take in the `modelos` DataFrame and a row from `df` and return a filtered DataFrame. Default conditions are:
        1. Match `genero` and `epiteto`.
        2. Match `genero` and when `epiteto` is missing.
        3. Match only `genero`.
        4. Match only `clave_ecoregion_n2`.

    ### Returns:
    - **np.ndarray**: An array containing the assigned equations based on the provided conditions.

    ### Example Usage:
    ```python
    conditions_den = [
        lambda df, row: df[(df.genero == row.genero) & (df.epiteto == row.epiteto)],
        lambda df, row: df[(df.genero == row.genero) & (df.epiteto.isnull())],
        lambda df, row: df[(df.genero == row.genero)],
        lambda df, row: df[df.clave_ecoregion_n2 == row.clave_ecoregion_n2]
    ]

    assigned_equations = assign_equations(df, modelos, "p", conditions_den)
    ```

    ### Notes:
    - The function iterates over each row in the main `df`, applying each condition sequentially until a match is found. If no match is found, the index is printed.
    - The function uses the first matching model found based on the conditions, and it assigns the corresponding equation (fifth column) to the result array.
    """

    # Default conditions if none are provided
    if conditions == "biomasa":
        conditions_eq = biomasa
    elif conditions == "carbono":
        conditions_eq = carbono
    elif conditions == "densidad":
        conditions_eq = densidad
    else:
        raise ValueError(f'{conditions} is not known. The only available options are "biomasa", "carbono", "densidad".')

    # Filter the models to only include those with the desired variable result
    equations = modelos[modelos.variable_resultado == variable_resultado]

    # Initialize an array to store the equations
    n = len(df)
    p_eq = np.empty(n, dtype=object)

    # Iterate over each row in the main dataframe
    #for index, row in df.iterrows():
    for row in tqdm(df.itertuples(), total=len(df)):
        index = row.Index
        flag = False
        for condition in conditions_eq:
            # Apply the condition to filter equations
            equation_df = condition(equations, row)
            if not equation_df.empty:
                return equation_df
                equation = select_eq(df)
                # If a match is found, assign the equation and break
                p_eq[index] = equation_df.iloc[0, 5]  # The 6th column is selected here
                flag = True
                break
        if not flag:
            # Print the index if no condition matched
            print(f"No match found for index: {index}")
            print(conditions)
            break

    return p_eq


def volumen(df_muerto, df_tocon, modelos):
    """
    Assigns specific equations based on conditions to the `v_eq` array.

    ### Parameters:
    - **df_muerto** (`pd.DataFrame`): DataFrame containing dead tree data.
    - **df_tocon** (`pd.DataFrame`): DataFrame containing stump data.
    - **modelos** (`pd.DataFrame`): DataFrame containing model equations.

    ### Returns:
    - **np.ndarray**: An array containing the assigned equations based on the conditions.

    ### Example Usage:
    ```python
    assigned_equations = assign_specific_equations(df_muerto, df_tocon, modelos)
    ```

    ### Notes:
    - For rows in `df_muerto`, the function assigns the equation found in the 2883rd row and 6th column of `modelos`.
    - For rows in `df_tocon`, if `grado_putrefaccion` is not NaN, the function appends its value to the equation found in the 2884th row and 6th column of `modelos`. Otherwise, it assigns the equation without appending anything.
    - The function returns the `v_eq` array with the assigned equations.
    """

    # Initialize the result array with the size of both dataframes combined
    n = len(df_muerto) + len(df_tocon)
    v_eq = np.empty(n, dtype=object)

    # Process the df_muerto dataframe
    for index, row in df_muerto.iterrows():
        v_eq[index] = modelos.iloc[2883, 5]

    # Process the df_tocon dataframe
    for index, row in df_tocon.iterrows():
        if not np.isnan(row.grado_putrefaccion):
            eq = modelos.iloc[2884, 5]
            eq += f"/{row.grado_putrefaccion}"
            print(eq, index)
            v_eq[index + len(df_muerto)] = eq
        else:
            v_eq[index + len(df_muerto)] = modelos.iloc[2884, 5]

    return v_eq
# Conditions

biomasa = [

            
            lambda df, row: df[(df.genero == row.genero) & (df.epiteto == row.epiteto) 
                    & (df.clave_ecoregion_n2 == row.clave_ecoregion_n2) & (df.clave_bur == row.clave_bur) 
                    & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],   
    
            lambda df, row: df[(df.genero == row.genero) & (df.epiteto == row.epiteto) 
                    & (df.clave_ecoregion_n2 == row.clave_ecoregion_n2) 
                    & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],  
    
            lambda df, row: df[(df.genero == row.genero) & (df.epiteto == row.epiteto)
                    & (df.clave_bur == row.clave_bur) 
                    & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],
    
            lambda df, row: df[(df.genero == row.genero) & (df.epiteto == row.epiteto) 
                    & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],

    
    
            lambda df, row: df[(df.genero == row.genero) & (df.epiteto.isnull()) 
                    & (df.clave_ecoregion_n2 == row.clave_ecoregion_n2) & (df.clave_bur == row.clave_bur) 
                    & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],
    
            lambda df, row: df[(df.genero == row.genero) & (df.epiteto.isnull()) 
                    & (df.clave_ecoregion_n2 == row.clave_ecoregion_n2) 
                    & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],
    
            lambda df, row: df[(df.genero == row.genero) & (df.epiteto.isnull())
                    & (df.clave_bur == row.clave_bur)
                    & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],
    
            lambda df, row: df[(df.genero == row.genero) & (df.epiteto.isnull()) 
                    & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],



    
    
            lambda df, row: df[(df.genero == row.genero) 
                    & (df.clave_ecoregion_n2 == row.clave_ecoregion_n2) & (df.clave_bur == row.clave_bur) 
                    & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],
    
            lambda df, row: df[(df.genero == row.genero)
                    & (df.clave_ecoregion_n2 == row.clave_ecoregion_n2)                 
                    & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],
    
            lambda df, row: df[(df.genero == row.genero)
                    & (df.clave_bur == row.clave_bur)
                    & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],
    
            lambda df, row: df[(df.genero == row.genero)
                    & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],

    

    
            lambda df, row: df[(df.clave_ecoregion_n2 == row.clave_ecoregion_n2)
                    & (df.clave_bur == row.clave_bur)
                    & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],
    
            lambda df, row: df[(df.clave_ecoregion_n2 == row.clave_ecoregion_n2)
                    & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],
    
            lambda df, row: df[(df.clave_bur == row.clave_bur)
                    & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],

    
            
            
            lambda df, row: df[(df.condicion == "Vivo")
                    & (df.tipo == "General")],
            lambda df, row: df[(df.condicion == "Muerto")
                    & (df.tipo == "General")]
            ]


carbono = [
    lambda df, row: df[(df.genero == row.genero) & (df.epiteto == row.epiteto) 
        & (df.clave_ecoregion_n2 == row.clave_ecoregion_n2) & (df.clave_bur == row.clave_bur) 
        & (df.diametro_min >= row.diametro) & (df.diametro_max >= row.diametro)],

    lambda df, row: df[(df.genero == row.genero) & (df.epiteto == row.epiteto) 
        & (df.clave_ecoregion_n2 == row.clave_ecoregion_n2) 
        & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],

    lambda df, row: df[(df.genero == row.genero) & (df.epiteto == row.epiteto) 
        & (df.clave_bur == row.clave_bur) 
        & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],

    lambda df, row: df[(df.genero == row.genero) & (df.epiteto == row.epiteto) 
        & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],

    lambda df, row: df[(df.genero == row.genero) & (df.epiteto.isnull()) 
        & (df.clave_ecoregion_n2 == row.clave_ecoregion_n2) & (df.clave_bur == row.clave_bur) 
        & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],

    lambda df, row: df[(df.genero == row.genero) & (df.epiteto.isnull()) 
        & (df.clave_ecoregion_n2 == row.clave_ecoregion_n2) 
        & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],

    lambda df, row: df[(df.genero == row.genero) & (df.epiteto.isnull()) 
        & (df.clave_bur == row.clave_bur) 
        & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],

    lambda df, row: df[(df.genero == row.genero) & (df.epiteto.isnull()) 
        & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],

    lambda df, row: df[(df.genero == row.genero) 
        & (df.clave_ecoregion_n2 == row.clave_ecoregion_n2) & (df.clave_bur == row.clave_bur) 
        & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],

    lambda df, row: df[(df.genero == row.genero)
        & (df.clave_ecoregion_n2 == row.clave_ecoregion_n2) 
        & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],

    lambda df, row: df[(df.genero == row.genero) 
        & (df.clave_bur == row.clave_bur) 
        & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],

    lambda df, row: df[(df.genero == row.genero) 
        & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],

    lambda df, row: df[(df.genero == row.genero) & (df.epiteto == row.epiteto) 
        & (df.diametro_min.isnull()) & (df.diametro_max.isnull())],

    lambda df, row: df[(df.genero == row.genero) & (df.epiteto.isnull()) 
        & (df.diametro_min.isnull()) & (df.diametro_max.isnull())],

    lambda df, row: df[(df.genero == row.genero)
        & (df.diametro_min.isnull()) & (df.diametro_max.isnull())],

    lambda df, row: df[(df.familia == row.familia) & (df.genero.isnull()) 
        & (df.epiteto.isnull())],

    lambda df, row: df[(df.clave_ecoregion_n2 == row.clave_ecoregion_n2) 
        & (df.clave_bur == row.clave_bur) 
        & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],

    lambda df, row: df[(df.clave_ecoregion_n2 == row.clave_ecoregion_n2) 
        & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],

    lambda df, row: df[(df.clave_bur == row.clave_bur) 
        & (df.diametro_min <= row.diametro) & (df.diametro_max >= row.diametro)],

    lambda df, row: df[(df.clave_ecoregion_n2 == row.clave_ecoregion_n2) 
        & (df.clave_bur == row.clave_bur) 
        & (df.diametro_min.isnull()) & (df.diametro_max.isnull())],

    lambda df, row: df[(df.clave_ecoregion_n2 == row.clave_ecoregion_n2) 
        & (df.diametro_min.isnull()) & (df.diametro_max.isnull())],

    lambda df, row: df[(df.clave_bur == row.clave_bur) 
        & (df.diametro_min.isnull()) & (df.diametro_max.isnull())],

    lambda df, row: df[(df.id == 998)]
]

densidad = [
    (lambda df,row: df[(df.genero == row.genero) & (df.epiteto == row.epiteto)]),
    (lambda df,row: df[(df.genero == row.genero) & (df.epiteto.isnull())]),
    (lambda df,row: df[(df.genero == row.genero)]),
    (lambda df,row: df[df.clave_ecoregion_n2 == row.clave_ecoregion_n2]) 
]