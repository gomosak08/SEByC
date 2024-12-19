import pandas as pd
import argparse


def calcular_biomasa_carbono(resultado):
    """
    Calcula métricas de biomasa y carbono a nivel de conglomerado y sitio, a partir de los datos proporcionados.

    Args:
        resultado (DataFrame): DataFrame con información de conglomerados, sitios, y métricas de biomasa y carbono.
            Debe incluir las columnas: conglomerado, sitio, biomasa, carbono, latitud, longitud, anio_levantamiento, estado.

    Returns:
        tuple: Contiene dos listas de diccionarios:
            - data_list: Métricas calculadas a nivel de conglomerado.
            - sitio_list: Métricas calculadas a nivel de sitio.
    """
    data_list = []
    sitio_list = []

    # Iterar sobre cada conglomerado único
    for conglomerado_id in resultado['conglomerado'].unique():
        conglomerado_data = resultado[resultado['conglomerado'] == conglomerado_id]
        sitios = conglomerado_data['sitio'].nunique()

        # Procesar cada sitio dentro del conglomerado
        for sitio_id in conglomerado_data['sitio'].unique():
            sitio_data = conglomerado_data[conglomerado_data['sitio'] == sitio_id]
            
            # Calcular métricas a nivel de sitio
            biomasa = sitio_data['biomasa_kg'].sum() 
            carbono = sitio_data['carbono_kg'].sum() 
            numero_arboles = len(sitio_data)
            sitio_referencia = sitio_data.iloc[0]
            area_basal = sitio_data["area_basal_m2"].sum()

            # Crear diccionario para el sitio
            sitio_dict = {
                'anio_levantamiento': sitio_referencia['anio_levantamiento'],
                'conglomerado': sitio_referencia['conglomerado'],
                'sitio': sitio_id,
                'latitud': sitio_referencia['latitud'],
                'longitud': sitio_referencia['longitud'],
                'clave_ecoregion_n2': sitio_referencia["clave_ecoregion_n2"],
                'clave_bur': sitio_referencia["clave_bur"],
                'referencia_1': sitio_referencia["referencia_1"],
                'referencia_2': sitio_referencia["referencia_2"],
                'user_id': sitio_referencia["user_id"],
                'created_at': sitio_referencia["created_at"],
                'updated_at': sitio_referencia["updated_at"],
                'clave_ecoregion_n1': sitio_referencia["clave_ecoregion_n1"],
                'clave_ecoregion_n3': sitio_referencia["clave_ecoregion_n3"],
                'clave_ecoregion_n4': sitio_referencia["clave_ecoregion_n4"],
                'estado_inegi': sitio_referencia["estado_inegi"],
                'estado': sitio_referencia['estado'],
                'numero_arboles_sitio': numero_arboles,
                'area_basal_sitio_m2': area_basal, 
                'biomasa_sitio_kg': biomasa,
                'carbono_sitio_kg': carbono              
            }
            sitio_list.append(sitio_dict)

        # Calcular métricas a nivel de conglomerado
        biomasa_conglomerado = conglomerado_data['biomasa_kg'].sum() / 1000
        carbono_conglomerado = conglomerado_data['carbono_kg'].sum() / 1000
        numero_arboles_conglomerado = len(conglomerado_data)
        conglomerado_referencia = conglomerado_data.iloc[0]
        area = sitios * 0.04  # Supone que cada sitio equivale a 0.04 hectáreas
        area_basal = conglomerado_data["area_basal_m2"].sum()
        # Crear diccionario para el conglomerado
        conglomerado_dict = {
            'anio_levantamiento': conglomerado_referencia['anio_levantamiento'],
            'conglomerado': conglomerado_referencia['conglomerado'],
            'sitios': sitios,
            'sito_referencia_xy': conglomerado_referencia['sitio'],
            'latitud': conglomerado_referencia['latitud'],
            'longitud': conglomerado_referencia['longitud'],
            'clave_ecoregion_n2': sitio_referencia["clave_ecoregion_n2"],
            'clave_bur': conglomerado_referencia["clave_bur"],
            'referencia_1': conglomerado_referencia["referencia_1"],
            'referencia_2': conglomerado_referencia["referencia_2"],
            'user_id': conglomerado_referencia["user_id"],
            'created_at': conglomerado_referencia["created_at"],
            'updated_at': conglomerado_referencia["updated_at"],
            'clave_ecoregion_n1': conglomerado_referencia["clave_ecoregion_n1"],
            'clave_ecoregion_n3': conglomerado_referencia["clave_ecoregion_n3"],
            'clave_ecoregion_n4': conglomerado_referencia["clave_ecoregion_n4"],
            'estado_inegi': conglomerado_referencia["estado_inegi"],
            'estado': conglomerado_referencia['estado'],
            'area': area,
            'numero_arboles_conglomerado': numero_arboles_conglomerado,
            'area_basal_conglomerado_m2':area_basal,
            'biomasa_conglomerado_Mg': biomasa_conglomerado,
            'carbono_conglomerado_Mg': carbono_conglomerado,
            'carbono_hectarea_Mg': carbono_conglomerado / area,
            'biomasa_hectarea_Mg': biomasa_conglomerado / area,

        }
        data_list.append(conglomerado_dict)

    return data_list, sitio_list

def main(args):
    resultado = pd.read_csv(args.original_path, low_memory=False)
    data_list, sitio_list = calcular_biomasa_carbono(resultado)
    df_c = pd.DataFrame(data_list) 
    df_s = pd.DataFrame(sitio_list)


    df_c.to_csv(args.output_dir+f"/conglomerado_ciclo_{args.cicle}.csv")
    df_s.to_csv(args.output_dir+f"/sitio_ciclo_{args.cicle}.csv")
    print(f'Conglomerado stadistics were saved in {args.output_dir+f"/conglomerado_ciclo_{args.cicle}.csv"}')
    print(f'Sitio stadistics were saved in {args.output_dir+f"/sitio_ciclo_{args.cicle}.csv"}')


if __name__ == "__main__":
    # Argument parser setup for command-line usage
    parser = argparse.ArgumentParser(description="Process tree data for regression.")

    parser.add_argument('--original_path', type=str, help="Path to the CSV file containing the regression data.")
    parser.add_argument('--output_dir', type=str, help="The path where bouth csvs will be saved")
    parser.add_argument('--cicle', type=int, help="The numer of the cicle")

    args = parser.parse_args()
    main(args)