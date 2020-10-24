# -*- coding: utf-8 -*-
""" Script example to read a pkl file back into a dataframe

    Author: Ben Spivey
    Created: 10/24/20
    Modified: N/A
    Python: 3
"""

import pandas as pd

filepath = '../Data/df_grad_rate_19.pkl'
df_grad_rate_19 = pd.read_pickle(filepath)

filepath = '../Data/df_staff_qualifications_19_20.pkl'
df_staff_qualifications_19_20 = pd.read_pickle(filepath)

"""
filepath = '../Data All/df_grad_rate_all.pkl'
df_grad_rate_all = pd.read_pickle(filepath)

filepath = '../Data All/df_staff_qualifications_all.pkl'
df_staff_qualifications_all = pd.read_pickle(filepath)
"""