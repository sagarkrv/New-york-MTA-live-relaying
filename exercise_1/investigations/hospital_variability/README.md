Launch the command

/data/spark15/bin/spark-sql –master yarn-client –conf spark.ui.port=40445 –executor-memory 15g –hiveconf load_date=`date +%Y-%m-%d` –driver-memory 10g –queue default –num-executors 20 –conf spark.yarn.executor.memoryOverhead=4096 –queue Q1 -i ./hospital_variability.sql

The procedures with the highest variability is calculated using the formula 
range/std deviation

Basically how many std deviations is the range. Higher the spread, higher the variability of the procedure. The fill_rate is the percentage of hospitals that have reported this data.

measure_id              measure_name               fill_rate       min_score       max_score   avg_score       std_deviation   variability

ED_1b                   ED1                        0.769           30              1239        277.255          103.988         11.626

OP_20                   Door to diagnostic eval    0.778            0               158         24.15            14.963         10.559

ED_2b                   ED2                        0.767            0               628        101.476           65.142          9.64

OP_18b                  OP 18                      0.777           45               440        141.693           42.051          9.393

OP_21                   Median time to pain med    0.735            5               151         51.536           17.669          8.263

IMM_2                   Immunization for influenza 0.84             0               100         91.843           13.169          7.594

IMM_3_OP_27_FAC_ADHPCT  Healthcare workers given   0.873            0               100         85.892           14.06           7.113
         
                        influenza vaccination
                        
Time taken: 33.912 seconds, Fetched 7 row(s)
