# -*- coding: utf-8 -*-
""" Script example to read .mdb files and view one table as a dataframe

    Author: Ben Spivey
    Created: 10/24/20
    Modified: N/A
    Python: 3
"""

from importlib import reload
import mdb_pandas_api
reload(mdb_pandas_api)

# Report Card Staff Qualifications 2019
database_path = '../Data/GRAD_RATE_AND_OUTCOMES_2018.mdb'
out_tables = mdb_pandas_api.mdb_to_pandas(database_path)
table_names = list(out_tables.keys())
df_grad_rate_18 = out_tables['GRAD_RATE_AND_OUTCOMES_2018']

print('-------')
print('\ntable names = ', table_names)
print('\ntable columns = ', df_grad_rate_18.columns)
print('\ntable head = ', df_grad_rate_18.head())

df_grad_rate_18.to_pickle('../Data/df_grad_rate_18.pkl')