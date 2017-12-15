SET hive.cli.print.header=true;
DROP TABLE IF EXISTS hos_parquet;
CREATE TABLE hos_parquet AS SELECT * FROM hospitals WHERE provider_id NOT LIKE 'Prov%';
CACHE TABLE hos_parquet;
SELECT COUNT(*) hospitals_count FROM hos_parquet;
EXIT;
