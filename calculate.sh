#!/bin/bash

# Get the current working directory and store it in a variable
original_path=$1
cicle=$2
echo "this is the cicle $cicle"
global_path=$(pwd)
echo "$global_path/env/bin/activate"

# Activate the Python virtual environment
source "$global_path/env/bin/activate"

last_run=$(ls -d runs/run_* 2>/dev/null | grep -o '[0-9]*' | sort -n | tail -1)

# If there are no previous runs, set the run number to 1, else increment it
if [ -z "$last_run" ]; then
    next_run=1
else
    next_run=$((last_run + 1))
fi


# Ensure the directory gets created
mkdir -p runs/run_${next_run}_cicle_${cicle}/
# Run the Python script with the correct path
set -e


echo "Linear regression start to calculate the missing data herre $original_path "
if ! python3 linear_regression/linear_regresion.py --file_path "$original_path" \
 --output_file "runs/run_${next_run}_cicle_${cicle}/regression_${next_run}_head.csv"; then
    echo "Error: Linear regression failed to calculate the missing data" >&2
    exit 1
fi
echo "Missing data calculated"

echo "Start to assign the equations to the dataframe runs/run_${next_run}_cicle_${cicle}/regression_${next_run}_head.csv"

len_df=$(wc -l < "$original_path")
len_df=$((len_df - 1))


echo $len_df

if ! python3 normalization/asignation.py --modelo_path csvs/modelo2.csv \
 --origina_path runs/run_${next_run}_cicle_${cicle}/regression_${next_run}_head.csv \
 --output_file runs/run_${next_run}_cicle_${cicle}/normalizaded_${next_run}_head.csv --len_df $len_df; then
    echo "Error: Equation assignment failed" >&2
    exit 1
fi
echo "The assignation was correctly done"

echo "Start to calculate biomass and carbon"
if ! python3 calculo_biomasa_carbono/calculus_biomass_carbon.py --origina_path runs/run_${next_run}_cicle_${cicle}/normalizaded_${next_run}_head.csv \
    --output_file runs/run_${next_run}_cicle_${cicle}/calculo_bio_car_${next_run}_head.csv; then
    echo "Error: Biomass and carbon calculation failed" >&2
    exit 1
fi
echo "The calculus was correctly done"

echo "Start to making post procesing"
if ! python3 post_procces/post_porecces.py --original_path "$original_path" --bc_csv runs/run_${next_run}_cicle_${cicle}/calculo_bio_car_${next_run}_head.csv \
    --output_file runs/run_${next_run}_cicle_${cicle}/result_final_${next_run}.csv --cicle ${cicle}; then
    echo "Error: post procesing failed" >&2
    exit 1
fi

mkdir runs/run_${next_run}_cicle_${cicle}/stadistics/
echo "Start to calculate biomass and carbon by sitio and conglomerado"
if ! python3 conglomerado_sitio/estadisticas.py --origina_path runs/run_${next_run}_cicle_${cicle}/result_final_${next_run}.csv \
    --output_dir runs/run_${next_run}_cicle_${cicle}/stadistics/ --cicle ${cicle}; then
    echo "Error: Biomass and carbon calculation failed" >&2
    exit 1
fi
echo "The calculus was correctly done"

echo "All was correctly done!!"

