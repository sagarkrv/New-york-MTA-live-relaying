Launch command:

/data/spark15/bin/spark-sql –master yarn-client –conf spark.ui.port=40445 –executor-memory 15g –hiveconf load_date=`date +%Y-%m-%d` –driver-memory 10g –queue default –num-executors 20 –conf spark.yarn.executor.memoryOverhead=4096 –queue Q1 -i ./best_states.sql

The best states query follow the pattern of the best hospitals, except that hospitals are not printed

The following should be the result:

================================

State  Overall_ effective_care_
       score    score

================================

TX      13      185.98

MO      12      199.0

IA      12      190.0

OH      12      184.92

SD      12      184.0

IL      12      181.99

IN      11      200.96

MI      11      200.0

IL      11      199.97

WA      11      198.97
