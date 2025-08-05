"""
Optimized SQL queries for Quantium Healthcare Analytics Platform
Focus: <3 second execution times on 1M+ record datasets
"""

# Q.CheckUp Lite Queries (Medical Device Analytics)
CHECKUP_LITE_QUERIES = {
    
    # Overview KPIs
    'overview_kpis': """
        SELECT 
            COUNT(*) as total_claims,
            COUNT(DISTINCT CLAIM_ID) as unique_patients,
            COUNT(DISTINCT PRACTICE_NO_DESCR) as unique_providers,
            SUM(AMT_CLAIMED_TY) as total_claim_amount,
            SUM(AMT_PAID_TY) as total_paid_amount,
            AVG(AMT_CLAIMED_TY) as avg_claim_amount,
            AVG(AMT_PAID_TY) as avg_paid_amount
        FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.HEALTHCARE_CLAIMS
        WHERE DATE_KEY >= CURRENT_DATE - INTERVAL '12 MONTHS'
    """,
    
    # Province Performance
    'province_performance': """
        SELECT 
            PROVINCE_DESCR as province,
            COUNT(*) as total_claims,
            SUM(AMT_CLAIMED_TY) as total_claimed,
            SUM(AMT_PAID_TY) as total_paid,
            AVG(AMT_CLAIMED_TY) as avg_claim_amount,
            COUNT(DISTINCT CLAIM_ID) as unique_patients,
            COUNT(DISTINCT PRACTICE_NO_DESCR) as unique_providers
        FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.HEALTHCARE_CLAIMS
        WHERE DATE_KEY >= CURRENT_DATE - INTERVAL '12 MONTHS'
        GROUP BY PROVINCE_DESCR
        ORDER BY total_claims DESC
    """,
    
    # Provider Analysis
    'provider_analysis': """
        SELECT 
            PRACTICE_NO_DESCR as provider_name,
            CATEGORY_DESCR as provider_category,
            PROVIDER_GROUP as provider_group,
            PROVINCE_DESCR as province,
            COUNT(*) as total_claims,
            SUM(AMT_CLAIMED_TY) as total_claimed,
            SUM(AMT_PAID_TY) as total_paid,
            AVG(AMT_CLAIMED_TY) as avg_claim_amount,
            COUNT(DISTINCT CLAIM_ID) as unique_patients,
            (SUM(AMT_PAID_TY) / NULLIF(SUM(AMT_CLAIMED_TY), 0)) * 100 as approval_rate
        FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.HEALTHCARE_CLAIMS
        WHERE DATE_KEY >= CURRENT_DATE - INTERVAL '12 MONTHS'
        GROUP BY PRACTICE_NO_DESCR, CATEGORY_DESCR, PROVIDER_GROUP, PROVINCE_DESCR
        HAVING COUNT(*) >= 10
        ORDER BY total_claims DESC
        LIMIT 50
    """,
    
    # Product Hierarchy Analysis
    'product_hierarchy': """
        SELECT 
            HIGH_LEVEL_1 as level_1,
            HIGH_LEVEL_2 as level_2,
            HIGH_LEVEL_3 as level_3,
            HIGH_LEVEL_4 as level_4,
            COUNT(*) as total_claims,
            SUM(AMT_CLAIMED_TY) as total_claimed,
            SUM(AMT_PAID_TY) as total_paid,
            AVG(AMT_CLAIMED_TY) as avg_claim_amount
        FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.HEALTHCARE_CLAIMS
        WHERE DATE_KEY >= CURRENT_DATE - INTERVAL '12 MONTHS'
        GROUP BY HIGH_LEVEL_1, HIGH_LEVEL_2, HIGH_LEVEL_3, HIGH_LEVEL_4
        ORDER BY total_claims DESC
    """,
    
    # Monthly Trends
    'monthly_trends': """
        SELECT 
            DATE_TRUNC('month', DATE_KEY) as month,
            COUNT(*) as total_claims,
            SUM(AMT_CLAIMED_TY) as total_claimed,
            SUM(AMT_PAID_TY) as total_paid,
            AVG(AMT_CLAIMED_TY) as avg_claim_amount,
            COUNT(DISTINCT CLAIM_ID) as unique_patients
        FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.HEALTHCARE_CLAIMS
        WHERE DATE_KEY >= CURRENT_DATE - INTERVAL '24 MONTHS'
        GROUP BY DATE_TRUNC('month', DATE_KEY)
        ORDER BY month
    """,
    
    # High-Value Claims Analysis
    'high_value_claims': """
        SELECT 
            CLAIM_ID,
            PRACTICE_NO_DESCR as provider_name,
            PROVINCE_DESCR,
            HIGH_LEVEL_1,
            AMT_CLAIMED_TY as total_claim_amount,
            AMT_PAID_TY as total_paid_amount,
            DATE_KEY,
            CASE 
                WHEN AMT_CLAIMED_TY > 15000 THEN 'Very High'
                WHEN AMT_CLAIMED_TY > 10000 THEN 'High'
                WHEN AMT_CLAIMED_TY > 5000 THEN 'Medium'
                ELSE 'Normal'
            END as risk_category
        FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.HEALTHCARE_CLAIMS
        WHERE AMT_CLAIMED_TY > 5000
        AND DATE_KEY >= CURRENT_DATE - INTERVAL '12 MONTHS'
        ORDER BY AMT_CLAIMED_TY DESC
        LIMIT 100
    """
}

