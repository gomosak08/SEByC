# New Start: Biomass and Carbon Calculation Project

**Author:** Kevin Saúl Gómez Molina  

If you have any questions or need further assistance with this project, feel free to reach out via any of the contact options above.

---

This project is designed to process data from multiple cycles to calculate biomass and carbon metrics. The process is outlined step-by-step below.

## Getting Started

### Step 1: Calculate Cycle Data

First, you need to run the `calculate.py` script, which requires accurate input data for each cycle. This script generates the initial processed data.

### Step 2: Data Normalization

Next, execute the `normalization.py` script. This step fills in any missing information and standardizes the data across cycles.

### Step 3: Model Assignment for Biomass and Carbon Calculations

Run the `asignation_tree.py` script, which assigns the appropriate models for calculating biomass, density, volume, and carbon based on the data. This step is essential for ensuring the correct equations are applied to your dataset.

### Step 4: Calculate Biomass and Carbon

Now, execute the `calculo_biomasa_carbono.py` script. This script calculates the biomass and carbon for each data entry. Be aware that some rows may have missing values for biomass and carbon after this step.

### Step 5: Handling Missing Data

To address missing values, open the `lab_missing_data.ipynb` Jupyter notebook. This notebook provides tools for identifying and correcting incomplete data, ensuring that your dataset is as comprehensive as possible.

### Automating the Process

If you prefer to run all the steps at once, you can execute the `calculate_all.py` script. This script automates the entire workflow, from data preparation to final calculations. Keep in mind that depending on your computer’s performance and the size of your dataset, this process may take some time.


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
