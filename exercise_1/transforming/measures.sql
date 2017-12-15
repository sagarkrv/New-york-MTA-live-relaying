SET hive.cli.print.header=true;
DROP TABLE IF EXISTS mea_parquet;
CREATE TABLE mea_parquet AS SELECT * FROM measures WHERE measure_id NOT LIKE 'Meas%';
CACHE TABLE mea_parquet;
SELECT COUNT(*) measures_count FROM mea_parquet;
EXIT;
