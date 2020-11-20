#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script to merge all features for statistics and machine learning

    Author: Ben Spivey
    Created: 11/07/20
    Modified: N/A
    Python: 3
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load dataframe for combined tables
filepath = 'df_combined_all.pkl'
df_combined_all = pd.read_pickle(filepath)

# Select only school rows
df_combined_all = df_combined_all[df_combined_all['AGGREGATION_INDEX'] == 4]

# Select only one school
#df_combined_1 = df_combined_all[df_combined_all['AGGREGATION_NAME'] == 	'CENTRAL VALLEY ACADEMY']
df_combined_1 = df_combined_all

# Select only feature columns and key columns
cols_to_merge = ['AGGREGATION_CODE', 'AGGREGATION_NAME', 'YEAR', 'NUM_OUT_CERT', 'PER_TEACH_INEXP', 'PER_OUT_CERT', 'NRC_CODE']
df_combined_features = df_combined_1[cols_to_merge]
df_combined_features.drop_duplicates(inplace=True)
cols_to_merge_key = ['AGGREGATION_CODE', 'AGGREGATION_NAME', 'YEAR']
df_combined_features = df_combined_features.groupby(cols_to_merge_key, group_keys=True).min()
df_combined_features = df_combined_features.sort_values(by=cols_to_merge_key) \
                                           .reset_index()

# Load dataframe for wide table
filepath = 'df_grad_rate_pct_school.csv'
df_grad_rate_pct_school = pd.read_csv(filepath)

# Select only one school
#df_grad_rate_pct_school = df_grad_rate_pct_school[df_grad_rate_pct_school['AGGREGATION_NAME'] == 'CENTRAL VALLEY ACADEMY']

df_grad_rate_pct_school = df_grad_rate_pct_school.sort_values(by=cols_to_merge_key) \
                                                 .reset_index() \
                                                 .drop(columns=['index'])

# Merge staff qualification and charter school colums into the wide table
df_grad_rate_pct_school_merge = df_grad_rate_pct_school.merge(df_combined_features, \
                                                              how='left', on=cols_to_merge_key)
df_grad_rate_pct_school_merge['CHARTER'] = df_grad_rate_pct_school_merge['NRC_CODE'] > 6
df_grad_rate_pct_school_merge.replace(np.NaN, 0, inplace=True)

df_grad_rate_pct_school_merge.to_csv('df_grad_rate_pct_school_merge.csv')