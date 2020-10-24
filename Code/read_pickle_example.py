#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Script to read .mdb files and convert to pandas dataframes

    Author: Ben Spivey
    Created: 10/24/20
    Modified: N/A
    Python: 3
"""
import pandas as pd


filepath = '../Data/df_grad_rate_18.pkl'
df_grad_rate_18 = pd.read_pickle(filepath)