# Q.Dose Queries (Pharmaceutical Analytics)
DOSE_QUERIES = {
    
    # Overview KPIs
    'overview_kpis': """
        SELECT 
            SUM(CLAIMS) as TOTAL_PRESCRIPTIONS,
            COUNT(DISTINCT ENTITY_NO) as UNIQUE_PATIENTS,
            COUNT(DISTINCT PROVIDER) as UNIQUE_PROVIDERS,
            SUM(AMT_PAID) as TOTAL_BENEFIT_PAID,
            SUM(AMT_PAID_MEM) as TOTAL_COPAY,
            SUM(AMT_CLAIMED) as TOTAL_GROSS_COST,
            AVG(AMT_PAID) as AVG_BENEFIT_PAID
        FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.PHARMACEUTICAL_CLAIMS
        WHERE YEAR BETWEEN 2017 AND 2019
    """,
    
    # ATC Hierarchy Analysis
    'atc_hierarchy': """
        SELECT 
            'N/A' as ATC_LEVEL_1_CODE,
            ATC_LEVEL_DESC_1,
            'N/A' as ATC_LEVEL_2_CODE,
            ATC_LEVEL_DESC_2,
            'N/A' as ATC_LEVEL_3_CODE,
            ATC_LEVEL_DESC_3,
            SUM(CLAIMS) as TOTAL_PRESCRIPTIONS,
            SUM(AMT_PAID) as TOTAL_BENEFIT_PAID,
            SUM(AMT_CLAIMED) as TOTAL_GROSS_COST,
            AVG(AMT_PAID) as AVG_BENEFIT_PAID,
            COUNT(DISTINCT ENTITY_NO) as UNIQUE_PATIENTS
        FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.PHARMACEUTICAL_CLAIMS
        WHERE YEAR BETWEEN 2017 AND 2019
        GROUP BY ATC_LEVEL_DESC_1, ATC_LEVEL_DESC_2, ATC_LEVEL_DESC_3
        ORDER BY TOTAL_PRESCRIPTIONS DESC
    """,
    
    # Multiple Sclerosis Analysis
    'ms_analysis': """
        SELECT 
            PRODUCT_NAME,
            NAPPI_MANUFACTURER,
            SUM(CLAIMS) as PRESCRIPTION_COUNT,
            SUM(AMT_PAID) as TOTAL_BENEFIT_PAID,
            SUM(AMT_CLAIMED) as TOTAL_GROSS_COST,
            AVG(AMT_PAID) as AVG_BENEFIT_PAID,
            COUNT(DISTINCT ENTITY_NO) as UNIQUE_PATIENTS,
            PROVIDER_PROVINCE
        FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.PHARMACEUTICAL_CLAIMS
        WHERE ATC_LEVEL_DESC_3 ILIKE '%multiple sclerosis%'
        OR ATC_LEVEL_DESC_4 ILIKE '%multiple sclerosis%'
        OR PRODUCT_NAME ILIKE '%copaxone%'
        OR PRODUCT_NAME ILIKE '%interferon%'
        GROUP BY PRODUCT_NAME, NAPPI_MANUFACTURER, PROVIDER_PROVINCE
        ORDER BY TOTAL_BENEFIT_PAID DESC
    """,
    
    # Patient Demographics Analysis
    'patient_demographics': """
        SELECT 
            AGE_BUCKET,
            GENDER,
            PROVINCE,
            COUNT(DISTINCT ENTITY_NO) as UNIQUE_PATIENTS,
            SUM(CLAIMS) as TOTAL_PRESCRIPTIONS,
            SUM(AMT_PAID) as TOTAL_BENEFIT_PAID,
            AVG(AMT_PAID) as AVG_BENEFIT_PER_PATIENT,
            SUM(AMT_CLAIMED) as TOTAL_GROSS_COST
        FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.PHARMACEUTICAL_CLAIMS
        WHERE YEAR BETWEEN 2017 AND 2019
        GROUP BY AGE_BUCKET, GENDER, PROVINCE
        ORDER BY TOTAL_PRESCRIPTIONS DESC
    """,
    
    # Provider Prescribing Patterns
    'provider_patterns': """
        SELECT 
            PROVIDER as PROVIDER_NAME,
            PROVIDER_TYPE,
            PROVIDER_PROVINCE,
            SUM(CLAIMS) as TOTAL_PRESCRIPTIONS,
            COUNT(DISTINCT ENTITY_NO) as UNIQUE_PATIENTS,
            COUNT(DISTINCT NAPPI9) as UNIQUE_PRODUCTS,
            SUM(AMT_PAID) as TOTAL_BENEFIT_PAID,
            AVG(AMT_PAID) as AVG_PRESCRIPTION_VALUE,
            -- Potential fraud indicators
            MAX(AMT_PAID) as MAX_PRESCRIPTION_VALUE,
            STDDEV(AMT_PAID) as PRESCRIPTION_VALUE_STDDEV
        FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.PHARMACEUTICAL_CLAIMS
        WHERE YEAR BETWEEN 2017 AND 2019
        GROUP BY PROVIDER, PROVIDER_TYPE, PROVIDER_PROVINCE
        HAVING SUM(CLAIMS) >= 50  -- Minimum prescription threshold
        ORDER BY TOTAL_PRESCRIPTIONS DESC
        LIMIT 100
    """,
    
    # Financial Breakdown Analysis
    'financial_breakdown': """
        SELECT 
            YEAR,
            SUM(CLAIMS) as TOTAL_PRESCRIPTIONS,
            SUM(AMT_PAID) as BENEFIT_PAID,
            SUM(AMT_PAID_MEM) as PATIENT_COPAY,
            SUM(AMT_PAID_CEB) as DEDUCTIBLE,
            SUM(AMT_PAID_MSA) as COINSURANCE,
            SUM(AMT_CLAIMED) as GROSS_DRUG_COST,
            SUM(AMT_PAID_ATB) as ALLOWABLE_COST,
            SUM(AMT_PAID_GPN) as INGREDIENT_COST,
            SUM(AMT_PAID_PROV) as DISPENSING_FEE,
            SUM(AMT_PAID_MOB) as SALES_TAX,
            SUM(AMT_PAID_HCC) as INCENTIVE_FEE,
            SUM(AMT_PAID_PMB) as PROFESSIONAL_FEE,
            SUM(AMT_PAID_TP) as OTHER_FEES
        FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.PHARMACEUTICAL_CLAIMS
        WHERE YEAR BETWEEN 2017 AND 2019
        GROUP BY YEAR
        ORDER BY YEAR
    """,
    
    # Yearly Trends
    'yearly_trends': """
        SELECT 
            YEAR,
            MONTH_KEY / 100 as YEAR_EXTRACTED,
            MONTH_KEY % 100 as MONTH_EXTRACTED,
            SUM(CLAIMS) as PRESCRIPTION_COUNT,
            SUM(AMT_PAID) as TOTAL_BENEFIT_PAID,
            AVG(AMT_PAID) as AVG_PRESCRIPTION_VALUE,
            COUNT(DISTINCT ENTITY_NO) as UNIQUE_PATIENTS,
            COUNT(DISTINCT PROVIDER) as UNIQUE_PROVIDERS
        FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.PHARMACEUTICAL_CLAIMS
        WHERE YEAR BETWEEN 2017 AND 2019
        GROUP BY YEAR, MONTH_KEY
        ORDER BY YEAR, MONTH_KEY
    """,
    
    # High-Cost Patients Analysis
    'high_cost_patients': """
        SELECT 
            ENTITY_NO,
            AGE_BUCKET,
            GENDER,
            PROVINCE,
            SUM(CLAIMS) as PRESCRIPTION_COUNT,
            SUM(AMT_PAID) as TOTAL_BENEFIT_PAID,
            SUM(AMT_CLAIMED) as TOTAL_GROSS_COST,
            AVG(AMT_PAID) as AVG_PRESCRIPTION_VALUE,
            LISTAGG(DISTINCT PRODUCT_NAME, ', ') as PRODUCTS_USED,
            -- Risk indicators
            CASE 
                WHEN SUM(AMT_PAID) > 100000 THEN 'Very High Cost'
                WHEN SUM(AMT_PAID) > 50000 THEN 'High Cost'
                WHEN SUM(AMT_PAID) > 25000 THEN 'Medium Cost'
                ELSE 'Normal Cost'
            END as COST_CATEGORY
        FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.PHARMACEUTICAL_CLAIMS
        WHERE YEAR BETWEEN 2017 AND 2019
        GROUP BY ENTITY_NO, AGE_BUCKET, GENDER, PROVINCE
        HAVING SUM(AMT_PAID) > 25000
        ORDER BY TOTAL_BENEFIT_PAID DESC
        LIMIT 100
    """
}

