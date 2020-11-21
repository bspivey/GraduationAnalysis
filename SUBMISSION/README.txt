### ------------------------------------------------------------------------------------- ###
  README for CSE 6242 Fall 2020
### ------------------------------------------------------------------------------------- ###

### ------------------------------------------------------------------------------------- ###
  DESCRIPTION
### ------------------------------------------------------------------------------------- ###

This package includes the code required to generate plots shown in this analysis of Socioeconomic Status factors. The code performs data cleansing and table merging and pivoting prior to any analysis. The analysis involves calculating variable cross-correlations and building models which are also used to investigate correlation with graduation rate via feature importances.
It also includes the data visulizations. The choropleth, scatter chart, and donut charts are all d3. Bootstrap is used for the layout and styling of the site.
### ------------------------------------------------------------------------------------- ###
  INSTALLATION
### ------------------------------------------------------------------------------------- ###

1. Get Python packages
Environment for this project is tracked through conda and environment.yml file.
Install the environment with this command `conda env update --file environment.yml`
Update any packages in the environment with this command `conda env export > environment.yml`

Confirm that the following packages are installed: pandas, numpy, matplotlib, plotly, and subprocess. Note that Python Standard Library packages sys and io are also required.

2. Download the CODE folder onto the user's machine.
3. Follow instructions in EXECUTION to download data and run scripts.

### ------------------------------------------------------------------------------------- ###
  EXECUTION
### ------------------------------------------------------------------------------------- ###


## --------------------------------------------------------------------------------------- ##
  NYSED DATASET ANALYSIS

1. Create a folder called NysedAnalysis.
2. Download the data from the following link: https://data.nysed.gov/downloads.php. Users must download Report Card Databases and Graduation Rate Databases for the school years ending in years 2015-2019 as MDB files. Note that MDB files can be on the order of 100 MB.
3. Copy the MDB files into the **NysedAnalysis** folder.
4. Copy PY files in the CODE/NYSED folder into the **NysedAnalysis** folder.
5. Open the NysedAnalysis folder.
6. Run main_nysed_analysis.py file which runs five scripts below.

# ----------------------------------------------------------------------------------------- #
  main_nysed_analysis.py
# ----------------------------------------------------------------------------------------- #

Output:
Runs all scripts required to generate analysis and plots for the NYSED dataset.

# ----------------------------------------------------------------------------------------- #
  run_statistics.py
# ----------------------------------------------------------------------------------------- #

Output:
- Calculates Rank Spearman Correlation coefficient
- Fits Random Forest Regressors
- Calculates Impurity and Permutation Feature Importances over all data
- Calculates Impurity and Permutation Feature Importances for Economically Disadvantaged
- Plots Histograms and perform Mann Whitney U Test
	- All Data split on Economically Disadvantaged T/F
	- Economically Disadvantaged T split on Charter School T/F
	- Minority T split on Charter School T/F

Data Input:
- df_grad_rate_pct_school_merge.csv
	- Description: wide table containing SES factors and confounding factors as columns and each school as a row.
	- Source: make_wide_all_features_school.py

# ----------------------------------------------------------------------------------------- #
  make_wide_all_features_school.py
# ----------------------------------------------------------------------------------------- #

Output:
- Creates the wide table containing SES factors and confounding factors as columns and each school as a row.
- Output table file: df_grad_rate_pct_school_merge

Data Input:
- df_combined_all.pkl
	- Description: tall table containing all schools and school years with subgroup counts as the column and each school/year/subgroup as a row.
	- Source: merge_pkl_tables.py
- df_grad_rate_pct_school.csv
	-Description: wide table containing SES factors as columns and each school as a row.
	- Source: make_wide_dataframe_school.py

# ----------------------------------------------------------------------------------------- #
  make_wide_dataframe_school.py
# ----------------------------------------------------------------------------------------- #

Output:
- Creates the wide table containing SES factors as columns and each school as a row.
- Output table file: df_grad_rate_pct_school.csv

Data Input:
- df_grad_rate_15.pkl
- df_grad_rate_16.pkl
- df_grad_rate_17.pkl
- df_grad_rate_18.pkl
- df_grad_rate_19.pkl


# ----------------------------------------------------------------------------------------- #
  merge_pkl_tables.py
# ----------------------------------------------------------------------------------------- #

Output:
- Merges the Graduation Rate and Staff Qualification tables across five years. Output table is still a tall table.
- Output table file: df_combined_all.pkl

Data Input:
- df_grad_rate_15.pkl
- df_grad_rate_16.pkl
- df_grad_rate_17.pkl
- df_grad_rate_18.pkl
- df_grad_rate_19.pkl
- df_staff_qualifications_15.pkl
- df_staff_qualifications_16.pkl
- df_staff_qualifications_17.pkl
- df_staff_qualifications_18_19.pkl
- df_staff_qualifications_19_20.pkl

# ----------------------------------------------------------------------------------------- #
  mdb_pandas_api.py
# ----------------------------------------------------------------------------------------- #

Output:
- Generates the files containing raw DataFrames from the data downloaded from the following link: https://data.nysed.gov/downloads.php. Users must download Report Card Databases and Graduation Rate Databases for the school years ending in years 2015-2019.

- Output table files:
	- df_grad_rate_15.pkl
	- df_grad_rate_16.pkl
	- df_grad_rate_17.pkl
	- df_grad_rate_18.pkl
	- df_grad_rate_19.pkl
	- df_staff_qualifications_15.pkl
	- df_staff_qualifications_16.pkl
	- df_staff_qualifications_17.pkl
	- df_staff_qualifications_18_19.pkl
	- df_staff_qualifications_19_20.pkl

Data Input:
Downloaded MDB files.

  END: NYSED DATASET ANALYSIS
## --------------------------------------------------------------------------------------- ##

## --------------------------------------------------------------------------------------- ##
  DATA VISUALIZATION 
1. Open cmd/bash
2. cd into the d3-bootstrap-viz dir
3. Run the following command, python run -m http.server
4. Open web browser and go to localhost:8000
5. Click on a county to view demographic breakdown and analysis
## --------------------------------------------------------------------------------------- ##
