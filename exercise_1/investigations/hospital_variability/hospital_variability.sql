SET hive.cli.print.header=true;

SELECT a.measure_id, a.measure_name, 
       round(COUNT(a.provider_id)/4812,3) fill_rate,
       min(int(a.score)) min_score, 
       max(int(a.score)) max_score,
       round(avg(int(a.score)),3) avg_score,
       round(stddev_pop(a.score),3) std_deviation,
       round(abs(max(int(a.score)) - min(int(a.score)) )/stddev_pop(a.score),3) as variability  
FROM eff_care_parquet a
WHERE
     a.score NOT LIKE 'Not%'
GROUP BY a.measure_id, a.measure_name
HAVING fill_rate > 0.73
ORDER BY variability DESC 
;

EXIT;

