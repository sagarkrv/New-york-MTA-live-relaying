These files have DDLs that create the necessary parquet tables

In this step, we create parquet tables from the hive tables in spark sql. No specific transformation would be done
as I intend to use the in-memory columnar DB 's advantages to do transformations on the fly after loading.
For this OLAP task, reduction into 3rd Normal Form is a liability. 

Step 1: Download the .sql files into your current directory and execute the shell command

Step 2: Launch the below commands in your shell /data/spark15/bin/spark-sql –master yarn-client –conf spark.ui.port=40445 –executor-memory 15g –hiveconf load_date=date +%Y-%m-%d –driver-memory 10g –queue default –num-executors 20 –conf spark.yarn.executor.memoryOverhead=4096 –queue Q1 -i ./hospital.sql

/data/spark15/bin/spark-sql –master yarn-client –conf spark.ui.port=40445 –executor-memory 15g –hiveconf load_date=date +%Y-%m-%d –driver-memory 10g –queue default –num-executors 20 –conf spark.yarn.executor.memoryOverhead=4096 –queue Q1 -i ./eff_care.sql

/data/spark15/bin/spark-sql –master yarn-client –conf spark.ui.port=40445 –executor-memory 15g –hiveconf load_date=date +%Y-%m-%d –driver-memory 10g –queue default –num-executors 20 –conf spark.yarn.executor.memoryOverhead=4096 –queue Q1 -i ./readmissions.sql

/data/spark15/bin/spark-sql –master yarn-client –conf spark.ui.port=40445 –executor-memory 15g –hiveconf load_date=date +%Y-%m-%d –driver-memory 10g –queue default –num-executors 20 –conf spark.yarn.executor.memoryOverhead=4096 –queue Q1 -i ./measures.sql

/data/spark15/bin/spark-sql –master yarn-client –conf spark.ui.port=40445 –executor-memory 15g –hiveconf load_date=date +%Y-%m-%d –driver-memory 10g –queue default –num-executors 20 –conf spark.yarn.executor.memoryOverhead=4096 –queue Q1 -i ./survey_responses.sql

