-- =====================================================
-- Quantium Healthcare Analytics Demo Platform
-- IMPROVED Synthetic Data Generation - With Rich Variation
-- Task 1.3: Generate realistic transaction data with diverse dimensions
-- =====================================================

USE DATABASE QUANTIUM_HEALTHCARE_DEMO;
USE SCHEMA QUANTIUM_HEALTHCARE_DEMO;

-- =====================================================
-- CLEAN EXISTING DATA FIRST
-- =====================================================

DELETE FROM PHARMACEUTICAL_CLAIMS;
DELETE FROM HEALTHCARE_CLAIMS;
DELETE FROM DIM_PATIENTS;

-- =====================================================
-- ENHANCED DOSE PATIENT DEMOGRAPHICS (Base Population)
-- =====================================================

-- Generate 100,000 unique patients with DIVERSE demographic distribution
INSERT INTO DIM_PATIENTS (ENTITY_NO, AGE_BUCKET, AGE_GROUPS, GENDER, PROVINCE, REGION_OF_RESIDENCE)
WITH patient_generation AS (
  SELECT 
    'PAT_' || LPAD(seq4(), 8, '0') || '_' || 
    SUBSTR(MD5(RANDOM()), 1, 20) AS entity_no,
    seq4() as patient_id,
    UNIFORM(1, 100, RANDOM()) as age_rand,
    UNIFORM(1, 100, RANDOM()) as gender_rand,
    UNIFORM(1, 100, RANDOM()) as province_rand  -- Using weighted distribution
  FROM TABLE(GENERATOR(rowcount => 100000))
),
patient_demographics AS (
  SELECT 
    entity_no,
    -- MULTIPLE AGE BUCKETS for interesting charts
    CASE 
      WHEN age_rand <= 15 THEN 'Under 18 Yrs'
      WHEN age_rand <= 75 THEN 'Above 18 Yrs'  
      WHEN age_rand <= 95 THEN 'Above 65 Yrs'
      ELSE 'Above 80 Yrs'
    END as age_bucket,
    CASE 
      WHEN age_rand <= 8 THEN 'Under 18'
      WHEN age_rand <= 25 THEN 'Between 18-35'
      WHEN age_rand <= 50 THEN 'Between 35-50'
      WHEN age_rand <= 75 THEN 'Between 50-65'
      WHEN age_rand <= 95 THEN 'Between 65-80'
      ELSE 'Greater than 80'
    END as age_groups,
    CASE WHEN gender_rand <= 52 THEN 'F' ELSE 'M' END as gender, -- Slightly more females (realistic)
    -- WEIGHTED PROVINCE DISTRIBUTION (Gauteng & Western Cape more populated)
    CASE 
      WHEN province_rand <= 35 THEN 'GAUTENG'       -- 35% (most populated)
      WHEN province_rand <= 55 THEN 'WESTERN CAPE'  -- 20% 
      WHEN province_rand <= 70 THEN 'KWAZULU-NATAL' -- 15%
      WHEN province_rand <= 80 THEN 'EASTERN CAPE'  -- 10%
      WHEN province_rand <= 86 THEN 'FREE STATE'    -- 6%
      WHEN province_rand <= 91 THEN 'MPUMALANGA'    -- 5%
      WHEN province_rand <= 95 THEN 'LIMPOPO'       -- 4%
      WHEN province_rand <= 98 THEN 'NORTH WEST'    -- 3%
      ELSE 'NORTHERN CAPE'                          -- 2%
    END as province,
    CASE 
      WHEN province_rand <= 35 THEN  -- Gauteng regions
        CASE UNIFORM(1, 5, RANDOM())
          WHEN 1 THEN 'JOHANNESBURG'
          WHEN 2 THEN 'PRETORIA'
          WHEN 3 THEN 'EKURHULENI'
          WHEN 4 THEN 'RANDBURG'
          ELSE 'MIDRAND'
        END
      WHEN province_rand <= 55 THEN  -- Western Cape regions
        CASE UNIFORM(1, 4, RANDOM())
          WHEN 1 THEN 'CAPE TOWN'
          WHEN 2 THEN 'STELLENBOSCH'
          WHEN 3 THEN 'PAARL'
          ELSE 'GEORGE'
        END
      WHEN province_rand <= 70 THEN  -- KwaZulu-Natal regions
        CASE UNIFORM(1, 3, RANDOM())
          WHEN 1 THEN 'DURBAN'
          WHEN 2 THEN 'PIETERMARITZBURG'
          ELSE 'NEWCASTLE'
        END
      ELSE 'OTHER'
    END as region_of_residence
  FROM patient_generation
)
SELECT entity_no, age_bucket, age_groups, gender, province, region_of_residence
FROM patient_demographics;

