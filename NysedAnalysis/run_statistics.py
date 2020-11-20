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
import plotly.io as pio
import plotly.graph_objects as go
pio.renderers.default='browser'

# Load dataframe containing all features
filepath = 'df_grad_rate_pct_school_merge.csv'
df_all_features_school = pd.read_csv(filepath)

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
spearman_unique.to_csv('spearman_unique.csv')


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

# Make bar chart PCT_GRAD top correlations for high Economically Disadvantaged schools
condition = df_unique_features_school['ECONOMICALLY DISADVANTAGED'] >  \
    df_unique_features_school['ECONOMICALLY DISADVANTAGED'].median()

df_economically_disadvantaged_hi = df_unique_features_school[condition]

spearman_unique_ed = df_economically_disadvantaged_hi.corr(method='spearman')

spearman_unique_pct_grad = spearman_unique_ed.drop(['PCT_GRAD'])
spearman_unique_pct_grad = spearman_unique_pct_grad.sort_values('PCT_GRAD', ascending=False)
fig = go.Figure(go.Bar(
            x=spearman_unique_pct_grad['PCT_GRAD'],
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

# ------------- Random Forest Model - Economically Disadvantaged ------------ #
## All schools - economically disadvantaged
condition = df_unique_features_school['ECONOMICALLY DISADVANTAGED'] >  \
    df_unique_features_school['ECONOMICALLY DISADVANTAGED'].median()

df_economically_disadvantaged_hi = df_unique_features_school[condition]

# Prepare training and testing data
X = df_economically_disadvantaged_hi.drop(columns=['AGGREGATION_NAME', 'YEAR', 'COUNTY_CODE',
                                   'COUNTY_NAME', 'PCT_GRAD', 'ECONOMICALLY DISADVANTAGED'])
y = df_economically_disadvantaged_hi['PCT_GRAD']
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
    xaxis_title='Impurity Feature Importance  - Economically Disadvantaged'
)
fig.show()

# Make bar chart for PCT_GRAD permutation feature importance
df_perm_import = df_perm_import.sort_values('importance', ascending=True)
fig = go.Figure(go.Bar(
            x=df_perm_import['importance'],
            y=df_perm_import['feature'],
            orientation='h'))
fig.update_layout(
    xaxis_title='Permutation Feature Importance - Economically Disadvantaged'
)
fig.show()

# -------------------------- Plot Histograms -------------------------------- #
import scipy.stats as stats

## All schools - economically disadvantaged
condition = df_unique_features_school['ECONOMICALLY DISADVANTAGED'] >  \
    df_unique_features_school['ECONOMICALLY DISADVANTAGED'].median()

df_economically_disadvantaged_hi = df_unique_features_school[condition]
df_economically_disadvantaged_lo = df_unique_features_school[~condition]

x_hi = df_economically_disadvantaged_hi['PCT_GRAD']
x_lo = df_economically_disadvantaged_lo['PCT_GRAD']

fig = go.Figure()
fig.add_trace(go.Histogram(x=x_hi, name='ECONOMICALLY DISADVANTAGED'))
fig.add_trace(go.Histogram(x=x_lo,  name='NOT ECONOMICALLY DISADVANTAGED'))

# Overlay both histograms
fig.update_layout(barmode='overlay',
                  title='Histogram of School Graduation Rates with Median Feature Split',
                  xaxis_title='Graduation Rate',
                  yaxis_title='Count')

# Reduce opacity to see both histograms
fig.update_traces(opacity=0.75)
fig.show()

# Normality test
statistic_hi, p_value_hi = stats.kstest(x_hi, 'norm')
statistic_lo, p_value_lo = stats.kstest(x_lo, 'norm')

print('Histogram of School Graduation Rates with Median Feature Split')
print('p_value_hi', p_value_hi)
print('p_value_lo', p_value_lo)

# Mean hypothesis test
results = stats.mannwhitneyu(x_hi, x_lo, alternative='less')
print('results', results)

## Economically disadvantaged schools - charter schools
condition = df_unique_features_school['ECONOMICALLY DISADVANTAGED'] >  \
    df_unique_features_school['ECONOMICALLY DISADVANTAGED'].median()

df_economically_disadvantaged_hi = df_unique_features_school[condition]

condition_2 = df_economically_disadvantaged_hi['CHARTER'] > \
    df_economically_disadvantaged_hi['CHARTER'].median()

df_charter_hi = df_economically_disadvantaged_hi[condition_2]
df_charter_lo = df_economically_disadvantaged_hi[~condition_2]

x_hi = df_charter_hi['PCT_GRAD']
x_lo = df_charter_lo['PCT_GRAD']

fig = go.Figure()
fig.add_trace(go.Histogram(x=x_hi, name='CHARTER'))
fig.add_trace(go.Histogram(x=x_lo,  name='PUBLIC'))

# Overlay both histograms
fig.update_layout(barmode='overlay',
                  title='Histogram of School Graduation Rates with Median Feature Split given High Economic Disadvantage',
                  xaxis_title='Charter schools',
                  yaxis_title='Count')

# Reduce opacity to see both histograms
fig.update_traces(opacity=0.75)
fig.show()

# Normality test
statistic_hi, p_value_hi = stats.kstest(x_hi, 'norm')
statistic_lo, p_value_lo = stats.kstest(x_lo, 'norm')

print('Histogram of School Graduation Rates with Median Feature Split given High Economic Disadvantage')
print('p_value_hi', p_value_hi)
print('p_value_lo', p_value_lo)

# Mean hypothesis test
results = stats.mannwhitneyu(x_hi, x_lo, alternative='greater')
print('results', results)

## Minority (black and hispanic) schools - charter schools
condition_a = df_unique_features_school['BLACK'] > df_unique_features_school['BLACK'].median()
condition_b = df_unique_features_school['HISPANIC'] > df_unique_features_school['HISPANIC'].median()

df_minority_hi = df_unique_features_school[condition_a | condition_b]

condition_2 = df_minority_hi['CHARTER'] > \
    df_minority_hi['CHARTER'].median()

df_charter_hi = df_minority_hi[condition_2]
df_charter_lo = df_minority_hi[~condition_2]

x_hi = df_charter_hi['PCT_GRAD']
x_lo = df_charter_lo['PCT_GRAD']

fig = go.Figure()
fig.add_trace(go.Histogram(x=x_hi, name='CHARTER'))
fig.add_trace(go.Histogram(x=x_lo,  name='PUBLIC'))

# Overlay both histograms
fig.update_layout(barmode='overlay',
                  title='Histogram of School Graduation Rates with Median Feature Split given High Minority Percentage',
                  xaxis_title='Charter schools',
                  yaxis_title='Count')

# Reduce opacity to see both histograms
fig.update_traces(opacity=0.75)
fig.show()

# Normality test
statistic_hi, p_value_hi = stats.kstest(x_hi, 'norm')
statistic_lo, p_value_lo = stats.kstest(x_lo, 'norm')

print('Histogram of School Graduation Rates with Median Feature Split given High Minority Percentage')
print('p_value_hi', p_value_hi)
print('p_value_lo', p_value_lo)

# Mean hypothesis test
results = stats.mannwhitneyu(x_hi, x_lo, alternative='greater')
print('results', results)