###############
# DESCRIPTION #
###############
There are 3 folders in the CODE folder.  

1. CORNELL
2. NYSED
3. d3-bootstrap-viz

The CORNELL folder has 2 folders in it:
	1. data folder - The 'data' folder includes both the source (input) and the results (output) files needed to recreate the analyses.  Here are those descriptions:
		* source: apm_all.csv
		* source: 36_County_Coverage_A.txt - county to district mapping information
		* source: BasicInfo2.csv - District information
		* source: apm_all.csv - cohort and year information.
		* source: FARU_all.csv - financial information to district - we join this to graduation data.
		* source: graduation_all.csv - graduation rates and basic cohort information  
		---
		* results: cornell_data_dictionary.txt - data dictionary for the final output
		* results: PCA_plus_preds.csv - the dimensionality reduction raw information and raw prediction information by county
		* results: county_agg_results.csv - Linear model summary statistics (Explained Variance, MSE, R^2, Coefs and Intercept) data
		* results: regressionR2.csv - summary statistics for the random forest regression model (in R)
	2. notebooks folder - this contains the R markdown file and python notebook files required to recreate the analysis.
		- data_clean_final.ipynb - this jupyter notebook merges all the input data and imputes missing values, after cleaning.  It is used for both the cornell_rf_model.Rmd and the cornell_pca_lass_model.ipynb.
		- cornell_rf_model.Rmd - R markdown file (annotated inline) that contains the random forest feature selection.
		- cornell_pca_lasso_model.ipynb - the jupyter notebook contains all the code (annotated inline) required to reproduce the analysis.

The NYSED folder has 6 py files in it:
	1. main_nysed_analysis.py 
		- Runs all scripts required to generate analysis and plots for the NYSED dataset.
	2. make_wide_all_features_school.py 
		- Creates the wide table containing SES factors and confounding factors as columns and each school as a row.
	3. make_wide_dataframe_school.py 
		- Creates the wide table containing SES factors as columns and each school as a row.
	4. mdb_pandas_api.py
		- Generates the files containing raw DataFrames from the data downloaded from the following link: https://data.nysed.gov/downloads.php. Users must download Report Card Databases and Graduation Rate Databases for the school years ending in years 2015-2019. 
	5. merge_pkl_tables.py 
		- Merges the Graduation Rate and Staff Qualification tables across five years. Output table is still a tall table
	6. run_statistics.py - does the following:
		- Calculates Rank Spearman Correlation coefficient
		- Fits Random Forest Regressors
		- Calculates Impurity and Permutation Feature Importances over all data
		- Calculates Impurity and Permutation Feature Importances for Economically Disadvantaged
		- Plots Histograms and perform Mann Whitney U Test
		- All Data split on Economically Disadvantaged T/F
		- Economically Disadvantaged T split on Charter School T/F
		- Minority T split on Charter School T/F

The d3-bootstrap-viz folder contains all the code necessary for data visualization.  The choropleth, scatter chart, and donut charts are all d3. Bootstrap is used for the layout and styling of the site.


################
# INSTALLATION #
################
In order to run the code, you'll need 5 things:
1. A working python 3.7.4 version
2. A working jupyter notebook environment
3. R and Rstudio (which is the easiest way to view / run R-markdown files)
4. Appropriate python libraries
	python = "^3.7"
	jupyterlab = "^2.2.9"
	pandas = "^1.1.3"
	matplotlib = "^3.3.2"
	scikit-learn = "^0.23.2"
	seaborn = "^0.11.0"
	numpy = "^1.19.2"
5. Appropriate R libraries
	corrplot
	randomForest
	tidyverse
	broom

#############
# Execution #
#############
CORNELL - Recreate Analysis:
	1. Open data_clean_final.ipynb in a jupyter notebook or jupyterlab.
	2. Choose run > run all ... enjoy
	3. Open cornell_pca_lasso_model.ipynb in a jupyter notebook or jupyteralb.
	4. Choose run > run all ... enjoy.
	5. Open cornell_rf_model.Rmd in Rstudio - use setwd() to set the working directory to the notebooks/ folder.
	6. Choose Knit ... enjoy.

d3-bootstrap-viz - run interactive visualization:
	1. Open cmd/bash
	2. cd into the d3-bootstrap-viz dir
	3. Run the following command, python run -m http.server
	4. Open web browser and go to localhost:8000
	5. Click on a county to view demographic breakdown and analysis - enjoy

NYSED - Recreate Analysis:
	1. Create a folder called NysedAnalysis.
	2. Download the data from the following link: https://data.nysed.gov/downloads.php. Users must download Report Card Databases and Graduation Rate Databases for the school years ending in years 2015-2019 as MDB files. Note that MDB files can be on the order of 100 MB.
	3. Copy the MDB files into the **NysedAnalysis** folder.
	4. Copy PY files in the CODE/NYSED folder into the **NysedAnalysis** folder.
	5. Open the NysedAnalysis folder.
	6. Run main_nysed_analysis.py file which runs five scripts

##############
# Demo Video #
##############