-- =====================================================
-- Q.DOSE PHARMACEUTICAL CLAIMS WITH RICH VARIATION (1.2M records)
-- =====================================================

INSERT INTO PHARMACEUTICAL_CLAIMS (
    ENTITY_NO, DATE_KEY, YEAR, MONTH_KEY, NAPPI9, PRODUCT_NAME, NAPPI_MANUFACTURER,
    AGE_BUCKET, AGE_GROUPS, GENDER, PROVINCE, REGION_OF_RESIDENCE,
    PLAN_GRP, PLAN_SCHEME, DEG_DESCR, IN_OUT_HOSPITAL_IND, TREATING_DR,
    STRENGTH, SCHEDULE, PACK_SIZE, DOSAGE_FORM,
    ATC_DESCRIPTION, ATC_LEVEL_DESC_1, ATC_LEVEL_DESC_2, ATC_LEVEL_DESC_3, ATC_LEVEL_DESC_4, ATC_LEVEL_DESC_5,
    PROVIDER_TYPE, PROVIDER_GROUP, PROVIDER, PROVIDER_REGION, PROVIDER_PROVINCE,
    BUCKET, TR_PROCEDURE_CODE_DESCRIPTION,
    AMT_PAID_CEB, AMT_PAID_HCC, AMT_PAID_PMB, AMT_PAID_PMB_CHRONIC, AMT_PAID_PROV, AMT_PAID_MEM,
    AMT_PAID, AMT_CLAIMED, QTY, CLAIMS
)
WITH claim_generation AS (
  SELECT 
    seq4() as claim_seq,
    UNIFORM(1, 100000, RANDOM()) as patient_rand,
    -- ENHANCED DATE DISTRIBUTION with year-based volume growth
    CASE 
      WHEN seq4() <= 350000 THEN UNIFORM(1, 365, RANDOM())      -- 2017 (baseline year)
      WHEN seq4() <= 750000 THEN UNIFORM(366, 730, RANDOM())    -- 2018 (growth year)
      ELSE UNIFORM(731, 1095, RANDOM())                         -- 2019 (peak year)
    END as date_rand,
    UNIFORM(1, 18, RANDOM()) as pharma_rand, -- 18 pharmaceutical products
    UNIFORM(1, 26, RANDOM()) as provider_rand,
    UNIFORM(1, 20, RANDOM()) as scheme_rand,
    UNIFORM(50, 5000, RANDOM()) as cost_base, -- REDUCED base cost for better patient cost distribution
    UNIFORM(1, 100, RANDOM()) as pattern_rand   -- For creating realistic patterns
  FROM TABLE(GENERATOR(rowcount => 1200000))
),
claim_details AS (
  SELECT 
    c.claim_seq,
    -- Patient demographics from DIM_PATIENTS
    p.entity_no,
    p.age_bucket,
    p.age_groups,
    p.gender,
    p.province,
    p.region_of_residence,
    
    -- Date calculation with seasonal patterns (more claims in winter)
    DATEADD(day, c.date_rand, '2017-01-01') as date_key,
    EXTRACT(YEAR FROM DATEADD(day, c.date_rand, '2017-01-01')) as year,
    EXTRACT(YEAR FROM DATEADD(day, c.date_rand, '2017-01-01')) * 100 + 
    EXTRACT(MONTH FROM DATEADD(day, c.date_rand, '2017-01-01')) as month_key,
    EXTRACT(MONTH FROM DATEADD(day, c.date_rand, '2017-01-01')) as month_no,
    
    -- Product details from DIM_PHARMACEUTICALS
    ph.nappi9,
    ph.product_name,
    ph.nappi_manufacturer,
    ph.strength,
    ph.schedule,
    ph.pack_size,
    ph.dosage_form,
    
    -- ATC hierarchy from DIM_ATC_HIERARCHY
    atc.atc_description,
    atc.atc_level_desc_1,
    atc.atc_level_desc_2,
    atc.atc_level_desc_3,
    atc.atc_level_desc_4,
    atc.atc_level_desc_5,
    
    -- Provider details from DIM_PROVIDERS
    prov.provider_name as provider,
    prov.provider_group,
    CASE 
      WHEN prov.provider_category = 'Pharmacy' THEN 'Pharmacy'
      WHEN prov.provider_category = 'Hospitals' THEN 'Hospitals'
      ELSE 'Other'
    END as provider_type,
    prov.region as provider_region,
    prov.province as provider_province,
    
    -- Medical scheme details
    ms.scheme_name as plan_scheme,
    ms.plan_group as plan_grp,
    
    -- Clinical details based on ATC codes
    CASE 
      WHEN atc.atc_description IN ('FINGOLIMOD', 'GLATIRAMER ACETATE') THEN 'NEU040 - Multiple sclerosis'
      WHEN atc.atc_description IN ('ENALAPRIL', 'BISOPROLOL', 'FUROSEMIDE') THEN 'CAR001 - Cardiovascular disease'
      WHEN atc.atc_description IN ('ALPRAZOLAM', 'ESCITALOPRAM', 'MORPHINE') THEN 'PSY001 - Mental health'
      WHEN atc.atc_description = 'METFORMIN' THEN 'END001 - Diabetes mellitus'
      ELSE 'GEN001 - General medicine'
    END as deg_descr,
    
    -- Treatment setting
    CASE WHEN prov.provider_category = 'Hospitals' THEN 1 ELSE 0 END as in_out_hospital_ind,
    
    -- Treating doctor specialty
    CASE 
      WHEN atc.atc_description IN ('FINGOLIMOD', 'GLATIRAMER ACETATE') THEN 'Neurologist'
      WHEN atc.atc_description IN ('ENALAPRIL', 'BISOPROLOL', 'FUROSEMIDE') THEN 'Cardiologist'
      WHEN atc.atc_description IN ('ALPRAZOLAM', 'ESCITALOPRAM') THEN 'Psychiatrist'
      WHEN atc.atc_description = 'MORPHINE' THEN 'Oncologist'
      ELSE 'General Practitioner'
    END as treating_dr,
    
    -- Financial calculations with seasonal multipliers
    c.cost_base,
    c.pattern_rand,
    
    -- Quantity with realistic patterns
    CASE 
      WHEN ph.dosage_form = 'INJ' THEN UNIFORM(1, 4, RANDOM()) -- Injections: 1-4 units
      WHEN ph.dosage_form = 'INH' THEN 1 -- Inhalers: typically 1
      WHEN ph.pack_size <= 14 THEN 1 -- Small packs: 1 pack
      WHEN ph.pack_size <= 30 THEN UNIFORM(1, 2, RANDOM()) -- Monthly packs: 1-2
      ELSE UNIFORM(1, 3, RANDOM()) -- Larger packs: 1-3
    END as qty
    
  FROM claim_generation c
  JOIN (SELECT entity_no, age_bucket, age_groups, gender, province, region_of_residence, 
               ROW_NUMBER() OVER (ORDER BY entity_no) as rn 
        FROM DIM_PATIENTS) p 
    ON (c.patient_rand % 100000) + 1 = p.rn
  JOIN (SELECT *, ROW_NUMBER() OVER (ORDER BY nappi9) as rn 
        FROM DIM_PHARMACEUTICALS) ph 
    ON (c.pharma_rand % 18) + 1 = ph.rn
  JOIN DIM_ATC_HIERARCHY atc ON ph.atc_code = atc.atc_code
  JOIN (SELECT *, ROW_NUMBER() OVER (ORDER BY provider_id) as rn 
        FROM DIM_PROVIDERS) prov 
    ON (c.provider_rand % 26) + 1 = prov.rn
  JOIN (SELECT *, ROW_NUMBER() OVER (ORDER BY scheme_id) as rn 
        FROM DIM_MEDICAL_SCHEMES) ms 
    ON (c.scheme_rand % 20) + 1 = ms.rn
),
final_claims AS (
  SELECT 
    entity_no, date_key, year, month_key, nappi9, product_name, nappi_manufacturer,
    age_bucket, age_groups, gender, province, region_of_residence,
    plan_grp, plan_scheme, deg_descr, in_out_hospital_ind, treating_dr,
    strength, schedule, pack_size, dosage_form,
    atc_description, atc_level_desc_1, atc_level_desc_2, atc_level_desc_3, atc_level_desc_4, atc_level_desc_5,
    provider_type, provider_group, provider, provider_region, provider_province,
    'NA' as bucket,
    CASE 
      WHEN dosage_form = 'INJ' THEN 'Intravenous infusion of pharmaceutical preparation'
      WHEN in_out_hospital_ind = 1 THEN 'Medical Per Diem'
      ELSE 'NA'
    END as tr_procedure_code_description,
    
    -- BALANCED FINANCIAL CALCULATIONS for better cost distribution
    ROUND(cost_base * qty * 
      CASE 
        -- MS drugs - reduced to create more medium/high cost patients
        WHEN atc_description IN ('FINGOLIMOD', 'GLATIRAMER ACETATE') THEN UNIFORM(80, 200, RANDOM())
        -- Other chronic medications - moderate range
        WHEN atc_description IN ('ESCITALOPRAM', 'MORPHINE') THEN UNIFORM(25, 80, RANDOM())
        -- Standard chronic medications - lower range
        WHEN atc_description IN ('ENALAPRIL', 'BISOPROLOL', 'METFORMIN') THEN UNIFORM(5, 25, RANDOM())
        -- General medications - lowest range
        ELSE UNIFORM(8, 40, RANDOM())
      END * 
      -- Year-over-year growth (2017: baseline, 2018: +5%, 2019: +8%)
      CASE year
        WHEN 2017 THEN 1.0
        WHEN 2018 THEN 1.05
        WHEN 2019 THEN 1.08
        ELSE 1.0
      END *
      -- Seasonal patterns (winter months cost more due to more illness)
      CASE month_no
        WHEN 5 THEN 1.2  -- May (flu season start)
        WHEN 6 THEN 1.3  -- June (winter)
        WHEN 7 THEN 1.3  -- July (winter)
        WHEN 8 THEN 1.2  -- August (late winter)
        ELSE 1.0
      END / 100.0, 2) as amt_claimed,
    
    qty,
    1 as claims
  FROM claim_details
)
SELECT 
  entity_no, date_key, year, month_key, nappi9, product_name, nappi_manufacturer,
  age_bucket, age_groups, gender, province, region_of_residence,
  plan_grp, plan_scheme, deg_descr, in_out_hospital_ind, treating_dr,
  strength, schedule, pack_size, dosage_form,
  atc_description, atc_level_desc_1, atc_level_desc_2, atc_level_desc_3, atc_level_desc_4, atc_level_desc_5,
  provider_type, provider_group, provider, provider_region, provider_province,
  bucket, tr_procedure_code_description,
  
      -- ENHANCED Financial breakdown with VARIED PATIENT COPAYS
  CASE WHEN deg_descr LIKE '%Multiple sclerosis%' THEN ROUND(amt_claimed * 0.15, 2) ELSE 0 END as amt_paid_ceb,
  CASE WHEN in_out_hospital_ind = 1 THEN ROUND(amt_claimed * 0.4, 2) ELSE 0 END as amt_paid_hcc,
  ROUND(amt_claimed * 0.65, 2) as amt_paid_pmb,
  CASE WHEN deg_descr NOT LIKE '%General%' THEN ROUND(amt_claimed * 0.65, 2) ELSE 0 END as amt_paid_pmb_chronic,
  ROUND(amt_claimed * 0.85, 2) as amt_paid_prov,
  
  -- BALANCED patient copay (AMT_PAID_MEM) for dashboard chart
  ROUND(amt_claimed * 
    CASE 
      -- Moderate copays for expensive MS drugs (8-18%)
      WHEN atc_description IN ('FINGOLIMOD', 'GLATIRAMER ACETATE') THEN UNIFORM(8, 18, RANDOM()) / 100.0
      -- Standard copays for other chronic meds (4-12%)
      WHEN deg_descr NOT LIKE '%General%' THEN UNIFORM(4, 12, RANDOM()) / 100.0
      -- Low copays for general meds (1-6%)
      ELSE UNIFORM(1, 6, RANDOM()) / 100.0
    END *
    -- Year-based copay trend (increasing over time)
    CASE year
      WHEN 2017 THEN 1.0
      WHEN 2018 THEN 1.1  -- 10% increase
      WHEN 2019 THEN 1.25 -- 25% increase from baseline
      ELSE 1.0
    END, 2) as amt_paid_mem,
  
  ROUND(amt_claimed * 0.85, 2) as amt_paid, -- Total paid (85% of claimed for cost control)
  amt_claimed,
  qty,
  claims
