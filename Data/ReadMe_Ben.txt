NYSED Dataset Analysis README

# ------------------------------------------------------------------------------------------#
  run_statistics.py
# ------------------------------------------------------------------------------------------#

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
- df_grad_rate_pct_school_merge.pkl
	- Description: wide table containing SES factors and confounding factors as columns 		and each school as a row.
	- Source: make_wide_all_features_school.py

# ------------------------------------------------------------------------------------------#
  make_wide_all_features_school.py
# ------------------------------------------------------------------------------------------#

Output:
- Creates the wide table containing SES factors and confounding factors as columns and each school as a row.
- Output table file: df_grad_rate_pct_school_merge

Data Input:
- df_combined_all.pkl
	- Description: tall table containing all schools and school years with subgroup 	counts as the column and each school/year/subgroup as a row.
	- Source: merge_pkl_tables.py
- df_grad_rate_pct_school.csv
	-Description: wide table containing SES factors as columns and each school as a row.
	- Source: make_wide_dataframe_school.py

# ------------------------------------------------------------------------------------------#
  make_wide_dataframe_school.py
# ------------------------------------------------------------------------------------------#

Output:
- Creates the wide table containing SES factors as columns and each school as a row.
- Output table file: df_grad_rate_pct_school.csv

Data Input:
- df_grad_rate_15.pkl
- df_grad_rate_16.pkl
- df_grad_rate_17.pkl
- df_grad_rate_18.pkl
- df_grad_rate_19.pkl


# ------------------------------------------------------------------------------------------#
  merge_pkl_tables.py
# ------------------------------------------------------------------------------------------#

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


