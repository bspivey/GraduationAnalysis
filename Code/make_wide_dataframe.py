#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script example to create a wide dataframe with subgroup feature columns.
    
    The default table is *long* in how each school has a row for the subgroup.
    We want a *wide* table for building a model such that each school only
    has one row with a column for each subgroup instead.    

    Author: Ben Spivey
    Created: 10/24/20
    Modified: N/A
    Python: 3
"""

import pandas as pd
import numpy as np

# Load dataframe for combined tables
filepath = '../Data/df_grad_rate_19.pkl'
df_grad_rate_19 = pd.read_pickle(filepath)
df_grad_rate_19.columns = df_grad_rate_19.columns.str.upper()
df_grad_rate_19['YEAR'] = 2019

# Select only school rows, no counties, districts, etc.
df_grad_rate_19 = df_grad_rate_19[df_grad_rate_19['AGGREGATION_INDEX'] == 4]

# Remove rows with ENROLL_CNT == '-'
df_grad_rate_19.replace('-', np.NaN, inplace=True)
df_grad_rate_19 = df_grad_rate_19[df_grad_rate_19['ENROLL_CNT'].notna()]

# Make integer columns an integer data type instead of '0' Python object
int_columns = ['SUBGROUP_CODE', 'ENROLL_CNT', 'GRAD_CNT', 'REG_CNT', 'REG_ADV_CNT', 'DROPOUT_CNT']
df_grad_rate_19[int_columns] = df_grad_rate_19[int_columns].apply(pd.to_numeric, downcast='integer') 

### Pivot the long table to a wide tables
## Set values as ENROLL_CNT
df_grad_rate_19_enroll = pd.pivot_table(df_grad_rate_19,
                                         values='ENROLL_CNT',
                                         index='AGGREGATION_NAME',
                                         columns='SUBGROUP_NAME',
                                         aggfunc=np.sum)
df_grad_rate_19_enroll.replace(np.NaN, 0, inplace=True)

# Calculate percent student population by subgroup
grad_rate_19_enroll_values = df_grad_rate_19_enroll.values
grad_rate_19_enroll_totals = grad_rate_19_enroll_values[:, 0]
grad_rate_19_enroll_pct = 100 * grad_rate_19_enroll_values/grad_rate_19_enroll_totals[:,None]
df_grad_rate_19_pct_enroll = pd.DataFrame(grad_rate_19_enroll_pct, \
                                          columns=df_grad_rate_19_enroll.columns,
                                          index=df_grad_rate_19_enroll.index)

# Remove the 'All Students' column
df_grad_rate_19_pct_enroll.drop(columns=['All Students'], inplace=True)

## Set values as GRAD_CNT
df_grad_rate_19_grad = pd.pivot_table(df_grad_rate_19,
                                         values='GRAD_CNT',
                                         index='AGGREGATION_NAME',
                                         columns='SUBGROUP_NAME',
                                         aggfunc=np.sum)

df_grad_rate_19_grad.replace(np.NaN, 0, inplace=True)

# Calculate school graduation rate
school_graduation_rate = df_grad_rate_19_grad['All Students'] / df_grad_rate_19_enroll['All Students']
school_graduation_rate = 100 * school_graduation_rate

# Augment school graduation rate to the pct_enroll table
df_grad_rate_19_pct_enroll['PCT_GRAD'] = school_graduation_rate
df_grad_rate_19_pct_enroll.columns = df_grad_rate_19_pct_enroll.columns.str.upper()
df_grad_rate_19_pct_enroll = df_grad_rate_19_pct_enroll.round(decimals=2)

# Join the AGGREGATION_CODE, COUNTY_CODE, COUNTY_NAME columns back into the table
df_grad_rate_19_small = df_grad_rate_19[['AGGREGATION_NAME', 'AGGREGATION_CODE', \
                                        'COUNTY_CODE', 'COUNTY_NAME']]
df_grad_rate_19_small.drop_duplicates(inplace=True)
df_grad_rate_19_pct_enroll = df_grad_rate_19_pct_enroll.merge(df_grad_rate_19_small, how='inner', on='AGGREGATION_NAME')
df_grad_rate_19_pct_enroll['COUNTY_CODE'] = df_grad_rate_19_pct_enroll['COUNTY_CODE'].astype('int')

# Write out data files
df_grad_rate_19_pct_enroll.to_pickle('../Data/df_grad_rate_19_pct_enroll.pkl')
df_grad_rate_19_pct_enroll.to_csv('../Data/df_grad_rate_19_pct_enroll.csv')