FROM final_claims;

-- =====================================================
-- Q.CHECKUP_LITE HEALTHCARE CLAIMS WITH RISK CATEGORIES (1.1M records)
-- =====================================================

INSERT INTO HEALTHCARE_CLAIMS (
    YEAR, MONTH_NO, DATE_KEY, NAPPI9, MANUFACTURER,
    PRACTICE_NO_DESCR, CATEGORY_DESCR, PROVIDER_GROUP,
    P_PROVINCE, PROVINCE_DESCR,
    HIGH_LEVEL_1, HIGH_LEVEL_2, HIGH_LEVEL_3, HIGH_LEVEL_4, TR_LEVEL_1,
    LEVELS_CONCAT_TILL_2, ALL_LEVELS_CONCAT, ALL_LEVELS_CONCAT_4,
    AMT_CLAIMED_TY, AMT_CLAIMED_LY, AMT_PAID_TY, AMT_PAID_LY,
    UNITS_TY, UNITS_LY, WF
)
WITH checkup_generation AS (
  SELECT 
    seq4() as claim_seq,
    UNIFORM(1, 365, RANDOM()) as date_rand, -- Current year dates
    UNIFORM(1, 18, RANDOM()) as product_rand, -- 18 medical products
    UNIFORM(1, 26, RANDOM()) as provider_rand,
    UNIFORM(20, 500, RANDOM()) as cost_base, -- MUCH LOWER base costs for better distribution
    UNIFORM(1, 100, RANDOM()) as risk_rand     -- For risk categorization
  FROM TABLE(GENERATOR(rowcount => 1100000))
),
checkup_details AS (
  SELECT 
    c.claim_seq,
    
    -- Current year (2024) and last year data
    2024 as year,
    EXTRACT(MONTH FROM DATEADD(day, c.date_rand, '2024-01-01')) as month_no,
    DATEADD(day, c.date_rand, '2024-01-01') as date_key,
    
    -- Product details from DIM_PRODUCTS
    p.nappi9,
    p.manufacturer,
    p.high_level_1,
    p.high_level_2,
    p.high_level_3,
    p.high_level_4,
    p.tr_level_1,
    p.levels_concat_till_2,
    p.all_levels_concat,
    p.all_levels_concat_4,
    
    -- Provider details
    prov.provider_name as practice_no_descr,
    prov.provider_category as category_descr,
    prov.provider_group,
    prov.province as p_province,
    prov.province as province_descr,
    
    -- Cost calculations with risk factors
    c.cost_base,
    c.risk_rand,
    
    -- DIVERSE UNITS based on product type and risk
    CASE 
      WHEN p.tr_level_1 = 'Wound Management' THEN UNIFORM(1, 15, RANDOM())
      WHEN p.tr_level_1 = 'Sutures' THEN UNIFORM(1, 8, RANDOM())
      WHEN p.tr_level_1 = 'Syringes' THEN UNIFORM(5, 100, RANDOM())
      WHEN p.tr_level_1 = 'Diagnostics' THEN UNIFORM(1, 5, RANDOM())
      WHEN p.tr_level_1 = 'Surgical Instruments' THEN UNIFORM(1, 3, RANDOM())
      WHEN p.tr_level_1 = 'Orthopedics' THEN 1
      ELSE UNIFORM(1, 10, RANDOM())
    END as units_ty,
    
    -- Workflow flag with patterns
    CASE 
      WHEN c.risk_rand <= 10 THEN 1  -- Very Low risk
      WHEN c.risk_rand <= 30 THEN 3  -- Low risk  
      WHEN c.risk_rand <= 60 THEN 5  -- Medium risk
      WHEN c.risk_rand <= 85 THEN 8  -- High risk
      ELSE 10                        -- Very High risk
    END as wf
    
  FROM checkup_generation c
  JOIN (SELECT *, ROW_NUMBER() OVER (ORDER BY nappi9) as rn 
        FROM DIM_PRODUCTS) p 
    ON (c.product_rand % 18) + 1 = p.rn
  JOIN (SELECT *, ROW_NUMBER() OVER (ORDER BY provider_id) as rn 
        FROM DIM_PROVIDERS) prov 
    ON (c.provider_rand % 26) + 1 = prov.rn
),
final_checkup_claims AS (
  SELECT 
    year, month_no, date_key, nappi9, manufacturer,
    practice_no_descr, category_descr, provider_group,
    p_province, province_descr,
    high_level_1, high_level_2, high_level_3, high_level_4, tr_level_1,
    levels_concat_till_2, all_levels_concat, all_levels_concat_4,
    
    -- BALANCED FINANCIAL CALCULATIONS for proper dashboard distribution
    -- Dashboard expects: >15K=Very High, >10K=High, >5K=Medium for risk categories
    ROUND(cost_base * units_ty * 
      CASE 
        -- Risk-based multipliers designed specifically for dashboard thresholds
        WHEN wf = 1 THEN UNIFORM(0.8, 2.0, RANDOM())   -- Very Low: R400-R2K range (below 5K)
        WHEN wf = 3 THEN UNIFORM(2.0, 4.0, RANDOM())   -- Low: R2K-R4K range (below 5K)
        WHEN wf = 5 THEN UNIFORM(4.0, 8.0, RANDOM())   -- Medium: R4K-R8K range (5K-10K bracket)
        WHEN wf = 8 THEN UNIFORM(8.0, 15.0, RANDOM())  -- High: R8K-R15K range (10K-15K bracket)
        WHEN wf = 10 THEN UNIFORM(15.0, 25.0, RANDOM()) -- Very High: R15K-R25K range (>15K bracket)
        ELSE 1.0
      END, 2) as amt_claimed_ty,
    
    units_ty,
    
    -- Last year data with realistic patterns (some growth, some decline)
    ROUND(UNIFORM(0.6, 1.4, RANDOM()) * units_ty, 0) as units_ly,
    wf
  FROM checkup_details
)
SELECT 
  year, month_no, date_key, nappi9, manufacturer,
  practice_no_descr, category_descr, provider_group,
  p_province, province_descr,
  high_level_1, high_level_2, high_level_3, high_level_4, tr_level_1,
  levels_concat_till_2, all_levels_concat, all_levels_concat_4,
  
  amt_claimed_ty,
  -- Last year claimed with realistic variance
  ROUND(amt_claimed_ty * (units_ly::FLOAT / NULLIF(units_ty, 0)) * UNIFORM(0.8, 1.2, RANDOM()), 2) as amt_claimed_ly,
  
  -- Paid amounts (typically 88-95% of claimed, varies by risk)
  ROUND(amt_claimed_ty * 
    CASE 
      WHEN wf >= 8 THEN UNIFORM(0.88, 0.92, RANDOM()) -- Lower payout for high risk
      ELSE UNIFORM(0.92, 0.96, RANDOM()) -- Higher payout for low risk
    END, 2) as amt_paid_ty,
  ROUND(amt_claimed_ty * (units_ly::FLOAT / NULLIF(units_ty, 0)) * UNIFORM(0.85, 0.95, RANDOM()), 2) as amt_paid_ly,
  
  units_ty,
  units_ly,
  wf
