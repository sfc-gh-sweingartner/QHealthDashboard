-- =====================================================
-- Quantium Healthcare Analytics Demo Platform  
-- IMPROVED Data Quality Validation and Performance Testing
-- Task 1.4: Validate enhanced data with rich dimensions
-- =====================================================

USE DATABASE QUANTIUM_HEALTHCARE_DEMO;
USE SCHEMA QUANTIUM_HEALTHCARE_DEMO;

-- =====================================================
-- ENHANCED PERFORMANCE TESTING QUERIES
-- =====================================================

-- Test 1: Age bucket analysis (should show multiple age categories)
SELECT 
  'Performance Test 1: Enhanced Age Analysis' as test_name,
  CURRENT_TIMESTAMP() as start_time;

SELECT 
  d.age_bucket,
  d.province,
  COUNT(DISTINCT d.entity_no) as unique_patients,
  ROUND(SUM(d.amt_claimed), 2) as total_benefit_paid,
  ROUND(AVG(d.amt_claimed), 2) as avg_per_claim
FROM PHARMACEUTICAL_CLAIMS d
GROUP BY d.age_bucket, d.province
ORDER BY total_benefit_paid DESC;

SELECT 
  'Performance Test 1 Complete' as test_name,
  CURRENT_TIMESTAMP() as end_time;

-- Test 2: Risk category analysis (should show multiple risk levels)
SELECT 
  'Performance Test 2: Risk Category Analysis' as test_name,
  CURRENT_TIMESTAMP() as start_time;

SELECT 
  CASE 
    WHEN c.wf = 1 THEN 'Very Low'
    WHEN c.wf = 3 THEN 'Low'
    WHEN c.wf = 5 THEN 'Medium'
    WHEN c.wf = 8 THEN 'High'
    WHEN c.wf = 10 THEN 'Very High'
    ELSE 'Other'
  END as risk_category,
  c.tr_level_1,
  COUNT(*) as claim_count,
  ROUND(SUM(c.amt_claimed_ty), 2) as total_claimed,
  ROUND(AVG(c.amt_claimed_ty), 2) as avg_per_claim
FROM HEALTHCARE_CLAIMS c
WHERE c.amt_claimed_ty > 500  -- Focus on higher value claims
GROUP BY 
  CASE 
    WHEN c.wf = 1 THEN 'Very Low'
    WHEN c.wf = 3 THEN 'Low'
    WHEN c.wf = 5 THEN 'Medium'
    WHEN c.wf = 8 THEN 'High'
    WHEN c.wf = 10 THEN 'Very High'
    ELSE 'Other'
  END,
  c.tr_level_1
ORDER BY total_claimed DESC
LIMIT 50;

SELECT 
  'Performance Test 2 Complete' as test_name,
  CURRENT_TIMESTAMP() as end_time;

-- Test 3: Provincial variation analysis (should show realistic distribution)
SELECT 
  'Performance Test 3: Provincial Variation' as test_name,
  CURRENT_TIMESTAMP() as start_time;

SELECT 
  d.province,
  COUNT(DISTINCT d.entity_no) as unique_patients,
  COUNT(*) as total_prescriptions,
  ROUND(SUM(d.amt_claimed), 2) as total_cost,
  ROUND(AVG(d.amt_claimed), 2) as avg_cost_per_prescription,
  ROUND(SUM(d.amt_claimed) / COUNT(DISTINCT d.entity_no), 2) as avg_cost_per_patient
FROM PHARMACEUTICAL_CLAIMS d
GROUP BY d.province
ORDER BY total_cost DESC;

SELECT 
  'Performance Test 3 Complete' as test_name,
  CURRENT_TIMESTAMP() as end_time;

-- =====================================================
-- ENHANCED DATA INTEGRITY CHECKS
-- =====================================================

-- Check 1: Age bucket validation
SELECT 'ENHANCED AGE BUCKET VALIDATION' as check_category;

SELECT 
  'Age Bucket Distribution' as check_name,
  age_bucket,
  COUNT(*) as patient_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM DIM_PATIENTS
GROUP BY age_bucket
ORDER BY patient_count DESC;

-- Should show multiple age buckets, not just "Above 18 Yrs"
SELECT 
  'Age Bucket Variety Check' as check_name,
  COUNT(DISTINCT age_bucket) as distinct_age_buckets,
  CASE 
    WHEN COUNT(DISTINCT age_bucket) >= 3 THEN 'PASS - Multiple age buckets found'
    ELSE 'FAIL - Insufficient age bucket variety'
  END as validation_result
FROM DIM_PATIENTS;

-- Check 2: Risk category validation  
SELECT 'RISK CATEGORY VALIDATION' as check_category;

SELECT 
  'Risk Category Distribution' as check_name,
  CASE 
    WHEN wf = 1 THEN 'Very Low'
    WHEN wf = 3 THEN 'Low'
    WHEN wf = 5 THEN 'Medium'
    WHEN wf = 8 THEN 'High'
    WHEN wf = 10 THEN 'Very High'
    ELSE 'Other'
  END as risk_category,
  COUNT(*) as claim_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM HEALTHCARE_CLAIMS
