#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main script to run NYSED data analysis

    Author: Ben Spivey
    Created: 11/19/20
    Modified: N/A
    Python: 3
"""

exec(open('mdb_pandas_api.py').read())

exec(open('merge_pkl_tables.py').read())

exec(open('make_wide_dataframe_school.py').read())

exec(open('make_wide_all_features_school.py').read())

exec(open('run_statistics.py').read())