FROM final_checkup_claims;

-- =====================================================
-- CREATE ADDITIONAL ANALYSIS TABLES FOR DASHBOARD
-- =====================================================

-- ENHANCED Patient Cost Categories aligned with dashboard query thresholds
CREATE OR REPLACE TABLE PATIENT_COST_CATEGORIES AS
WITH patient_costs AS (
  SELECT 
    entity_no,
    province,
    age_groups,
    SUM(amt_paid) as total_benefit_paid,  -- Use amt_paid to match dashboard query
    COUNT(*) as prescription_count
  FROM PHARMACEUTICAL_CLAIMS
  GROUP BY entity_no, province, age_groups
)
SELECT 
  entity_no,
  province,
  age_groups,
  total_benefit_paid,
  prescription_count,
  -- MATCH DASHBOARD THRESHOLDS: >100K=Very High, >50K=High, >25K=Medium, else=Low
  CASE 
    WHEN total_benefit_paid > 100000 THEN 'Very High Cost'
    WHEN total_benefit_paid > 50000 THEN 'High Cost'
    WHEN total_benefit_paid > 25000 THEN 'Medium Cost'
    WHEN total_benefit_paid > 10000 THEN 'Low Cost'
    ELSE 'Very Low Cost'
  END as cost_category
FROM patient_costs;

