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

def clean_grad_rate(df_grad_rate):
    # Select only school rows, no counties, districts, etc.
    df_grad_rate = df_grad_rate[df_grad_rate['AGGREGATION_INDEX'] == 4]

    # Remove rows with ENROLL_CNT == '-'
    df_grad_rate.replace('-', np.NaN, inplace=True)
    df_grad_rate = df_grad_rate[df_grad_rate['ENROLL_CNT'].notna()]

    # Make integer columns an integer data type instead of '0' Python object
    int_columns = ['SUBGROUP_CODE', 'ENROLL_CNT', 'GRAD_CNT', 'REG_CNT', 'REG_ADV_CNT', 'DROPOUT_CNT']
    df_grad_rate[int_columns] = df_grad_rate[int_columns].apply(pd.to_numeric, downcast='integer')

    df_grad_rate.replace(np.NaN, 0, inplace=True)

    return df_grad_rate

def make_wide_dataframe_school(df_grad_rate, year):
    df_grad_rate.columns = df_grad_rate.columns.str.upper()
    df_grad_rate['YEAR'] = year

    # clean df_grad_rate
    df_grad_rate = clean_grad_rate(df_grad_rate)

    ### Pivot the long table to a wide tables
    ## Set values as ENROLL_CNT
    df_grad_rate_enroll = pd.pivot_table(df_grad_rate,
                                             values='ENROLL_CNT',
                                             index='AGGREGATION_CODE',
                                             columns='SUBGROUP_NAME',
                                             aggfunc=np.sum)
    df_grad_rate_enroll.replace(np.NaN, 0, inplace=True)

    # Calculate percent student population by subgroup
    grad_rate_enroll_values = df_grad_rate_enroll.values
    grad_rate_enroll_totals = grad_rate_enroll_values[:, 0]
    grad_rate_enroll_pct = 100 * grad_rate_enroll_values/grad_rate_enroll_totals[:,None]
    df_grad_rate_pct_enroll = pd.DataFrame(grad_rate_enroll_pct, \
                                              columns=df_grad_rate_enroll.columns,
                                              index=df_grad_rate_enroll.index)

    # Remove the 'All Students' column
    df_grad_rate_pct_enroll.drop(columns=['All Students'], inplace=True)

    ## Set values as GRAD_CNT
    df_grad_rate_grad = pd.pivot_table(df_grad_rate,
                                             values='GRAD_CNT',
                                             index='AGGREGATION_CODE',
                                             columns='SUBGROUP_NAME',
                                             aggfunc=np.sum)

    df_grad_rate_grad.replace(np.NaN, 0, inplace=True)

    # Calculate school graduation rate
    school_graduation_rate = df_grad_rate_grad['All Students'] / df_grad_rate_enroll['All Students']
    school_graduation_rate = 100 * school_graduation_rate

    # Augment school graduation rate to the pct_enroll table
    df_grad_rate_pct_enroll['PCT_GRAD'] = school_graduation_rate
    df_grad_rate_pct_enroll.columns = df_grad_rate_pct_enroll.columns.str.upper()
    df_grad_rate_pct_enroll = df_grad_rate_pct_enroll.round(decimals=2)

    # Join the AGGREGATION_CODE, COUNTY_CODE, COUNTY_NAME columns back into the table
    df_grad_rate_small = df_grad_rate[['AGGREGATION_NAME', 'AGGREGATION_CODE', \
                                            'COUNTY_CODE', 'COUNTY_NAME']]
    df_grad_rate_small.drop_duplicates(inplace=True)
    df_grad_rate_pct_enroll = df_grad_rate_pct_enroll.merge(df_grad_rate_small, how='inner', on='AGGREGATION_CODE')
    df_grad_rate_pct_enroll['COUNTY_CODE'] = df_grad_rate_pct_enroll['COUNTY_CODE'].astype('int')
    df_grad_rate_pct_enroll.set_index('AGGREGATION_CODE', drop=True, inplace=True)

    # Standardize column names
    if 'AMERICAN INDIAN/ALASKA NATIVE' in df_grad_rate_pct_enroll.columns:
        before = 'AMERICAN INDIAN/ALASKA NATIVE'
        after = 'AMERICAN INDIAN OR ALASKA NATIVE'
        df_grad_rate_pct_enroll.rename(columns={before:after}, inplace=True)

    if 'ASIAN/PACIFIC ISLANDER' in df_grad_rate_pct_enroll.columns:
        before = 'ASIAN/PACIFIC ISLANDER'
        after = 'ASIAN OR PACIFIC ISLANDER'
        df_grad_rate_pct_enroll.rename(columns={before:after}, inplace=True)

    if 'BLACK OR AFRICAN AMERICAN' in df_grad_rate_pct_enroll.columns:
        before = 'BLACK OR AFRICAN AMERICAN'
        after = 'BLACK'
        df_grad_rate_pct_enroll.rename(columns={before:after}, inplace=True)

    if 'HISPANIC OR LATINO' in df_grad_rate_pct_enroll.columns:
        before = 'HISPANIC OR LATINO'
        after = 'HISPANIC'
        df_grad_rate_pct_enroll.rename(columns={before:after}, inplace=True)

    if 'ENGLISH LANGUAGE LEARNER' in df_grad_rate_pct_enroll.columns:
        before = 'ENGLISH LANGUAGE LEARNER'
        after = 'LIMITED ENGLISH PROFICIENT'
        df_grad_rate_pct_enroll.rename(columns={before:after}, inplace=True)

    if 'NOT ENGLISH LANGUAGE LEARNER' in df_grad_rate_pct_enroll.columns:
        before = 'NOT ENGLISH LANGUAGE LEARNER'
        after = 'NOT LIMITED ENGLISH PROFICIENT'
        df_grad_rate_pct_enroll.rename(columns={before:after}, inplace=True)

    if 'FORMERLY ENGLISH LANGUAGE LEARNER' in df_grad_rate_pct_enroll.columns:
        before = 'FORMERLY ENGLISH LANGUAGE LEARNER'
        after = 'FORMERLY LIMITED ENGLISH PROFICIENT'
        df_grad_rate_pct_enroll.rename(columns={before:after}, inplace=True)

    if 'ENGLISH LANGUAGE LEARNERS' in df_grad_rate_pct_enroll.columns:
        before = 'ENGLISH LANGUAGE LEARNERS'
        after = 'LIMITED ENGLISH PROFICIENT'
        df_grad_rate_pct_enroll.rename(columns={before:after}, inplace=True)

    if 'NON-ENGLISH LANGUAGE LEARNERS' in df_grad_rate_pct_enroll.columns:
        before = 'NON-ENGLISH LANGUAGE LEARNERS'
        after = 'NOT LIMITED ENGLISH PROFICIENT'
        df_grad_rate_pct_enroll.rename(columns={before:after}, inplace=True)

    # Make year columns
    df_grad_rate_pct_enroll['YEAR'] = year

    return df_grad_rate_pct_enroll

