#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script to calculate statistics and identify feature importances

    Reads the df_grad_rate_pct_school_merge dataframe and runs statistics
    to understand the features that correlate most with graduation rate.

    Author: Ben Spivey
    Created: 11/07/20
    Modified: N/A
    Python: 3
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.io as pio
import plotly.graph_objects as go
pio.renderers.default='browser'

# Load dataframe containing all features
filepath = '../Data/df_grad_rate_pct_school_merge.pkl'
df_all_features_school = pd.read_pickle(filepath)

# -------------------- Spearman's Rank Correlation -------------------------- #
# Spearman's Rank Correlation test on all features
spearman = df_all_features_school.corr(method='spearman')

spearman_binary = spearman.copy()
condition = (spearman.values > 0.7) | (spearman.values < -0.7)
spearman_binary[condition] = 1
spearman_binary[~condition] = 0

fig = go.Figure(data=go.Heatmap(z=spearman_binary.values,
                                x=spearman_binary.index,
                                y=spearman_binary.columns,
                                colorscale='Blues'))
fig.show()

# Spearman's Rank Correlation test on reduced features
columns = ['NOT ECONOMICALLY DISADVANTAGED',
           'NOT LIMITED ENGLISH PROFICIENT',
           'NOT IN FOSTER CARE',
           'PARENT NOT IN ARMED FORCES',
           'NUM_OUT_CERT',
           'NOT MIGRANT',
           'GENERAL EDUCATION STUDENTS',
           'NOT HOMELESS',
           'MALE',
           'FORMERLY LIMITED ENGLISH PROFICIENT',
           'NRC_CODE',
           'AGGREGATION_CODE']
df_unique_features_school = df_all_features_school.drop(columns=columns)

spearman_unique = df_unique_features_school.corr(method='spearman')
spearman_unique.to_csv('../Data/PlotData/spearman_unique.csv')


fig = go.Figure(data=go.Heatmap(z=spearman_unique.values,
                                x=spearman_unique.index,
                                y=spearman_unique.columns,
                                colorscale='RdBu'))
fig.show()

# Make bar chart for PCT_GRAD top correlations
spearman_unique_pct_grad = spearman_unique.drop(['PCT_GRAD'])
spearman_unique_pct_grad = spearman_unique_pct_grad.sort_values('PCT_GRAD', ascending=False)
fig = go.Figure(go.Bar(
            x=spearman_unique_pct_grad['PCT_GRAD'],
            y=spearman_unique_pct_grad.index,
            orientation='h'))
fig.update_layout(
    xaxis_title='Spearman Rank Correlation'
)
fig.show()

# Make bar chart for ECONOMICALLY DISADVANTAGED top correlations
spearman_unique_pct_grad = spearman_unique.drop(['ECONOMICALLY DISADVANTAGED'])
spearman_unique_pct_grad = spearman_unique_pct_grad.sort_values('ECONOMICALLY DISADVANTAGED', ascending=True)
fig = go.Figure(go.Bar(
            x=spearman_unique_pct_grad['ECONOMICALLY DISADVANTAGED'],
            y=spearman_unique_pct_grad.index,
            orientation='h'))
fig.update_layout(
    xaxis_title='Spearman Rank Correlation'
)
fig.show()

# ------------------------ Random Forest Model ------------------------------ #
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import permutation_importance

# Prepare training and testing data
X = df_unique_features_school.drop(columns=['AGGREGATION_NAME', 'YEAR', 'COUNTY_CODE',
                                   'COUNTY_NAME', 'PCT_GRAD'])
y = df_unique_features_school['PCT_GRAD']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)

# Fit the Random Forest Regressor
rf = RandomForestRegressor(n_estimators=200, max_features=0.33,
                           random_state=1, oob_score=True)
rf.fit(X_train, y_train)

importance = rf.feature_importances_
df_feat_import = pd.DataFrame({'feature':X.columns, 'importance':importance})

perm_importance = permutation_importance(rf, X_test, y_test)
df_perm_import = pd.DataFrame({'feature':X.columns, 'importance':perm_importance.importances_mean})

# Make bar chart for PCT_GRAD impurity-based feature importance
df_feat_import = df_feat_import.sort_values('importance', ascending=True)
fig = go.Figure(go.Bar(
            x=df_feat_import['importance'],
            y=df_feat_import['feature'],
            orientation='h'))
fig.update_layout(
    xaxis_title='Impurity Feature Importance'
)
fig.show()

# Make bar chart for PCT_GRAD permutation feature importance
df_perm_import = df_perm_import.sort_values('importance', ascending=True)
fig = go.Figure(go.Bar(
            x=df_perm_import['importance'],
            y=df_perm_import['feature'],
            orientation='h'))
fig.update_layout(
    xaxis_title='Permutation Feature Importance'
)
fig.show()


