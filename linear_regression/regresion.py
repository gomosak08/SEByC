import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression # type: ignore
from tqdm import tqdm
import joblib


def regression(df_species :pd.DataFrame, X_train:list[str],
 y_train: str ):
    """
    Calculate the regression over a column, or columns 

    The function takes the columns in a dataframe, and builds
    a linear-regression model, so it calculates the missing 
    data in the Y column 

    Parameters
    ----------
    df:_species: is a dataframe that contains just a type of specie
    X_train: A list of the X columns
    Y_train: string of the name of Y column

    Returns
    -------
    tuple
        A tuple, first value is a list with all the y_predicted and 
        the second is np.array to put correctly y_array in the dataframe

    Raises
    ------
    ValueError
        If the list is empty.
    """

    if not df_species[y_train].isnull().any():
        raise ValueError(f"The column {y_train} must have at least" 
        f"one missing value.")
    if df_species[y_train].isnull().all():
        raise ValueError(f"LinearRegresion need at least one"
         f"value at {y_train} are all null values ")    

    train_df_ = df_species[(df_species[y_train].notnull())]
    train_df = train_df_[( train_df_[X_train[0]].notnull())]
    X_train_df = train_df[X_train]
    y_train_df = train_df[[y_train]]  
    
    model = LinearRegression()
    model.fit(X_train_df, y_train_df)   

    predict_df = df_species[df_species[y_train].isnull()]
    X_predict = predict_df[X_train]
    y_predict = model.predict(X_predict)
 

    return y_predict, np.ones((len(y_predict),1))



def regression_speices(df: pd.DataFrame, condicion:str = 'Vivo'):
    """
    Calculate the missing data in "altura" and "diametro"

    This function take a dataframe where "altura" and "diametro" 
    does not have missing values in the same row, and create a model 
    to calculate the missing data through LinearRegresion
    
    Parameters
    ------------
    df: The dataframe where are the data
    
    Returns
    ------------
    df: pd.Dataframe
        Have the same data as the original, but the missing data have 
        been calculated 
    condition: str
        The condition of each tree this are the options 
        ['Vivo', 'Muerto', 'Tocón']
    condicion
    Raises
    ------------
    ValueError
        if some dimensionally error or empty column 
    
    """
    allowed_conditions = ['Vivo', 'Muerto']

    if condicion not in allowed_conditions:
        raise NameError(f"Unknown condition '{condicion}'"
        f"Allowed conditions are {allowed_conditions}.")

    
    species = df.familia.value_counts().index
    
    for i in tqdm((species),  total=len(species)):
        #i = 'Oleaceae'
        #print(i)
        #print(df.loc[75817])

        df_species = df[(df.familia ==  i) & (df.condicion ==  condicion)]
        altura_null = df_species.altura.isnull().any()
        diametro_null = df_species.diametro.isnull().any()
        try:
            if altura_null:
                y_predict, is_predicted = regression(df_species,['diametro'],
                                                                    'altura')                
                df.loc[(df.familia ==  i) & (df.altura.isnull()) & 
                    (df.condicion == condicion), 
                    ['altura','is_predicted']] = np.concatenate((y_predict,
                    is_predicted), axis=1)

                
            if diametro_null:
                y_predict, is_predicted = regression(df_species,['altura'],
                'diametro')
                is_predicted *= 2
                df.loc[(df.familia ==  i) & (df.diametro.isnull()) & 
                (df.condicion == condicion), ['diametro', 'is_predicted']
                ] = np.concatenate((y_predict, is_predicted), axis=1)
            #print(df.loc[75817])

        except ValueError as e:
            if not (df_species['diametro'].isnull().any() and df_species['diametro'].isnull().all()) or not (df_species['altura'].isnull().any() and df_species['altura'].isnull().all()):
                continue
            else:
                print(f"\nValueError processing species: {i}, error: {e}")
        
    return df

def regression_all(df: pd.DataFrame, condicion:str = 'Vivo'):
    allowed_conditions = ['Vivo', 'Muerto']

    if condicion not in allowed_conditions:
        raise NameError(f"Unknown condition '{condicion}'"
        f"Allowed conditions are {allowed_conditions}.")

    altura_null = df.altura.isnull().any()
    diametro_null = df.diametro.isnull().any()

    if altura_null:

        validation_df = df[["diametro"]][(df["altura"].isnull()) & (df["condicion"] == condicion)]

        #print(type(validation_df),validation_df.columns)
        loaded_model = joblib.load('linear_regression/linear_regression_diametro.pkl')

        y_predict = loaded_model.predict(validation_df)
        is_predicted = np.ones((len(y_predict),1))
        print("This is the len of y_predict h",len(y_predict))




        #print(df.loc[index[0]])
        df.loc[(df.altura.isnull()) & 
            (df.condicion == condicion), 
            ['altura','is_predicted']] = np.concatenate((y_predict,
            is_predicted), axis=1)
        #print(df.loc[index[0]])


    if diametro_null:

        #validation_df = df["altura"][(df["altura"].notnull())]
        validation_df = df[["altura"]][(df["diametro"].isnull()) & (df["condicion"] == condicion)]


        loaded_model = joblib.load('linear_regression/linear_regression_altura.pkl')
        

        y_predict = loaded_model.predict(validation_df)
        is_predicted = np.ones((len(y_predict),1))
        is_predicted *= 2
        print("This is the len of y_predict",len(y_predict))
        print("This is the first value of y_predict ", y_predict[0])
        



        df.loc[(df.diametro.isnull()) & 
            (df.condicion == condicion), 
            ['diametro','is_predicted']] = np.concatenate((y_predict,
            is_predicted), axis=1)
    
        #print(df.loc[index[0]])

    
    return df