-- High-Value Claims Risk Categories Table
CREATE OR REPLACE TABLE HIGH_VALUE_CLAIMS_RISK AS
WITH claim_risk_analysis AS (
  SELECT 
    claim_id,
    amt_claimed_ty,
    tr_level_1,
    category_descr,
    wf,
    CASE 
      WHEN wf = 1 THEN 'Very Low'
      WHEN wf = 3 THEN 'Low'
      WHEN wf = 5 THEN 'Medium'
      WHEN wf = 8 THEN 'High' 
      WHEN wf = 10 THEN 'Very High'
      ELSE 'Medium'
    END as risk_category
  FROM HEALTHCARE_CLAIMS
  WHERE amt_claimed_ty > 1000  -- High-value threshold
)
SELECT 
  risk_category,
  COUNT(*) as claim_count,
  ROUND(SUM(amt_claimed_ty), 2) as total_value,
  ROUND(AVG(amt_claimed_ty), 2) as avg_value_per_claim
FROM claim_risk_analysis
GROUP BY risk_category;

-- =====================================================
-- DATA VALIDATION AND SUMMARY STATISTICS
-- =====================================================

-- Check record counts
SELECT 'IMPROVED Q.Dose Claims' as dataset, COUNT(*) as record_count 
FROM PHARMACEUTICAL_CLAIMS
UNION ALL
SELECT 'IMPROVED Q.CheckUp Lite Claims', COUNT(*) 
FROM HEALTHCARE_CLAIMS
UNION ALL
SELECT 'IMPROVED Patient Demographics', COUNT(*) 
FROM DIM_PATIENTS
UNION ALL
SELECT 'Patient Cost Categories', COUNT(*)
FROM PATIENT_COST_CATEGORIES
UNION ALL
SELECT 'High-Value Claims Risk', COUNT(*)
FROM HIGH_VALUE_CLAIMS_RISK;

