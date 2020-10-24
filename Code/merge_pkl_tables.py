#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Merge dataframes and create pkl files

    Author: Ben Spivey
    Created: 10/24/20
    Modified: N/A
    Python: 3
"""

import pandas as pd

# Merge graduation rate tables for 2015-2019
filepath = '../Data/df_grad_rate_15.pkl'
df_grad_rate_15 = pd.read_pickle(filepath)

filepath = '../Data/df_grad_rate_16.pkl'
df_grad_rate_16 = pd.read_pickle(filepath)

filepath = '../Data/df_grad_rate_17.pkl'
df_grad_rate_17 = pd.read_pickle(filepath)

filepath = '../Data/df_grad_rate_18.pkl'
df_grad_rate_18 = pd.read_pickle(filepath)

filepath = '../Data/df_grad_rate_19.pkl'
df_grad_rate_19 = pd.read_pickle(filepath)
df_grad_rate_19.columns = df_grad_rate_19.columns.str.upper()

dataframe_array = [df_grad_rate_15, df_grad_rate_16, df_grad_rate_17, df_grad_rate_18, \
                   df_grad_rate_19]
df_grad_rate_all = pd.concat(dataframe_array)
df_grad_rate_all.to_pickle('../Data All/df_grad_rate_all.pkl')

# %% Merge staff qualification tables for 2015-2019
filepath = '../Data/df_staff_qualifications_15.pkl'
df_staff_qualifications_15 = pd.read_pickle(filepath)
print(df_staff_qualifications_15.columns)
print('--------------------------------')

filepath = '../Data/df_staff_qualifications_16.pkl'
df_staff_qualifications_16 = pd.read_pickle(filepath)
print(df_staff_qualifications_16.columns)
print('--------------------------------')

filepath = '../Data/df_staff_qualifications_17.pkl'
df_staff_qualifications_17 = pd.read_pickle(filepath)
print(df_staff_qualifications_17.columns)
print('--------------------------------')

filepath = '../Data/df_staff_qualifications_18_19.pkl'
df_staff_qualifications_18 = pd.read_pickle(filepath)
print(df_staff_qualifications_18.columns)
print('--------------------------------')

filepath = '../Data/df_staff_qualifications_19_20.pkl'
df_staff_qualifications_19 = pd.read_pickle(filepath)
print(df_staff_qualifications_19.columns)
print('--------------------------------')

dataframe_array = [df_staff_qualifications_15, df_staff_qualifications_16, \
                   df_staff_qualifications_17, df_staff_qualifications_18, \
                   df_staff_qualifications_19]
df_staff_qualifications_all = pd.concat(dataframe_array)
df_staff_qualifications_all.to_pickle('../Data All/df_staff_qualifications_all.pkl')

# %% Merge graduation rate and staff qualifications for all years into one table
df_staff_qualifications_all = pd.merge(df_grad_rate_all, df_staff_qualifications_all, \
                                       left_on=['AGGREGATION_CODE', 'SUBGROUP_CODE']\
                                       right_on='ENTITY_CD')
df_staff_qualifications_all.to_pickle('../Data/df_staff_qualifications_all.pkl')