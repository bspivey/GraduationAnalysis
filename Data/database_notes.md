# Database Tables


* Merging Graduation Rate and Report Card tables
	
	Graduation Rate		Report Card
	AGGREGATION_CODE   ==	ENTITY_CD


# Report Card Database Tables
* Combined state/federal expenditure per student by school and county: Expenditures per Pupil
	- PER_FED_STATE_LOCAL_EXP: combines state and federal
	- PUPIL_COUNT_TOT
	- YEAR
	- ENTITY_NAME
	- ENTITY_CD

* Staff inexperience or out of certification by school and county: Staff Qualifications or Staff
	- PER_TEACH_INEXP
	- PER_PRINC_INEXP
	- PER_OUT_CERT
	- ENTITY_NAME
	- ENTITY_CD

* Subgroup distributions: ACC HS Graduation Rate
	- SUBGROUP_NAME: ethnicity, disabilities, economically disadvantaged, English language learners.
	- COHORT_COUNT
	- GRAD_RATE
	- ENTITY_CD
	- ENTITY_NAME

* Annual EM ELA/Math/Science Proficiency: Annual EM ELA, Annual EM MATH, Annual EM SCIENCE
	- PER_PROF (Shows most distinction)
	- TOTAL_SCALE_SCORES
	- MEAN_SCORES
	- SUBGROUP_NAME
	- YEAR
	- ASSESSMENT_NAME
	- ENTITY_NAME
	- ENTITY_CD

* Graduation rates: ACC HS Graduation Rate
	- GRAD_RATE
	- COHORT_COUNT
	- YEAR
	- SUBGROUP_NAME
	- ENTITY_NAME
	- ENTITY_CD

# Graduation Rate tables
	- NRC_DESC: Charters, NYC, Average Needs, Low Needs, Rural High Needs, ...
	- NRC_CODE
	- SUBGROUP_NAME:
		- Sex: Male/Female
		- Ethnicity: Black or African American/Hispanic or Latino/Asian or Pacific Islander/White/Multiracial
		- Disability: Students with Disabilities
		- Non-English Language Learners/English Language Learners
		- Economically Disadvantaged/Not Economically Disadvantaged
		- Not Migrant/Migrant
		- All Students.
	- SUBGROUP_CODE
	- COUNTY_CODE
	- COUNTY_NAME
	- ENROLL_CNT
	- GRAD_CNT
	- GRAD_PCT
	- REG_ADV_CNT
	- REG_ADV_PCT
	- DROPOUT_CNT
	- DROPOUT_PCT

# Define Features
I see two options for defining features based on SUBGROUP which is one column in the raw Graduation Rate table. We need to build models for each county regardless.
* Create no new columns. Use SUBGROUP as the one input feature and GRAD_PCT and DROP_PCT as two outputs for two different models.
* Pivot the table to create a column for each SUBGROUP with the values being the percentage composition of that subgroup.



# Plots
	- Click on county. Show aggregate statistics per county.
	- Click on county. Show x vs. y. Example: Grad Rate vs. Economic Disadvantage
		- Regression: slope and intercept. p-value.
	- Click on county. Show feature importance by county.