-- Verify age bucket distribution
SELECT 
  'Age Bucket Distribution' as analysis,
  age_bucket,
  COUNT(*) as patient_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) as percentage
FROM DIM_PATIENTS
GROUP BY age_bucket
ORDER BY patient_count DESC;

-- Verify province distribution  
SELECT 
  'Province Distribution' as analysis,
  province,
  COUNT(*) as patient_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) as percentage
FROM DIM_PATIENTS
GROUP BY province
ORDER BY patient_count DESC;

-- Verify cost category distribution
SELECT 
  'Cost Category Distribution' as analysis,
  cost_category,
  COUNT(*) as patient_count,
  ROUND(AVG(total_benefit_paid), 2) as avg_cost_per_patient
FROM PATIENT_COST_CATEGORIES
GROUP BY cost_category
ORDER BY avg_cost_per_patient;

-- Verify risk category distribution  
SELECT 
  'Risk Category Distribution' as analysis,
  risk_category,
  claim_count,
  ROUND(claim_count * 100.0 / SUM(claim_count) OVER (), 1) as percentage
FROM HIGH_VALUE_CLAIMS_RISK
ORDER BY avg_value_per_claim DESC;

-- =====================================================
-- VALIDATION: TEST IMPROVED CHART DISTRIBUTIONS
-- =====================================================

