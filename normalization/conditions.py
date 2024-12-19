import numpy as np
from tqdm import tqdm
import re
import warnings
import math
warnings.filterwarnings("ignore")

def assign_equations(df, equations, vector=None, conditions=None):
    """
    Assigns equations based on specific conditions and fills in a result array.

    ### Parameters:
    - **df** (`pd.DataFrame`): The DataFrame containing the main dataset.
    - **modelos** (`pd.DataFrame`): The DataFrame containing the equation models for the specific resultado
    - **conditions** (`list of functions`): A list of functions that define the conditions to filter models. Each function should take in the `modelos` DataFrame and a row from `df` and return a filtered DataFrame. 
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
    else:
        raise ValueError(f'{conditions} is not known. The only available options are "biomasa", "carbono", "densidad".')

    # Filter the models to only include those with the desired variable result

    # Initialize an array to store the equations
    p_eq = vector
    criterio = np.empty(len(p_eq), dtype=object)

    # Iterate over each row in the main dataframe
    #for index, row in df.iterrows():
    for row in tqdm(df.itertuples(), total=len(df)):
        index = row.Index
        flag = False
        for i,condition in enumerate(conditions_eq):
            # Apply the condition to filter equations
            equation_df = condition(equations, row)
            if not equation_df.empty:
                if (equation_df['Funciones'] == 'alometrica').any():
                    #equation_df['Funciones'].isin(['alometrica']).idxmax() 
                    equation = equation_df.loc[equation_df['Funciones'].isin(['alometrica']).idxmax()]
                    p_eq[index] = equation.ecuacion_php  # The 6th column is selected here
                    flag = True
                    criterio[index] = i 
                    break
                equation = find_max_criteria_row(equation_df)
                # If a match is found, assign the equation and break
                p_eq[index] = equation.ecuacion_php  # The 6th column is selected here
                flag = True
                criterio[index] = i 
                break
        if not flag:
            # Print the index if no condition matched
            print(f"No match found for index: {index}")
            print(condition)
            break
    return p_eq,criterio



def assign_den(df, equations, vector=None):
    conditions_eq = densidad
    p_eq = vector
    criterio = np.empty(len(p_eq), dtype=object)
    for row in tqdm(df.itertuples(), total=len(df)):
        index = row.Index
        flag = False
        for i,condition in enumerate(conditions_eq):
            equation_df = condition(equations, row)
            if not equation_df.empty:
                equation = equation_df.iloc[0]
                p_eq[index] = equation.ecuacion_php  # The 6th column is selected here
                criterio[index] = i 
                flag = True
                break
        if not flag:
            # Print the index if no condition matched
            print(f"No match found for index: {index}")
            p_eq[index] = "0.5"
    return p_eq, criterio



def find_max_criteria_row(df):
    """
    Finds the row in the DataFrame `df` that satisfies the maximum or minimum criteria for 
    several specific columns. It checks for the following criteria in order:
    
    1. The minimum difference between 'diametro_max' and 'diametro_min'.
    2. The maximum value in the 'r2' column.
    3. The maximum value in the 'numero_arboles' column.
    4. The maximum number of unique variables in the 'ecuacion' column.
    
    The function returns the first row that satisfies any of these criteria.

    Parameters:
    ----------
    df : pandas.DataFrame
        The DataFrame containing the columns 'diametro_max', 'diametro_min', 'r2', 'numero_arboles', 
        and 'ecuacion'.

    Returns:
    -------
    pandas.Series or str
        The row from the DataFrame that meets the first of the specified criteria.
        If no criteria are met, it returns a message indicating no matches.
    """

    def count_variables(expression):
        """
        Counts the number of unique variables in a mathematical expression.

        Parameters:
        ----------
        expression : str
            The mathematical expression as a string.

        Returns:
        -------
        int
            The number of unique variables in the expression.
        """
        potential_vars = re.findall(r'\b[a-zA-Z_]\w*\b', expression)
        functions_and_constants = {'Exp', 'LN'}
        variables = [var for var in potential_vars if var not in functions_and_constants]
        unique_variables = set(variables)
        return len(unique_variables)

    # Calculate variable counts for each row in the 'ecuacion' column
    variable_counts = df['ecuacion'].apply(count_variables)

    # Find indices for the specified criteria
    indices = [
        (df['diametro_max'] - df['diametro_min']).idxmin(),  # Minimum range
        df['r2'].idxmax(),                                   # Maximum r2
        df['numero_arboles'].idxmax(),                       # Maximum number of trees
        variable_counts.idxmax()                             # Maximum variables
    ]
    # Iterate over indices and return the first valid row
    for index in indices:
        if not np.isnan(index):
            return df.loc[index]

    # If no valid index is found, return a message
    return "This does not have eq that match the conditions"

def volumen(df_muerto, df_tocon, modelos, lon):
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
    v_eq = np.empty(lon, dtype=object)
    # Process the df_muerto dataframe
    for index, row in df_muerto.iterrows():
        v_eq[index] = modelos.iloc[2883, 6]

    # Process the df_tocon dataframe
    for index, row in df_tocon.iterrows():
        if not np.isnan(row.grado_putrefaccion):
            eq = modelos.iloc[2884, 6]
            eq += f"/{row.grado_putrefaccion}"
            #print(eq, index)
            v_eq[index] = eq
        else:
            #print(index)
            v_eq[index] = modelos.iloc[2884, 6]

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


biomasa_descriptions = {
    0: "genero,epiteto,clave_ecoregion,clave_bur,rango_diametro",
    1: "genero,epiteto,clave_ecoregion,rango_diametro",
    2: "genero,epiteto,clave_bur,rango_diametro",
    3: "genero,epiteto,rango_diametro",
    4: "genero,epiteto_nulo,clave_ecoregion,clave_bur,rango_diametro",
    5: "genero,epiteto_nulo,clave_ecoregion,rango_diametro",
    6: "genero,epiteto_nulo,clave_bur,rango_diametro",
    7: "genero,epiteto_nulo,rango_diametro",
    8: "genero,clave_ecoregion,clave_bur,rango_diametro",
    9: "genero,clave_ecoregion,rango_diametro",
    10: "genero,clave_bur,rango_diametro",
    11: "genero,rango_diametro",
    12: "clave_ecoregion,clave_bur,rango_diametro",
    13: "clave_ecoregion,rango_diametro",
    14: "clave_bur,rango_diametro",
    15: "condicion_vivo,tipo_general",
    16: "condicion_muerto,tipo_general"
}

carbono_descriptions = {
    0: "genero,epiteto,clave_ecoregion,clave_bur,diametro_min_mayor_igual,diametro_max_mayor_igual",
    1: "genero,epiteto,clave_ecoregion,rango_diametro",
    2: "genero,epiteto,clave_bur,rango_diametro",
    3: "genero,epiteto,rango_diametro",
    4: "genero,epiteto_nulo,clave_ecoregion,clave_bur,rango_diametro",
    5: "genero,epiteto_nulo,clave_ecoregion,rango_diametro",
    6: "genero,epiteto_nulo,clave_bur,rango_diametro",
    7: "genero,epiteto_nulo,rango_diametro",
    8: "genero,clave_ecoregion,clave_bur,rango_diametro",
    9: "genero,clave_ecoregion,rango_diametro",
    10: "genero,clave_bur,rango_diametro",
    11: "genero,rango_diametro",
    12: "genero,epiteto,diametro_min_nulo,diametro_max_nulo",
    13: "genero,epiteto_nulo,diametro_min_nulo,diametro_max_nulo",
    14: "genero,diametro_min_nulo,diametro_max_nulo",
    15: "familia,genero_nulo,epiteto_nulo",
    16: "clave_ecoregion,clave_bur,rango_diametro",
    17: "clave_ecoregion,rango_diametro",
    18: "clave_bur,rango_diametro",
    19: "clave_ecoregion,clave_bur,diametro_min_nulo,diametro_max_nulo",
    20: "clave_ecoregion,diametro_min_nulo,diametro_max_nulo",
    21: "clave_bur,diametro_min_nulo,diametro_max_nulo",
    22: "id_998"
}

densidad_descriptions = {
    0: "genero,epiteto",
    1: "genero,epiteto_nulo",
    2: "genero",
    3: "clave_ecoregion"
}
