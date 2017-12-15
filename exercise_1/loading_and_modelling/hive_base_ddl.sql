DROP TABLE hospitals;

CREATE EXTERNAL TABLE hospitals
(
Provider_Id string,
Hospital_Name string,
Address string,
City string,
State string,
Zipcode string,
County_Name string,
Phone_Number string,
Hospital_Type string,
Hospital_Ownership string,
Emergency_Services string,
Crit_Meaningful_use_of_EHRs string,
Hospital_Overall_Rating string,
Hospital_Overall_Rating_Footnote string,
Mortality_National_Comparison string,
Mortality_National_Comparison_Footnote string,
Safety_Of_Care_National_Comparison string,
Safety_Of_Care_National_Comparison_Footnote string,
Readmission_National_Comparison string,
Readmission_National_Comparison_Footnote string,
Patient_Experience_National_Comparison string,
Patient_Experience_National_Comparison_Footnote string,
Effectiveness_Of_Care_National_Comparison string,
Effectiveness_Of_Care_National_Comparison_Footnote string,
Timeliness_Of_Care_National_Comparison string,
Timeliness_Of_Care_National_Comparison_Footnote string,
Efficient_Use_Of_Medical_Imaging_National_Comparison string,
Efficient_Use_Of_Medical_Imaging_National_Comparison_Footnote string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES
(
"separatorChar" = ",",
"escapeChar"    = "\\"
)
STORED AS TEXTFILE
LOCATION '/user/w205/hospital_compare/hospitals_data';


DROP TABLE measures;
CREATE EXTERNAL TABLE measures
(
Measure_Name string,
Measure_ID string,
Measure_Start_Quarter string,
Measure_Start_Date string,
Measure_End_Quarter string,
Measure_End_Date string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES
(
"separatorChar"=",",
"escapeChar" = '\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/hospital_compare/measures_data';

DROP TABLE readmissions_and_deaths;
CREATE EXTERNAL TABLE readmissions_and_deaths
(
Provider_ID string,
Hospital_Name string,
Address string,
City string,
State string,
ZIPCode string,
County string,
Measure_Name string,
Measure_ID string,
VHA_National_Rate string,
Compare_To_National string,
Denominator string,
Score string,
Lower_Estimate string,
Higher_Estimate string,
Footnotes string,
Measure_Start_Date string,
Measure_End_Date string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES
(
"separatorChar"=",",
"escapeChar" = '\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/hospital_compare/readmissions_data';

DROP TABLE effective_care;
CREATE EXTERNAL TABLE effective_care
(
Provider_ID string,
Hospital_Name string,
Address string,
City string,
State string,
ZIPCode string,
County_Name string,
Phone_Number string,
Condition string,
Measure_Id string,
Measure_Name string,
Score string,
Sample string,
Footnote string,
Measure_Start_Date string,
Measure_End_Date string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES
(
"separatorChar"=",",
"escapeChar" = '\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/hospital_compare/effective_care_data';


DROP TABLE survey_responses;
CREATE EXTERNAL TABLE survey_responses
(
Provider_Number string,
Hospital_Name string,
Address string,
City string,
State string,
Zipcode string,
County_Name string,
Communication_With_Nurses_Floor string,
Communication_With_Nurses_Achievement_Threshold string,
Communication_With_Nurses_Benchmark string,
Communication_With_Nurses_Baseline_Rate string,
Communication_With_Nurses_Performance_Rate string,
Communication_With_Nurses_Achievement_Points string,
Communication_With_Nurses_Improvement_Points string,
Communication_With_Nurses_Dimension_Score string,
Communication_With_Doctors_Floor string,
Communication_With_Doctors_Achievement_Threshold string,
Communication_With_Doctors_Benchmark string,
Communication_With_Doctors_Baseline_Rate string,
Communication_With_Doctors_Performance_Rate string,
Communication_With_Doctors_Achievement_Points string,
Communication_With_Doctors_Improvement_Points string,
Communication_With_Doctors_Dimension_Score string,
Responsiveness_Of_Hospital_Staff_Floor string,
Responsiveness_Of_Hospital_Staff_Achievement_Threshold string,
Responsiveness_Of_Hospital_Staff_Benchmark string,
Responsiveness_Of_Hospital_Staff_Baseline_Rate string,
Responsiveness_Of_Hospital_Staff_Performance_Rate string,
Responsiveness_Of_Hospital_Staff_Achievement_Points string,
Responsiveness_Of_Hospital_Staff_Improvement_Points string,
Responsiveness_Of_Hospital_Staff_Dimension_Score string,
Pain_Management_Floor string,
Pain_Management_Achievement_Threshold string,
Pain_Management_Benchmark string,
Pain_Management_Baseline_Rate string,
Pain_Management_Performance_Rate string,
Pain_Management_Achievement_Points string,
Pain_Management_Improvement_Points string,
Pain_Management_Dimension_Score string,
Communication_about_Medicines_Floor string,
Communication_about_Medicines_Achievement_Threshold string,
Communication_about_Medicines_Benchmark string,
Communication_about_Medicines_Baseline_Rate string,
Communication_about_Medicines_Performance_Rate string,
Communication_about_Medicines_Achievement_Points string,
Communication_about_Medicines_Improvement_Points string,
Communication_about_Medicines_Dimension_Score string,
Cleanliness_and_Quietness_Of_Hospital_Environment_Floor string,
Cleanliness_and_Quietness_Of_Hospital_Environment_Achievement_Threshold string,
Cleanliness_and_Quietness_Of_Hospital_Environment_Benchmark string,
Cleanliness_and_Quietness_Of_Hospital_Environment_Baseline_Rate string,
Cleanliness_and_Quietness_Of_Hospital_Environment_Performance_Rate string,
Cleanliness_and_Quietness_Of_Hospital_Environment_Achievement_Points string,
Cleanliness_and_Quietness_Of_Hospital_Environment_Improvement_Points string,
Cleanliness_and_Quietness_Of_Hospital_Environment_Dimension_Score string,
Discharge_Information_Floor string,
Discharge_Information_Achievement_Threshold string,
Discharge_Information_Benchmark string,
Discharge_Information_Baseline_Rate string,
Discharge_Information_Performance_Rate string,
Discharge_Information_Achievement_Points string,
Discharge_Information_Improvement_Points string,
Discharge_Information_Dimension_Score string,
Overall_Rating_Of_Hospital_Floor string,
Overall_Rating_Of_Hospital_Achievement_Threshold string,
Overall_Rating_Of_Hospital_Benchmark string,
Overall_Rating_Of_Hospital_Baseline_Rate string,
Overall_Rating_Of_Hospital_Performance_Rate string,
Overall_Rating_Of_Hospital_Achievement_Points string,
Overall_Rating_Of_Hospital_Improvement_Points string,
Overall_Rating_Of_Hospital_Dimension_Score string,
HCAHPS_Base_Score string,
HCAHPS_Consistency_Score string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES
(
"separatorChar"=",",
"escapeChar" = '\\'
)
STORED AS TEXTFILE
LOCATION '/user/w205/hospital_compare/survey_responses_data';



