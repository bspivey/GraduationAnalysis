# Guide to the "dave" Folder
Nick and I put our models, data, cleaning, and Exploratory Data Analysis (EDA) code in here.  Here are the salient files and what they do:

## Code for Cleaning, EDA, and Models
* Modeling_Nick.Rmd - Random Forest and Feature Selection in R -- documented inline
* data_clean_final.ipynb - data loader, cleaner, and imputer -- documented inline
* regress_me.ipynb - EDA and assumptions.  Kinda messy, but somewhat documented inline... you can mostly ignore unless curious.
* dave_model.ipynb - Linear Modeling, dimensionality reduction, and Lasso feature selection by county

## Data
In the data folder is most of the data.  There are both source files from Cornell and results files.
* source: apm_all.csv
* source: 36_County_Coverage_A.txt - county to district mapping information
* source: BasicInfo2.csv - District information
* source: apm_all.csv - cohort and year information.
* source: FARU_all.csv - financial information to district - we join this to graduation data.
* source: graduation_all.csv - graduation rates and basic cohort information  
---
* results: boces_notes.txt - data dictionary for the final output
* results: PCA_plus_preds.csv - the dimensionality reduction raw information and raw prediction information by county
* results: county_agg_results.csv - Linear model summary statistics (Explained Variance, MSE, R^2, Coefs and Intercept) data
* results: regressionR2.csv - summary statistics for the random forest regression model (in R)

## Instructions:
1. Run `data_clean_final.ipynb` to load and clean the data.  Methods are documented in-notebook.
2. Run `Modeling_Nick.Rmd` to see Random Forest feature selection for the entire data set.
3. Run `dave_model.ipynb` to see summary statistics for linear models by county, as well as Lasso selection for feature importance.