# Performance Monitoring Queries
PERFORMANCE_QUERIES = {
    'table_stats': """
        SELECT 
            'HEALTHCARE_CLAIMS' as table_name,
            COUNT(*) as record_count,
            MIN(DATE_KEY) as min_date,
            MAX(DATE_KEY) as max_date
        FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.HEALTHCARE_CLAIMS
        UNION ALL
        SELECT 
            'PHARMACEUTICAL_CLAIMS' as table_name,
            COUNT(*) as record_count,
            MIN(DATE_KEY) as min_date,
            MAX(DATE_KEY) as max_date
        FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.PHARMACEUTICAL_CLAIMS
        UNION ALL
        SELECT 
            'DIM_PATIENTS' as table_name,
            COUNT(*) as record_count,
            NULL as min_date,
            NULL as max_date
        FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.DIM_PATIENTS
    """,
    
    'query_performance': """
        SELECT 
            query_text,
            execution_time,
            start_time,
            end_time,
            warehouse_name,
            user_name
        FROM TABLE(INFORMATION_SCHEMA.QUERY_HISTORY())
        WHERE start_time >= CURRENT_TIMESTAMP - INTERVAL '1 HOUR'
        AND query_type = 'SELECT'
        ORDER BY execution_time DESC
        LIMIT 20
    """
}

# Utility function to get query by name
def get_query(product: str, query_name: str) -> str:
    """Get a specific query by product and query name"""
    if product.lower() == 'checkup_lite':
        return CHECKUP_LITE_QUERIES.get(query_name, "")
    elif product.lower() == 'dose':
        return DOSE_QUERIES.get(query_name, "")
    elif product.lower() == 'performance':
        return PERFORMANCE_QUERIES.get(query_name, "")
    else:
        return ""

# List available queries for a product
def list_queries(product: str) -> list:
    """List all available queries for a product"""
    if product.lower() == 'checkup_lite':
        return list(CHECKUP_LITE_QUERIES.keys())
    elif product.lower() == 'dose':
        return list(DOSE_QUERIES.keys())
    elif product.lower() == 'performance':
        return list(PERFORMANCE_QUERIES.keys())
    else:
        return []