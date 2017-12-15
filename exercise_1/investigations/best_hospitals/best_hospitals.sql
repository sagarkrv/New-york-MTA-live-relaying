SET hive.cli.print.header=true;

SELECT h.provider_id, h.hospital_name, h.address, h.city, h.state, h.zipcode, h.county_name,
    (
    CASE WHEN h.mortality_national_comparison = "Above the national average" THEN 2 
         WHEN h.mortality_national_comparison = "Same as the national average" THEN 1
         ELSE 0
    END ) + (
    CASE WHEN h.Safety_of_care_national_comparison = "Above the national average" THEN 2 
         WHEN h.Safety_of_care_national_comparison = "Same as the national average" THEN 1
         WHEN h.Safety_of_care_national_comparison = "Below the national average" THEN 0
         ELSE -1
    END ) + (
    CASE WHEN h.Readmission_national_comparison = "Above the national average" THEN 2 
         WHEN h.Readmission_national_comparison = "Same as the national average" THEN 1
         WHEN h.Readmission_national_comparison = "Below the national average" THEN 0
         ELSE -1
    END ) + (
    CASE WHEN h.Patient_experience_national_comparison = "Above the national average" THEN 2 
         WHEN h.Patient_experience_national_comparison = "Same as the national average" THEN 1
         WHEN h.Patient_experience_national_comparison = "Below the national average" THEN 0
         ELSE -1
    END ) + (
    CASE WHEN h.Effectiveness_of_care_national_comparison = "Above the national average" THEN 2 
         WHEN h.Effectiveness_of_care_national_comparison = "Same as the national average" THEN 1
         WHEN h.Effectiveness_of_care_national_comparison = "Below the national average" THEN 0
         ELSE -1
    END ) + (
    CASE WHEN h.Timeliness_of_care_national_comparison = "Above the national average" THEN 2 
         WHEN h.Timeliness_of_care_national_comparison = "Same as the national average" THEN 1
         WHEN h.Timeliness_of_care_national_comparison = "Below the national average" THEN 0
         ELSE -1
    END ) + (
    CASE WHEN h.Efficient_use_of_medical_imaging_national_comparison = "Above the national average" THEN 2 
         WHEN h.Efficient_use_of_medical_imaging_national_comparison = "Same as the national average" THEN 1
         WHEN h.Efficient_use_of_medical_imaging_national_comparison = "Below the national average" THEN 0
         ELSE -1
    END ) as overall_score, 
    ROUND
    (
      CAST(imm2.score AS INT) + 
      CAST(imm3.score AS INT) + 
      (1 - CAST(pc01.score as INT )/100) +  
      (1 - CAST(op22.score as INT )/100)
    ) AS effective_care_score
FROM hos_parquet h, 
     ( SELECT provider_id, score FROM eff_care_parquet WHERE measure_id = 'IMM_2' 
                                                         AND score NOT LIKE 'Not%' ) imm2,
     ( SELECT provider_id, score FROM eff_care_parquet WHERE measure_id = 'IMM_3_OP_27_FAC_ADHPCT' 
                                                         AND score NOT LIKE 'Not%') imm3,
     ( SELECT provider_id, score FROM eff_care_parquet WHERE measure_id = 'PC_01' 
                                                         AND score NOT LIKE 'Not%') pc01,
     ( SELECT provider_id, score FROM eff_care_parquet WHERE measure_id = 'OP_22' 
                                                         AND score NOT LIKE 'Not%') op22
WHERE h.hospital_overall_rating = 5
  AND h.provider_id = imm2.provider_id
  AND h.provider_id = imm3.provider_id
  AND h.provider_id = pc01.provider_id
  AND h.provider_id = op22.provider_id
ORDER BY overall_score DESC, effective_care_score DESC LIMIT 10;

EXIT;

