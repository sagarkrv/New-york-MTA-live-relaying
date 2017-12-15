DROP TABLE IF EXISTS eff_care_parquet ;
CREATE TABLE eff_care_parquet AS SELECT * FROM effective_care WHERE provider_id NOT LIKE 'Prov%';
CACHE TABLE eff_care_parquet;
SELECT COUNT(*) effective_care_count FROM eff_care_parquet;
EXIT;
