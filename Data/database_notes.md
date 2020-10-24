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
