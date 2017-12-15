DROP TABLE IF EXISTS sur_resp_parquet;
CREATE TABLE sur_resp_parquet AS SELECT * FROM survey_responses WHERE provider_number NOT LIKE 'Prov%';
CACHE TABLE sur_resp_parquet;
SELECT COUNT(*) responses_count FROM sur_resp_parquet;
EXIT;
