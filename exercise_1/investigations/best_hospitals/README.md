Execute the query using the command:

/data/spark15/bin/spark-sql –master yarn-client –conf spark.ui.port=40445 –executor-memory 15g –hiveconf load_date=`date +%Y-%m-%d` –driver-memory 10g –queue default –num-executors 20 –conf spark.yarn.executor.memoryOverhead=4096 –queue Q1 -i ./best_hospitals.sql


Scope:

The scope is to look ak the overall ratings - above national average, below, same or not available.
Hospitals that have a 5 star rating are only considered, as there are roughly than 4800 hospitals. The best 10 hospitals are chosen based on how they fared against the national average on the following 7 diemsions:

1) mortality_national_comparison

2) Safety_of_care_national_comparison

3) Readmission_national_comparison

4) Patient_experience_national_comparison

5) Effectiveness_of_care_national_comparison

6) Timeliness_of_care_national_comparison

7) Efficient_use_of_medical_imaging_national_comparison



Explanation:

Each dimension such as "Safety of care" gets the below points for example:

    CASE WHEN h.Safety_of_care_national_comparison = "Above the national average" THEN 2 
    
         WHEN h.Safety_of_care_national_comparison = "Same as the national average" THEN 1
    
         WHEN h.Safety_of_care_national_comparison = "Below the national average" THEN 0
         
         WHEN "Not available"  THEN -1
         
Hospitals with no or very little data are penalized with 1 negative point. The minimum score in this scale is -7, while the maximum is 14. If multiple hospitals tie for a certain overall_Score, then the tie is broken with the help of the effective_care sub score.

The effective care sub score is calculated from the below 4 measures using the formula:
imm_2 score + imm_3* score + PC_01 complement score + OP_22 complement score . This score helps to break the tie between multiple hospitals with the same overall score. 


As PC_01 and OP_22 scores are on the opposite end of the scale (lower the better), the complement is taken. 
If 1 is better than 2, then 100-1 is better than 100-2. In this way, all measures are brought on the same side of the scale. 

provider_id     hospital_name           address                                 city           state   zipcode county_name     overall_score   effective_care_score

450023  CITIZENS MEDICAL CENTER         2701 HOSPITAL DRIVE                     VICTORIA        TX      77901   VICTORIA        13              382.0

260006  MOSAIC LIFE CARE AT ST JOSEPH   5325 FARAON STREET                      SAINT JOSEPH    MO      64506   BUCHANAN        12              397.0

160029  MERCY HOSPITAL                   500 E MARKET STREET                    IOWA CITY       IA      52245   JOHNSON         12              388.0

430014  AVERA ST LUKES                  305 S STATE ST  POST OFFICE BOX 4450    ABERDEEN        SD      57401   BROWN           12              382.0

140186  RIVERSIDE MEDICAL CENTER        350 N WALL ST                           KANKAKEE        IL      60901   KANKAKEE        12              379.0

360077  FAIRVIEW HOSPITAL               18101 LORAIN AVENUE                     CLEVELAND       OH      44111   CUYAHOGA        12              375.0

230072  HOLLAND COMMUNITY HOSPITAL      602 MICHIGAN AVE                        HOLLAND         MI      49423   OTTAWA          11              398.0

150158  IU HEALTH WEST HOSPITAL         1111 N RONALD REAGAN PKWY               AVON            IN      46123   HENDRICKS       11              395.0

140202  ADVOCATE CONDELL MEDICAL CENTER 801 S MILWAUKEE AVE                     LIBERTYVILLE    IL      60048   LAKE            11              395.0

450431  ST DAVID'S MEDICAL CENTER       919 E 32ND ST                           AUSTIN          TX      78705   TRAVIS          11              394



