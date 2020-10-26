# CSE6242
Repository for CSE 6242 Fall 2020

# Installing the environment
Environment for this project is tracked through conda and environment.yml file.
Install the environment with this command `conda env update --file environment.yml`
Update any packages in the environment with this command `conda env export > environment.yml`

# Getting the Data
The data files are too large to commit, and Ben and Nick wrote some data cleaning stuff that's very helpful.  All the data files can be found here: https://data.nysed.gov/downloads.php.  You can download the .zip files from that link, and then unzip them to a folder to use them.  I put my raw data in subfolders (for instance `./data/report_card/` contains all my report card .mdb files). Here's how you use those files to get the data into useful format:

1. create a new folder in the repo root called DataAll
2. open a command prompt and switch to the `/Code/` directory
3. run `python merge_pkl_tables.py`
4. check the DataAll folder and there should be 3 new files
    `df_combined_all.pkl`
    `df_grad_rate_all.pkl`
    `df_staff_qualifications_all.pkl`

# Progress Report Notes

## Introduction

## Problem Definition

## Survey

## Proposed Method
We suggest using proxy features for SES and AP, as much as we can reasonably include in the data set and still be able to roll up to various aggregate levels.  Here is a list of the proposed proxies.

### As of 10/25/20:
I'd like to have more proxies for inputs, but it's not in the data we have already.  We can put it off until later if we want because it's going to take some digging in my opinion. Let's discuss criteria for SES proxies.

##### (agg level) SES Proxies -- inputs / features / treatment variables.
* (school, district only) NRC_Code / NRC_Desc
* (county, state, district) Income / Earnings statistics for that aggregation levels - (we still need this data - maybe https://data.bls.gov/cew/doc/access/csv_data_slices.htm?)

##### (agg level) AP Proxies -- outputs / outcome variables
* (school, district, county, state) - grad_rate.GRAD_CNT
* (school, district, county, state) - grad_rate.GRAD_PCT
* (district only) - Grades 3 to 8 Assessment in ELA and Math

## Conclusions and Discussion


# TODO:
[ ] - Discuss criteria for SES Proxies (AP is pretty straightforward)
[ ] - Begin progress report DRAFT
[ ] - Engineer more proxies for SES
[ ] - Engineer more proxies for AP
[ ] - Design Map Features: Aggregation Levels, Hover, Feature Set, etc.
[ ] - Write base model (regression?  RF?)
[ ] - Validate data assumptions & more EDA
[ ] - Dig through the rest of the tables in report_card
[ ] - Do we need some task management thing like Trello?  Seems like unnecesary overhead, but let's discuss.

