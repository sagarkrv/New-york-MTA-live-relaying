SET hive.cli.print.header=true;
DROP TABLE IF EXISTS rea_deat_parquet;
CREATE TABLE rea_deat_parquet AS SELECT * FROM readmissions_and_deaths WHERE provider_id NOT LIKE 'Prov%';
CACHE TABLE rea_deat_parquet;
SELECT COUNT(*) readmissions_count FROM rea_deat_parquet;
EXIT;
