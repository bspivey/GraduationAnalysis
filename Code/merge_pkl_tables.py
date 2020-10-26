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
df_grad_rate_15['YEAR'] = 2015

print(df_grad_rate_15.columns)
print('--------------------------------')

filepath = '../Data/df_grad_rate_16.pkl'
df_grad_rate_16 = pd.read_pickle(filepath)
df_grad_rate_16['YEAR'] = 2016

print(df_grad_rate_16.columns)
print('--------------------------------')

filepath = '../Data/df_grad_rate_17.pkl'
df_grad_rate_17 = pd.read_pickle(filepath)
df_grad_rate_17['YEAR'] = 2017

print(df_grad_rate_17.columns)
print('--------------------------------')

filepath = '../Data/df_grad_rate_18.pkl'
df_grad_rate_18 = pd.read_pickle(filepath)
df_grad_rate_18['YEAR'] = 2018

print(df_grad_rate_18.columns)
print('--------------------------------')

filepath = '../Data/df_grad_rate_19.pkl'
df_grad_rate_19 = pd.read_pickle(filepath)
df_grad_rate_19.columns = df_grad_rate_19.columns.str.upper()
df_grad_rate_19['YEAR'] = 2019

print(df_grad_rate_19.columns)
print('--------------------------------')

dataframe_array = [df_grad_rate_15, df_grad_rate_16, df_grad_rate_17, df_grad_rate_18, \
                   df_grad_rate_19]
df_grad_rate_all = pd.concat(dataframe_array)
df_grad_rate_all.to_pickle('../DataAll/df_grad_rate_all.pkl')

# %% Merge staff qualification tables for 2015-2019
def clean_2015_2017_data(df, year):
    df.rename({'SCHOOL_NAME': 'ENTITY_NAME'}, axis='columns', inplace=True)
    df.rename({'NUM_FEWER_3YRS_EXP': 'NUM_TEACH_INEXP'}, axis='columns', inplace=True)
    df.rename({'NUM_TEACH_OUT_CERT': 'NUM_OUT_CERT'}, axis='columns', inplace=True)
    df = df[['ENTITY_CD', 'NUM_TEACH', 'NUM_TEACH_INEXP', 'NUM_OUT_CERT']]
    df = df.groupby(['ENTITY_CD']).sum()
    df['YEAR'] = year
    df['PER_TEACH_INEXP'] = 100 * df['NUM_TEACH_INEXP'] / df['NUM_TEACH']
    df['PER_OUT_CERT'] = 100 * df['NUM_OUT_CERT'] / df['NUM_TEACH']
    df.update(df[['PER_TEACH_INEXP','PER_OUT_CERT']].fillna(0))
    df = df.round(decimals=2)
    return df

def clean_2018_2019_data(df, year):
    df = df[['ENTITY_CD', 'NUM_TEACH', 'NUM_TEACH_INEXP', 'NUM_TEACH_OC', 'NUM_OUT_CERT']]
    df = df.groupby(['ENTITY_CD']).sum()
    df['YEAR'] = year
    df['PER_TEACH_INEXP'] = 100 * df['NUM_TEACH_INEXP'] / df['NUM_TEACH']
    df['PER_OUT_CERT'] = 100 * df['NUM_OUT_CERT'] / df['NUM_TEACH_OC']
    df.update(df[['PER_TEACH_INEXP','PER_OUT_CERT']].fillna(0))
    df.drop(['NUM_TEACH_OC'], axis=1, inplace=True)
    df = df.round(decimals=2)
    return df

filepath = '../Data/df_staff_qualifications_15.pkl'
df_staff_qualifications_15 = pd.read_pickle(filepath)
df_staff_qualifications_15 = clean_2015_2017_data(df_staff_qualifications_15, 2015)

print(df_staff_qualifications_15.columns)
print('--------------------------------')

filepath = '../Data/df_staff_qualifications_16.pkl'
df_staff_qualifications_16 = pd.read_pickle(filepath)
df_staff_qualifications_16 = clean_2015_2017_data(df_staff_qualifications_16, 2016)

print(df_staff_qualifications_16.columns)
print('--------------------------------')

filepath = '../Data/df_staff_qualifications_17.pkl'
df_staff_qualifications_17 = pd.read_pickle(filepath)
df_staff_qualifications_17 = clean_2015_2017_data(df_staff_qualifications_17, 2017)

print(df_staff_qualifications_17.columns)
print('--------------------------------')

filepath = '../Data/df_staff_qualifications_18_19.pkl'
df_staff_qualifications_18 = pd.read_pickle(filepath)
df_staff_qualifications_18 = clean_2018_2019_data(df_staff_qualifications_18, 2018)

print(df_staff_qualifications_18.columns)
print('--------------------------------')

filepath = '../Data/df_staff_qualifications_19_20.pkl'
df_staff_qualifications_19 = pd.read_pickle(filepath)
df_staff_qualifications_19 = clean_2018_2019_data(df_staff_qualifications_19, 2019)

print(df_staff_qualifications_19.columns)
print('--------------------------------')

dataframe_array = [df_staff_qualifications_15, df_staff_qualifications_16, \
                   df_staff_qualifications_17, df_staff_qualifications_18, \
                   df_staff_qualifications_19]
df_staff_qualifications_all = pd.concat(dataframe_array)
df_staff_qualifications_all.to_pickle('../DataAll/df_staff_qualifications_all.pkl')

# %% Merge graduation rate and staff qualifications for all years into one table
df_combined_all = pd.merge(df_grad_rate_all, df_staff_qualifications_all, \
                                       left_on=['AGGREGATION_CODE', 'YEAR'], \
                                       right_on=['ENTITY_CD', 'YEAR'])
df_combined_all.to_pickle('../DataAll/df_combined_all.pkl')