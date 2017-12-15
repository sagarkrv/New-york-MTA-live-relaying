Launcg using the command:

/data/spark15/bin/spark-sql –master yarn-client –conf spark.ui.port=40445 –executor-memory 15g –hiveconf load_date=`date +%Y-%m-%d` –driver-memory 10g –queue default –num-executors 20 –conf spark.yarn.executor.memoryOverhead=4096 –queue Q1 -i ./hospitals_and_patients.sql

In order to find correlation, two tables are joined:

a) eff_care_parquet (Effective Care) and

b) sur_resp_parquet (Survey responses)

The overall_Rating_of_Hospital_Dimension_Score is the field in the survey responses that gives one single measure of overall satisfaction. This value is a function of 7 measures. That said, this field has values from 0 to 10. The procedure followed is to compare this field with the "score" from the effective care table/collection only for measures that have sufficient data for majority of the hospitals. As a consequence only 4 measures have been chosen for the scope of this analysis:

IMM_2: Patients assessed and given influenza vaccination Higher percentages are better

IMM_3_OP_27_FAC_ADHPCT: Healthcare workers given influenza vaccination Higher percentages are better

PC_01: Percent of mothers whose deliveries were scheduled too early (1-2 weeks early), when a scheduled delivery was not medically necessary (Lower percentages are better)

OP22: Percentage of patients who left the emergency department before being seen Lower percentages are better

The results obtained were as follows:
IMM2_coeff : 0.04
IMM3_coeff : 0.08
PC01 coeff : 0.004 
OP22 coeff : -0.0009

So the conclusion for the above 4 important "effective care measures", there is no or very little correlation between patient survey responses and hospital quality ratings
