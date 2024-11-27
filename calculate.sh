#!/bin/bash

# Get the current working directory and store it in a variable
original_path=$1

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
mkdir -p runs/run_$next_run/
# Run the Python script with the correct path
set -e


echo "Linear regression start to calculate the missing data herre $global_path/$original_path "
if ! python3 linear_regression/linear_regresion.py --file_path "$global_path/$original_path" \
 --output_file "runs/run_${next_run}/regression_${next_run}_head.csv"; then
    echo "Error: Linear regression failed to calculate the missing data" >&2
    exit 1
fi
echo "Missing data calculated"

echo "Start to assign the equations to the dataframe runs/run_${next_run}/regression_${next_run}_head.csv"

len_df=$(wc -l < "$global_path/$original_path")
len_df=$((len_df - 1))


echo $len_df

if ! python3 normalization/asignation.py --modelo_path csvs/modelo2.csv \
 --origina_path runs/run_${next_run}/regression_${next_run}_head.csv \
 --output_file runs/run_${next_run}/normalizaded_${next_run}_head.csv --len_df $len_df; then
    echo "Error: Equation assignment failed" >&2
    exit 1
fi
echo "The assignation was correctly done"

echo "Start to calculate biomass and carbon"
if ! python3 calculo_biomasa_carbono/bio_car.py --origina_path runs/run_${next_run}/normalizaded_${next_run}_head.csv \
--output_file runs/run_${next_run}/calculo_bio_car_${next_run}_head.csv; then
    echo "Error: Biomass and carbon calculation failed" >&2
    exit 1
fi
echo "All was correctly executed"
