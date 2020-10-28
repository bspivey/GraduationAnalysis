#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script example to fit a nonlinear model on the graduate rate and staff
    qualification data set.
    
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
filepath = '../DataAll/df_combined_all.pkl'
df_combined_all = pd.read_pickle(filepath)

# Select only school rows
df_combined_all = df_combined_all[df_combined_all['AGGREGATION_INDEX'] == 4]

# For Albany county
df_combined_1 = df_combined_all[df_combined_all['COUNTY_CODE'] == 1]