GROUP BY 
  CASE 
    WHEN wf = 1 THEN 'Very Low'
    WHEN wf = 3 THEN 'Low'
    WHEN wf = 5 THEN 'Medium'
    WHEN wf = 8 THEN 'High'
    WHEN wf = 10 THEN 'Very High'
    ELSE 'Other'
  END
ORDER BY claim_count DESC;

-- Should show multiple risk categories
SELECT 
  'Risk Category Variety Check' as check_name,
  COUNT(DISTINCT wf) as distinct_risk_levels,
  CASE 
    WHEN COUNT(DISTINCT wf) >= 4 THEN 'PASS - Multiple risk categories found'
    ELSE 'FAIL - Insufficient risk category variety'
  END as validation_result
FROM HEALTHCARE_CLAIMS;

-- Check 3: Cost tier validation
SELECT 'COST TIER VALIDATION' as check_category;

SELECT 
  'Cost Category Distribution' as check_name,
  cost_category,
  COUNT(*) as patient_count,
  ROUND(AVG(total_benefit_paid), 2) as avg_total_cost,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM PATIENT_COST_CATEGORIES
GROUP BY cost_category
ORDER BY avg_total_cost;

-- Check 4: Provincial distribution validation
SELECT 'PROVINCIAL DISTRIBUTION VALIDATION' as check_category;

SELECT 
  'Provincial Distribution' as check_name,
  province,
  COUNT(*) as patient_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 2) as percentage
FROM DIM_PATIENTS
GROUP BY province
ORDER BY patient_count DESC;

-- Validate that Gauteng and Western Cape have highest populations (realistic)
SELECT 
  'Provincial Distribution Realism Check' as check_name,
  CASE 
    WHEN (SELECT COUNT(*) FROM DIM_PATIENTS WHERE province = 'GAUTENG') = 
         (SELECT MAX(patient_count) FROM (
           SELECT province, COUNT(*) as patient_count 
           FROM DIM_PATIENTS 
           GROUP BY province
         ))
    THEN 'PASS - Gauteng has highest population (realistic)'
    ELSE 'FAIL - Unrealistic provincial distribution'
  END as validation_result;

-- =====================================================
-- FINANCIAL PATTERN VALIDATION
-- =====================================================

-- Check 5: Year-over-year growth patterns
SELECT 'FINANCIAL PATTERN VALIDATION' as check_category;

SELECT 
  'Year-over-Year Growth Pattern' as check_name,
  year,
  COUNT(*) as claim_count,
  ROUND(SUM(amt_claimed), 2) as total_claimed,
  ROUND(AVG(amt_claimed), 2) as avg_claimed,
  LAG(ROUND(AVG(amt_claimed), 2)) OVER (ORDER BY year) as prev_year_avg,
  ROUND(
    (ROUND(AVG(amt_claimed), 2) - LAG(ROUND(AVG(amt_claimed), 2)) OVER (ORDER BY year)) 
    / LAG(ROUND(AVG(amt_claimed), 2)) OVER (ORDER BY year) * 100, 2
  ) as growth_rate_percent
FROM PHARMACEUTICAL_CLAIMS
GROUP BY year
ORDER BY year;

-- Check 6: Seasonal patterns (winter months should be higher)
SELECT 
  'Seasonal Cost Pattern' as check_name,
  EXTRACT(MONTH FROM date_key) as month_no,
  CASE 
    WHEN EXTRACT(MONTH FROM date_key) IN (5, 6, 7, 8) THEN 'Winter'
    ELSE 'Other Seasons'
  END as season,
  COUNT(*) as claim_count,
  ROUND(AVG(amt_claimed), 2) as avg_claimed
FROM PHARMACEUTICAL_CLAIMS
GROUP BY EXTRACT(MONTH FROM date_key), 
  CASE 
    WHEN EXTRACT(MONTH FROM date_key) IN (5, 6, 7, 8) THEN 'Winter'
    ELSE 'Other Seasons'
  END
ORDER BY month_no;

-- =====================================================
-- DASHBOARD-SPECIFIC VALIDATIONS
-- =====================================================

-- Validate data for Patient Distribution by Age chart
SELECT 'DASHBOARD CHART VALIDATIONS' as validation_category;

SELECT 
  'Patient Distribution by Age - Data Availability' as chart_validation,
  dp.age_bucket,
  COUNT(*) as patient_count,
  SUM(pcc.total_benefit_paid) as total_benefits
FROM PATIENT_COST_CATEGORIES pcc
JOIN DIM_PATIENTS dp ON pcc.entity_no = dp.entity_no
GROUP BY dp.age_bucket
ORDER BY patient_count DESC;

-- Validate data for Demographics by Province chart  
SELECT 
  'Demographics by Province - Data Availability' as chart_validation,
  dp.province,
  COUNT(DISTINCT pcc.entity_no) as patients_by_province,
  ROUND(AVG(pcc.total_benefit_paid), 2) as avg_benefit_per_patient
