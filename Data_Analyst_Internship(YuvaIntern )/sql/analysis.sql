-- SQLite SQL. Database is built by src/analysis.py.
SELECT COUNT(*) AS records, AVG(target) AS mean_target, AVG(bmi) AS mean_bmi FROM diabetes;
SELECT CASE WHEN bmi < 25 THEN 'below_25' WHEN bmi < 30 THEN '25_to_30' ELSE '30_plus' END AS bmi_group,
COUNT(*) AS records, AVG(target) AS mean_target
FROM diabetes GROUP BY bmi_group;
SELECT bmi, bp, target FROM diabetes ORDER BY target DESC LIMIT 10;