-- Test 1: Risk Category Distribution (should be balanced)
SELECT 
  'RISK CATEGORY VALIDATION' as test_name,
  CASE 
    WHEN AMT_CLAIMED_TY > 15000 THEN 'Very High'
    WHEN AMT_CLAIMED_TY > 10000 THEN 'High'
    WHEN AMT_CLAIMED_TY > 5000 THEN 'Medium'
    ELSE 'Normal'
  END as risk_category,
  COUNT(*) as claim_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) as percentage,
  ROUND(AVG(AMT_CLAIMED_TY), 2) as avg_amount
FROM HEALTHCARE_CLAIMS
WHERE AMT_CLAIMED_TY > 5000
GROUP BY 
  CASE 
    WHEN AMT_CLAIMED_TY > 15000 THEN 'Very High'
    WHEN AMT_CLAIMED_TY > 10000 THEN 'High'
    WHEN AMT_CLAIMED_TY > 5000 THEN 'Medium'
    ELSE 'Normal'
  END
ORDER BY claim_count DESC;

-- Test 2: High-Cost Patient Distribution (should be balanced)
WITH patient_totals AS (
  SELECT 
    ENTITY_NO,
    SUM(AMT_PAID) as total_paid
  FROM PHARMACEUTICAL_CLAIMS
  WHERE YEAR BETWEEN 2017 AND 2019
  GROUP BY ENTITY_NO
  HAVING SUM(AMT_PAID) > 25000
)
SELECT 
  'HIGH-COST PATIENT VALIDATION' as test_name,
  CASE 
    WHEN total_paid > 100000 THEN 'Very High Cost'
    WHEN total_paid > 50000 THEN 'High Cost'
    WHEN total_paid > 25000 THEN 'Medium Cost'
    ELSE 'Normal Cost'
  END as cost_category,
  COUNT(*) as patient_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) as percentage,
  ROUND(AVG(total_paid), 2) as avg_cost
FROM patient_totals
GROUP BY 
  CASE 
    WHEN total_paid > 100000 THEN 'Very High Cost'
    WHEN total_paid > 50000 THEN 'High Cost'
    WHEN total_paid > 25000 THEN 'Medium Cost'
    ELSE 'Normal Cost'
  END
ORDER BY patient_count DESC;

-- Test 3: Patient Copay Trends (should show growth over years)
SELECT 
  'PATIENT COPAY VALIDATION' as test_name,
  YEAR,
  COUNT(*) as prescriptions,
  ROUND(SUM(AMT_PAID_MEM), 2) as total_copay,
  ROUND(AVG(AMT_PAID_MEM), 2) as avg_copay_per_prescription,
  ROUND(SUM(AMT_PAID_MEM) / SUM(AMT_CLAIMED) * 100, 1) as copay_percentage
FROM PHARMACEUTICAL_CLAIMS
WHERE YEAR BETWEEN 2017 AND 2019
GROUP BY YEAR
ORDER BY YEAR;

SELECT 'IMPROVED SYNTHETIC DATA GENERATION COMPLETE' as status;
SELECT 'Charts should now show balanced distributions across all categories!' as result;