FROM PATIENT_COST_CATEGORIES pcc
JOIN DIM_PATIENTS dp ON pcc.entity_no = dp.entity_no
GROUP BY dp.province
ORDER BY patients_by_province DESC;

-- Validate data for High-Cost Patient Analysis
SELECT 
  'High-Cost Patient Analysis - Data Availability' as chart_validation,
  pcc.cost_category,
  COUNT(*) as patient_count,
  dp.age_groups,
  ROUND(AVG(pcc.total_benefit_paid), 2) as avg_cost_per_patient
FROM PATIENT_COST_CATEGORIES pcc
JOIN DIM_PATIENTS dp ON pcc.entity_no = dp.entity_no
WHERE pcc.cost_category IN ('High Cost', 'Very High Cost')
GROUP BY pcc.cost_category, dp.age_groups
ORDER BY avg_cost_per_patient DESC;

-- Validate data for High-Value Claims by Risk Category  
SELECT 
  'High-Value Claims by Risk Category - Data Availability' as chart_validation,
  risk_category,
  claim_count,
  total_value,
  avg_value_per_claim
FROM HIGH_VALUE_CLAIMS_RISK
ORDER BY total_value DESC;

-- =====================================================
-- SUMMARY STATISTICS FOR IMPROVED DATA
-- =====================================================

SELECT 'IMPROVED DATA SUMMARY' as summary_section;

-- Enhanced dataset statistics
SELECT 
  'Enhanced Dataset Summary' as metric,
  'Q.Dose Pharmaceutical Claims' as dataset,
  COUNT(*) as total_records,
  COUNT(DISTINCT entity_no) as unique_patients,
  COUNT(DISTINCT province) as unique_provinces,
  COUNT(DISTINCT age_bucket) as unique_age_buckets,
  COUNT(DISTINCT age_groups) as unique_age_groups,
  MIN(date_key) as earliest_date,
  MAX(date_key) as latest_date,
  ROUND(SUM(amt_claimed), 2) as total_claimed,
  ROUND(AVG(amt_claimed), 2) as avg_claimed
FROM PHARMACEUTICAL_CLAIMS

UNION ALL

SELECT 
  'Enhanced Dataset Summary',
  'Q.CheckUp Lite Healthcare Claims',
  COUNT(*),
  NULL, -- No patient-level data in CheckUp Lite
  COUNT(DISTINCT p_province),
  NULL,
  NULL,
  MIN(date_key),
  MAX(date_key),
  ROUND(SUM(amt_claimed_ty), 2),
  ROUND(AVG(amt_claimed_ty), 2)
FROM HEALTHCARE_CLAIMS;

-- Risk and cost category summaries
SELECT 
  'Risk and Cost Categories' as metric,
  'Patient Cost Categories' as dataset,
  COUNT(*) as total_patients,
  COUNT(DISTINCT cost_category) as unique_cost_categories,
  NULL as unique_provinces,
  NULL as unique_age_buckets,
  NULL as unique_age_groups,
  NULL as earliest_date,
  NULL as latest_date,
  ROUND(SUM(total_benefit_paid), 2) as total_claimed,
  ROUND(AVG(total_benefit_paid), 2) as avg_claimed
FROM PATIENT_COST_CATEGORIES

UNION ALL

SELECT 
  'Risk and Cost Categories',
  'High-Value Claims Risk',
  SUM(claim_count),
  COUNT(DISTINCT risk_category),
  NULL, NULL, NULL, NULL, NULL,
  ROUND(SUM(total_value), 2),
  ROUND(AVG(avg_value_per_claim), 2)
FROM HIGH_VALUE_CLAIMS_RISK;

-- =====================================================
-- FINAL VALIDATION SUMMARY
-- =====================================================

SELECT 'ENHANCED DATA VALIDATION SUMMARY' as validation_summary;

-- Count distinct values in key dimensions to ensure variety
SELECT 
  'Dimension Variety Summary' as summary_type,
  (SELECT COUNT(DISTINCT age_bucket) FROM DIM_PATIENTS) as distinct_age_buckets,
  (SELECT COUNT(DISTINCT province) FROM DIM_PATIENTS) as distinct_provinces,
  (SELECT COUNT(DISTINCT cost_category) FROM PATIENT_COST_CATEGORIES) as distinct_cost_categories,
  (SELECT COUNT(DISTINCT risk_category) FROM HIGH_VALUE_CLAIMS_RISK) as distinct_risk_categories,
  (SELECT COUNT(DISTINCT tr_level_1) FROM HEALTHCARE_CLAIMS) as distinct_product_categories;

-- Final validation status
SELECT 
  'ENHANCED DATA VALIDATION COMPLETE' as status,
  CURRENT_TIMESTAMP() as completion_time,
  'Enhanced synthetic data with rich dimensions ready for dashboard' as next_steps;