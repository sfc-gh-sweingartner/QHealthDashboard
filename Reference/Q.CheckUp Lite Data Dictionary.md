Q.CheckUp Lite Dataset - Data Dictionary
Dataset Overview
Dataset Name:
Q.CheckUp Lite Healthcare Analytics Data
Purpose:
Healthcare claims and utilization analytics for medical products and services
Data Period:
Monthly healthcare transaction data
Record Type:
Transaction-level records aggregated by product, provider, and location
Total Records:
200 rows (sample dataset)
Total Columns:
24 columns
Column Definitions
Temporal Dimensions
 
Column Name
Data Type
Description
Sample Values
Business Rules
YEAR
Integer
Calendar year of the transaction
2021
Format: YYYY
MONTH_NO
Float
Calendar month number
1.0
Range: 1-12
Product Identification
 
Column Name
DataType
Description
Sample Values
Business Rules
NAPPI9
Integer
9-digit NationalPharmaceutical ProductInterface code
227044001, 454018003
Unique productidentifier in SouthAfrican healthcare
MANUFACTURER
String
Name of the productmanufacturer
"Systagenix WoundManagement (Pty) Ltd","Apex Vision"
Company name asregistered
Provider Information
 
Column Name
DataType
Description
Sample Values
Business Rules
PRACTICE_NO_DESCR
String
Practice or facilityname
"Care At Midstream Sub AcuteFacility", "Dermatologist"
Healthcareprovider identifier
CATEGORY_DESCR
String
Provider category/type
"Hospitals", "Dermatologist","Pharmacy"
13 uniquecategories
PROVIDER_GROUP
String
Provider group ornetwork affiliation
"NHN", "Life Healthcare", "Dis-Chem"
24 uniqueprovider groups
Geographic Dimensions
 
Column Name
DataType
Description
Sample Values
Business Rules
P_PROVINCE
String
Provider provincecode
"Gauteng", "North West", "KwaZulu Natal"
South African provincecodes
PROVINCE_DESCR
String
Full province name
"Gauteng", "Western Cape", "FreeState"
Full provincedescriptions
Product Hierarchy (4-Level Classification)
 
Column Name
DataType
Description
Sample Values
Business Rules
HIGH_LEVEL_1
String
Top-level productcategory with code
"WouM: WoundManagement", "Sut:Sutures"
Format: "CODE: Description"
HIGH_LEVEL_2
String
Second-level productsubcategory
"WouM-SynD: SyntheticDressing"
Format: "PARENT_CODE-CHILD_CODE: Description"
HIGH_LEVEL_3
String
Third-level productspecification
"WouM-SynD-SiliD: SiliconeDressing"
Further refinement of producttype
HIGH_LEVEL_4
String
Fourth-level detailedspecification
"WouM-SynD-SiliD-SiliD:Silicone Dressing"
Most granular productclassification
Simplified Product Hierarchy
 
ColumnName
DataType
Description
Sample Values
Business Rules
TR_LEVEL_1
String
Simplified top-levelcategory
"Wound Management", "Sutures","Syringes"
Clean version withoutcodes
Concatenated Classifications
 
Column Name
DataType
Description
Sample Values
Business Rules
LEVELS_CONCAT_TILL_2
String
Levels 1-2concatenated withpipe separator
"Wound Management | SyntheticDressing"
Format: "Level1 |Level2"
ALL_LEVELS_CONCAT
String
Levels 1-3concatenated
"Wound Management | SyntheticDressing | Silicone Dressing"
Format: "Level1 |Level2 | Level3"
ALL_LEVELS_CONCAT_4
String
All 4 levelsconcatenated
"Wound Management | SyntheticDressing | Silicone Dressing |Silicone Dressing"
Completehierarchy path
Financial Metrics
 
Column Name
DataType
Description
SampleValues
Business Rules
AMT_CLAIMED_TY
Float
Amount claimed this year(current year)
0.00, 12.42,36.57
Currency in South African Rand(ZAR)
AMT_CLAIMED_LY
Float
Amount claimed last year(previous year)
324.72,180.00, 0.00
Currency in South African Rand(ZAR)
AMT_PAID_TY
Float
Amount paid this year(current year)
0.00, 12.42,36.57
May be less than claimed due todeductibles/co-pays
AMT_PAID_LY
Float
Amount paid last year(previous year)
324.72,143.70, 0.00
Actual reimbursement amount
Volume Metrics
 
ColumnName
DataType
Description
SampleValues
Business Rules
UNITS_TY
Float
Number of units dispensed thisyear
0, 23, 2, 1
Physical quantity of products
UNITS_LY
Float
Number of units dispensed lastyear
3, 1, 0, 20
Previous year comparisonvolume
Technical Fields
 
ColumnName
DataType
Description
SampleValues
Business Rules
WF
Integer
Workflow or processingflag
1, 2, 3, 4, 5
Range: 1-11, likely processingsequence
Data Quality Notes
Completeness:
No null values present in sample dataset
Uniqueness:
NAPPI9 codes are mostly unique (185 unique values across 200 records)
Referential Integrity:
Geographic and provider codes appear consistent
Temporal Coverage:
Sample data represents January 2021 (YEAR=2021, MONTH_NO=1)
Business Context
TY/LY Comparison:
"This Year" vs "Last Year" allows for year-over-year analysis
Hierarchical Classification:
4-level product taxonomy enables drill-down analysis
Geographic Analysis:
Province-level geographic breakdown for regional insights
Provider Analysis:
Multiple provider dimensions (category, group, individual practice)
Financial vs Volume:
Separate tracking of monetary and unit volume metrics
Key Relationships
Each record represents a unique combination of: Product (NAPPI9) + Provider + Time Period
Product hierarchy levels are nested (Level 1 → Level 2 → Level 3 → Level 4)
Concatenated fields are derived from individual hierarchy levels
Financial amounts (claimed vs paid) show the relationship between requests and actualreimbursements
Usage Recommendations for Snowflake Implementation
Partitioning:
Consider partitioning by YEAR and MONTH_NO for performance
Indexing:
Create indexes on NAPPI9, P_PROVINCE, and CATEGORY_DESCR for common queries
Data Types:
Use appropriate Snowflake data types (NUMBER for financials, VARCHAR for text)
Hierarchies:
Consider implementing as separate dimension tables for better normalization