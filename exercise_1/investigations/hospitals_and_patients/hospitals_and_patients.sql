SET hive.cli.print.header=true;

SELECT corr(int(trim(substr(s.Overall_Rating_of_Hospital_Dimension_Score,1,2))), int(imm2.score)) AS imm2_correlation_coef, 
       corr(int(trim(substr(s.Overall_Rating_of_Hospital_Dimension_Score,1,2))), int(imm3.score)) AS imm3_correlation_coef, 
       corr(int(trim(substr(s.Overall_Rating_of_Hospital_Dimension_Score,1,2))), int(pc01.score)) AS pc01_correlation_coef, 
       corr(int(trim(substr(s.Overall_Rating_of_Hospital_Dimension_Score,1,2))), int(op22.score)) AS op22_correlation_coef
FROM
      sur_resp_parquet s,
     ( SELECT provider_id, score FROM eff_care_parquet WHERE measure_id = 'IMM_2' 
                                                         AND score NOT LIKE 'Not%' ) imm2,
     ( SELECT provider_id, score FROM eff_care_parquet WHERE measure_id = 'IMM_3_OP_27_FAC_ADHPCT' 
                                                         AND score NOT LIKE 'Not%') imm3,
     ( SELECT provider_id, score FROM eff_care_parquet WHERE measure_id = 'PC_01' 
                                                         AND score NOT LIKE 'Not%') pc01,
     ( SELECT provider_id, score FROM eff_care_parquet WHERE measure_id = 'OP_22' 
                                                         AND score NOT LIKE 'Not%') op22
WHERE
      s.provider_number = imm2.provider_id AND
      s.provider_number = imm3.provider_id AND
      s.provider_number = pc01.provider_id AND 
      s.provider_number = op22.provider_id AND
      s.Overall_Rating_of_Hospital_Dimension_Score NOT LIKE 'Not%'
ORDER BY imm2_correlation_coef + imm3_correlation_coef + pc01_correlation_coef + op22_correlation_coef DESC
;

EXIT;

