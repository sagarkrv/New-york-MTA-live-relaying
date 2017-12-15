hdfs dfs -ls /user
hdfs dfs -ls /user/w205
wget -O hrf.zip https://data.medicare.gov/views/bg9k-emty/files/e514828f-8ed2-445f-b49f-5ac11a58869d?content_type=application%2Fzip%3B%20charset%3Dbinary&filename=Hospital_Revised_Flatfiles.zip

hdfs dfs -mkdir /user/w205/hospital_compare
hdfs dfs -ls /user/w205

hdfs dfs -mkdir /user/w205/hospital_compare/hospitals_data
hdfs dfs -mkdir /user/w205/hospital_compare/measures_data
hdfs dfs -mkdir /user/w205/hospital_compare/readmissions_data
hdfs dfs -mkdir /user/w205/hospital_compare/effective_care_data
hdfs dfs -mkdir /user/w205/hospital_compare/survey_responses_data

hdfs dfs -ls /user/w205/hospital_compare
hdfs dfs -ls /user/w205

unzip hrf.zip
hdfs dfs -put Hospital\%20General\%20Information.csv /user/w205/hospital_compare/hospitals_data/hospitals.csv
hdfs dfs -put Timely\%20and\%20Effective\%20Care\%20-\%20Hospital.csv /user/w205/hospital_compare/effective_care_data/effective_care.csv
hdfs dfs -put Readmissions\%20and\%20Deaths\%20-\%20VA.csv /user/w205/hospital_compare/readmissions_data/readmissions.csv
hdfs dfs -put Measure\%20Dates.csv /user/w205/hospital_compare/measures_data/Measures.csv
hdfs dfs -put hvbp_hcahps_11_10_2016.csv /user/w205/hospital_compare/survey_responses_data/survey_responses.csv







