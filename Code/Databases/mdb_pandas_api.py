# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# -----------------------Not needed--------------------------------------------
# Using Meza

#from meza import io, convert as cv
# Read MDB file into Python
#records = io.read('GRAD_RATE_AND_OUTCOMES_2019.mdb') # only file path, no file objects
#print(next(records))
#io.write('grad_rate_and_outcomes_2019.csv', cv.records2csv(records))
# -----------------------Not needed--------------------------------------------

# ------------------------Using subprocess, pandas-----------------------------
# Read mdb into a dictionary of pandas tables
import sys, subprocess, os
from io import StringIO
import pandas as pd
verbose = True

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
database_path = 'gradrate_2019/GRAD_RATE_AND_OUTCOMES_2019.mdb'
out_tables = mdb_to_pandas(database_path)
table_names = list(out_tables.keys())
df_grad_rate_19 = out_tables['GRAD_RATE_AND_OUTCOMES_2019']
print('\ntable names = ', table_names)
print('\ntable columns = ', df_grad_rate_19.columns)
print('\ntable head = ', df_grad_rate_19.head())
print('unique nrc_desc', df_grad_rate_19['nrc_desc'].unique())
print('unique subgroup_name', df_grad_rate_19['subgroup_name'])

database_path = 'SRC2018/SRC2018_20190627.mdb'
out_tables = mdb_to_pandas(database_path)
table_names = list(out_tables.keys())
df_staff_qualifications_18 = out_tables['Staff Qualifications']

print('\ntable names = ', table_names)
print('\ntable columns = ', df_staff_qualifications_18.columns)
print('\ntable head = ', df_staff_qualifications_18.head())
#print('unique nrc_desc', df_grad['nrc_desc'].unique())
#print('unique subgroup_name', df_grad['subgroup_name'])