# Create grad rate wide table for 2019
filepath = 'df_grad_rate_19.pkl'
df_grad_rate_19 = pd.read_pickle(filepath)
year = 2019
df_grad_rate_19_pct_school = make_wide_dataframe_school(df_grad_rate_19, year)
df_grad_rate_19_pct_school.to_pickle('df_grad_rate_19_pct_school.pkl')
df_grad_rate_19_pct_school.to_csv('df_grad_rate_19_pct_school.csv')

# Create grad rate wide table for 2018
filepath = 'df_grad_rate_18.pkl'
df_grad_rate_18 = pd.read_pickle(filepath)
year = 2018
df_grad_rate_18_pct_school = make_wide_dataframe_school(df_grad_rate_18, year)
df_grad_rate_18_pct_school.to_pickle('df_grad_rate_18_pct_school.pkl')
df_grad_rate_18_pct_school.to_csv('df_grad_rate_18_pct_school.csv')

# Create grad rate wide table for 2017
filepath = 'df_grad_rate_17.pkl'
df_grad_rate_17 = pd.read_pickle(filepath)
year = 2017
df_grad_rate_17_pct_school = make_wide_dataframe_school(df_grad_rate_17, year)
df_grad_rate_17_pct_school.to_pickle('df_grad_rate_17_pct_school.pkl')
df_grad_rate_17_pct_school.to_csv('df_grad_rate_17_pct_school.csv')

# Create grad rate wide table for 2016
filepath = 'df_grad_rate_16.pkl'
df_grad_rate_16 = pd.read_pickle(filepath)
year = 2016
df_grad_rate_16_pct_school = make_wide_dataframe_school(df_grad_rate_16, year)
df_grad_rate_16_pct_school.to_pickle('df_grad_rate_16_pct_school.pkl')
df_grad_rate_16_pct_school.to_csv('df_grad_rate_16_pct_school.csv')

# Create grad rate wide table for 2015
filepath = 'df_grad_rate_15.pkl'
df_grad_rate_15 = pd.read_pickle(filepath)
year = 2015
df_grad_rate_15_pct_school = make_wide_dataframe_school(df_grad_rate_15, year)
df_grad_rate_15_pct_school.to_pickle('df_grad_rate_15_pct_school.pkl')
df_grad_rate_15_pct_school.to_csv('df_grad_rate_15_pct_school.csv')

df_grad_rate_pct_school = pd.concat([df_grad_rate_15_pct_school,
                                     df_grad_rate_16_pct_school,
                                     df_grad_rate_17_pct_school,
                                     df_grad_rate_18_pct_school,
                                     df_grad_rate_19_pct_school],
                                     axis=0)
df_grad_rate_pct_school.to_csv('df_grad_rate_pct_school.csv')