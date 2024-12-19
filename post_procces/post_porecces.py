import pandas as pd
import argparse
def main(args):
    """
    Main function to process tree data for regression analysis.

    This function reads input data from CSV files, applies various data processing steps,
    fills missing values, and assigns equations for biomass, carbon, density, and volume 
    based on predefined models. Finally, it outputs the processed data to a CSV file.

    Args:
        args: Command line arguments containing paths to input CSV files and output directory.
    """
    orden = ["id","ciclo","anio_levantamiento","conglomerado","sitio","condicion","numero_arbol","numero_tallo",
            "tallos","grado_putrefaccion","especie_id","familia","genero","epiteto","categoria_infra",
            "infraespecie","latitud","longitud","clave_ecoregion_n2","clave_bur","referencia_1","referencia_2",
            "user_id","created_at","updated_at","clave_ecoregion_n1","clave_ecoregion_n3","clave_ecoregion_n4","estado_inegi","estado",
            "edad","diametro","altura","is_predicted",
            "criterio_den","criterios_densidad","criterio_biomasa","criterios_biomasa","criterio_carbon",
            "criterios_carbono","densidad_eq","volumen_eq","biomasa_eq","carbon_eq","area_basal_m2","volumen",
            "biomasa","carbono"]
    df_original = pd.read_csv(args.original_path, low_memory=False)
    df_bc = pd.read_csv(args.bc_csv, low_memory=False)
    print("All the files were opened correctly")
     

    df_bc.insert(loc=1, column="ciclo", value=args.cicle)
    df_bc = df_bc[orden]
    df_bc.insert(loc=31, column="diametro_original_cm", value=df_original["diametro"].values)
    df_bc.insert(loc=32, column="altura_original_m", value=df_original["altura"].values)
    df_bc = df_bc.rename(columns={"altura": "altura_estandarizado_m", "diametro": "diametro_estandarizado_cm", "biomasa":"biomasa_kg","carbono":"carbono_kg","volumen":"volumen_m3"})


    df_bc.to_csv(args.output_file, index=False)
    print(f"The dataframe was saved in {args.output_file}")
if __name__ == "__main__":
    # Argument parser setup for command-line usage
    parser = argparse.ArgumentParser(description="Process tree data for regression.")

    parser.add_argument('--original_path', type=str, help="Path to the CSV file containing the regression data.")
    parser.add_argument('--bc_csv', type=str, help="Path to the CSV file containing the biomass and carbon calculus.")


    parser.add_argument('--cicle', type=int, help="The numer of the cicle")
    parser.add_argument('--output_file', type=str, help="The path where the output will be saved")

    args = parser.parse_args()
    main(args)
    #/home/gomosak/conafor/SEByc/labs/top_1000_resultado.csv



