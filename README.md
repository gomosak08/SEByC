# Biomass and Carbon Calculation Project

**Author:** Kevin Saúl Gómez Molina  
**Email:** [gomosak@outlook.es](mailto:gomosak@outlook.es)  

If you have any questions or need further assistance with this project, feel free to reach out via any of the contact options above.

---

## **Indice (Table of Contents)**

1. [Introduction](#introduction)  
2. [Project Overview](#project-overview)  
3. [Setting Up the Environment](#setting-up-the-environment)  
   - [Installing Requirements](#installing-requirements)  
4. [Step-by-Step Workflow](#step-by-step-workflow)  
   - [Step 1: Calculate Cycle Data](#step-1-calculate-cycle-data)  
   - [Step 2: Data Normalization](#step-2-data-normalization)  
   - [Step 3: Model Assignment for Biomass and Carbon Calculations](#step-3-model-assignment-for-biomass-and-carbon-calculations)  
   - [Step 4: Calculate Biomass and Carbon](#step-4-calculate-biomass-and-carbon)  
   - [Step 5: Handling Missing Data](#step-5-handling-missing-data)  
5. [Automating the Process](#automating-the-process)  
6. [Project File Structure](#project-file-structure)  

---

## **Introduction**

This project is designed to process data from multiple cycles to calculate biomass and carbon metrics, enabling accurate and efficient data analysis for environmental studies and applications.

---

## **Project Overview**

The workflow involves multiple scripts and tools to handle the data, normalize it, assign models for calculation, compute the required metrics, and handle missing data. For seamless processing, all steps can be automated using a single script.

---

## **Setting Up the Environment**

### Installing Requirements

To set up your environment, ensure you have Python installed on your system. Then, follow these steps:

1. Clone the project repository to your local machine:
   ```bash
   git clone git@github.com:gomosak08/SEByC.git
   cd SEByC
2. Create a virtual environment
    ```bash
    python3 -m venv env
    source env/bin/activate  
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
4. Verify the installation:
    ```bash
    python --version
    pip freeze
You are now ready to begin working on the project.

For a **T3.xlarge** instance on AWS, you can run the `setup.sh` script after cloning the repository. This script creates a virtual environment and installs all the necessary dependencies.


## **Step-by-Step Workflow**

### **Step 1: Calculate Cycle Data**

First, run the `linear_regresion.py` script. This script tandardize the data and fill in any missing information..
```bash
python linear_regresion.py --file_path <input_file_path> --output_file <output_file_path>
```

### **Step 2: Model Assignation**

Execute the `asignation.py` script to  assign models for calculating biomass, density, volume, and carbon. s

```bash
python asignation.py ---model_path <model_file_path> --original_path <original_data_path> --output_file <output_file_path> --len_df <dataframe_length>
```

### **Step 3: Model Calculus for Biomass and Carbon Calculations**

Run the `asignation_tree.py` script to assign models for calculating biomass, density, volume, and carbon.

```bash
python asignation_tree.py --origina_path --output_file
```

### **Step 4: Calculate Biomass and Carbon**

Run the `calculo_biomasa_carbono.py` script to calculate biomass and carbon for your dataset.

```bash
python calculo_biomasa_carbono.py --original_path <original_data_path> --output_file <output_file_path>
```

### **Spliting csv**
#### **How to Use**
Run the Script `split_csv.py` Use the command line to run the script and pass the required arguments:
```bash
python script_name.py "../csvs/arboles.csv" "arboles_1000_head.csv" 2015 2020
```
**Arguments:**

- input_path: Path to the input CSV file (e.g., "../csvs/arboles.csv").
- output_path: Path to save the filtered CSV file (e.g., "arboles_1000_head.csv").
- start_year: Start of the year range for filtering (e.g., 2015).
- end_year: End of the year range for filtering (e.g., 2020).

**Output:**

The filtered CSV file will be saved at the path specified by output_path.
### Automating the Process

If you prefer to run all the steps at once, you can execute the ```calculate.sh``` script. This script automates the entire workflow, from data preparation to final calculations. Keep in mind that the process may take some time, depending on your computer’s performance and the size of your dataset.

To use the ```calculate.sh``` script, provide the CSV path containing the data you want to use for biomass and carbon calculations.Make sure you are in the virtual environment where you installed the `requirements.txt` dependencies.


├── csvs        
│   └── modelos2.csv       
├── calculate.sh    
├── calculo_biomasa_carbono   
│   ├── bio_car.py  
│   └── funtions.py  
├── linear_regression   
│   ├── calculate.py   
│   ├── README.md   
│   └── regresion.py  
├── normalization   
│   ├── asignation.py   
│   └── conditions.py   
└── runs
