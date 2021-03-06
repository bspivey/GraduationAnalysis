# -*- coding: utf-8 -*-
"""Function to read .mdb files and convert to a dictionary of dataframes

    Author: Ben Spivey
    Created: 10/4/20
    Modified: N/A
    Python: 3
"""

import sys, subprocess
from io import StringIO
import pandas as pd
verbose = True

# Read mdb into a dictionary of pandas tables
def mdb_to_pandas(database_path):
    subprocess.call(["mdb-schema", database_path, "mysql"])
    # Get the list of table names with "mdb-tables"
    table_names = subprocess.Popen(["mdb-tables", "-1", database_path],
                                   stdout=subprocess.PIPE).communicate()[0]
    tables = table_names.splitlines()
    sys.stdout.flush()

    # Dump each table as a stringio using "mdb-export",
    out_tables = {}
    for rtable in tables:
        table = rtable.decode()
        if verbose: print('running table:',table)
        if table != '':
            if verbose: print("Dumping " + table)
            contents = subprocess.Popen(["mdb-export", database_path, table],
                                        stdout=subprocess.PIPE).communicate()[0]
            temp_io = StringIO(contents.decode())
            print(table, temp_io)
            out_tables[table] = pd.read_csv(temp_io)
    return out_tables

# Query tables

# Graduation Rate and Outcomes 2019
database_path = 'GRAD_RATE_AND_OUTCOMES_2019.mdb'
out_tables = mdb_to_pandas(database_path)
table_names = list(out_tables.keys())
df_grad_rate_19 = out_tables['GRAD_RATE_AND_OUTCOMES_2019']
df_grad_rate_19.to_pickle('df_grad_rate_19.pkl')

print('-------')
print('\ntable names = ', table_names)
print('\ntable columns = ', df_grad_rate_19.columns)
print('\ntable head = ', df_grad_rate_19.head())
print('unique nrc_desc', df_grad_rate_19['nrc_desc'].unique())
print('unique subgroup_name', df_grad_rate_19['subgroup_name'])

# Graduation Rate and Outcomes 2018
database_path = 'GRAD_RATE_AND_OUTCOMES_2018.mdb'
out_tables = mdb_to_pandas(database_path)
table_names = list(out_tables.keys())
df_grad_rate_18 = out_tables['GRAD_RATE_AND_OUTCOMES_2018']
df_grad_rate_18.to_pickle('df_grad_rate_18.pkl')

print('-------')
print('\ntable names = ', table_names)
print('\ntable columns = ', df_grad_rate_18.columns)
print('\ntable head = ', df_grad_rate_18.head())

# Graduation Rate and Outcomes 2017
database_path = 'GRAD_RATE_AND_OUTCOMES_2017.mdb'
out_tables = mdb_to_pandas(database_path)
table_names = list(out_tables.keys())
df_grad_rate_17 = out_tables['GRAD_RATE_AND_OUTCOMES_2017']
df_grad_rate_17.to_pickle('df_grad_rate_17.pkl')

print('-------')
print('\ntable names = ', table_names)
print('\ntable columns = ', df_grad_rate_17.columns)
print('\ntable head = ', df_grad_rate_17.head())

# Graduation Rate and Outcomes 2016
database_path = 'GRAD_RATE_AND_OUTCOMES_2016.mdb'
out_tables = mdb_to_pandas(database_path)
table_names = list(out_tables.keys())
df_grad_rate_16 = out_tables['GRAD_RATE_AND_OUTCOMES_2016']
df_grad_rate_16.to_pickle('df_grad_rate_16.pkl')

print('-------')
print('\ntable names = ', table_names)
print('\ntable columns = ', df_grad_rate_16.columns)
print('\ntable head = ', df_grad_rate_16.head())

# Graduation Rate and Outcomes 2015
database_path = 'GRAD_RATE_AND_OUTCOMES_2015.mdb'
out_tables = mdb_to_pandas(database_path)
table_names = list(out_tables.keys())
df_grad_rate_15 = out_tables['GRAD_RATE_AND_OUTCOMES_2015']
df_grad_rate_15.to_pickle('df_grad_rate_15.pkl')

print('-------')
print('\ntable names = ', table_names)
print('\ntable columns = ', df_grad_rate_15.columns)
print('\ntable head = ', df_grad_rate_15.head())


# Report Card Staff Qualifications 2019
database_path = 'SRC2019_20200703.mdb'
out_tables = mdb_to_pandas(database_path)
table_names = list(out_tables.keys())
df_staff_qualifications_19_20 = out_tables['Staff Qualifications']
df_staff_qualifications_19_20.to_pickle('df_staff_qualifications_19_20.pkl')

print('-------')
print('\ntable names = ', table_names)
print('\ntable columns = ', df_staff_qualifications_19_20.columns)
print('\ntable head = ', df_staff_qualifications_19_20.head())

# Report Card Staff Qualifications 2018
database_path = 'SRC2018_20190627.mdb'
out_tables = mdb_to_pandas(database_path)
table_names = list(out_tables.keys())
df_staff_qualifications_18_19 = out_tables['Staff Qualifications']
df_staff_qualifications_18_19.to_pickle('df_staff_qualifications_18_19.pkl')

print('-------')
print('\ntable names = ', table_names)
print('\ntable columns = ', df_staff_qualifications_18_19.columns)
print('\ntable head = ', df_staff_qualifications_18_19.head())

# Report Card Staff Qualifications 2017
database_path = 'SRC2017GroupIIRelease.mdb'
out_tables = mdb_to_pandas(database_path)
table_names = list(out_tables.keys())
df_staff_qualifications_17 = out_tables['Staff']
df_staff_qualifications_17.to_pickle('df_staff_qualifications_17.pkl')

print('-------')
print('\ntable names = ', table_names)
print('\ntable columns = ', df_staff_qualifications_17.columns)
print('\ntable head = ', df_staff_qualifications_17.head())

# Report Card Staff Qualifications 2016
database_path = 'SRC2016_GroupIII.mdb'
out_tables = mdb_to_pandas(database_path)
table_names = list(out_tables.keys())
df_staff_qualifications_16 = out_tables['Staff']
df_staff_qualifications_16.to_pickle('df_staff_qualifications_16.pkl')

print('-------')
print('\ntable names = ', table_names)
print('\ntable columns = ', df_staff_qualifications_16.columns)
print('\ntable head = ', df_staff_qualifications_16.head())

# Report Card Staff Qualifications 2015
database_path = 'SRC2015.mdb'
out_tables = mdb_to_pandas(database_path)
table_names = list(out_tables.keys())
df_staff_qualifications_15 = out_tables['Staff']
df_staff_qualifications_15.to_pickle('df_staff_qualifications_15.pkl')

print('-------')
print('\ntable names = ', table_names)
print('\ntable columns = ', df_staff_qualifications_15.columns)
print('\ntable head = ', df_staff_qualifications_15.head())