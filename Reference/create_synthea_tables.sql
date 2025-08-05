-- Synthea Database Table Creation Script
-- This script creates empty tables matching the structure of SYNTHEA.SYNTHEA schema
-- Generated from Snowflake MCP analysis

-- Create database and schema (uncomment if needed)
-- CREATE DATABASE IF NOT EXISTS SYNTHEA;
-- USE DATABASE SYNTHEA;
-- CREATE SCHEMA IF NOT EXISTS SYNTHEA;
-- USE SCHEMA SYNTHEA;

-- 1. PATIENTS Table - Patient demographic data
CREATE OR REPLACE TABLE PATIENTS (
    ID TEXT COMMENT 'Primary Key. Unique Identifier of the patient.',
    BIRTHDATE DATE COMMENT 'The date the patient was born.',
    DEATHDATE DATE COMMENT 'The date the patient died.',
    SSN TEXT COMMENT 'Patient Social Security identifier.',
    DRIVERS TEXT COMMENT 'Patient Drivers License identifier.',
    PASSPORT TEXT COMMENT 'Patient Passport identifier.',
    PREFIX TEXT COMMENT 'Name prefix, such as Mr., Mrs., Dr., etc.',
    FIRST TEXT COMMENT 'First name of the patient.',
    MIDDLE TEXT COMMENT 'Middle name of the patient.',
    LAST TEXT COMMENT 'Last or surname of the patient.',
    SUFFIX TEXT COMMENT 'Name suffix, such as PhD, MD, JD, etc.',
    MAIDEN TEXT COMMENT 'Maiden name of the patient.',
    MARITAL TEXT COMMENT 'Marital Status. M is married, S is single. Currently no support for divorce (D) or widowing (W)',
    RACE TEXT COMMENT 'Description of the patients primary race.',
    ETHNICITY TEXT COMMENT 'Description of the patients primary ethnicity.',
    GENDER TEXT COMMENT 'Gender. M is male, F is female.',
    BIRTHPLACE TEXT COMMENT 'Name of the town where the patient was born.',
    ADDRESS TEXT COMMENT 'Patients street address without commas or newlines.',
    CITY TEXT COMMENT 'Patients address city.',
    STATE TEXT COMMENT 'Patients address state.',
    COUNTY TEXT COMMENT 'Patients address county.',
    FIPS TEXT COMMENT 'Patients FIPS county code.',
    ZIP TEXT COMMENT 'Patients zip code.',
    LAT NUMBER COMMENT 'Latitude of Patients address.',
    LON NUMBER COMMENT 'Longitude of Patients address.',
    HEALTHCARE_EXPENSES NUMBER COMMENT 'The total lifetime cost of healthcare to the patient (i.e. what the patient paid).',
    HEALTHCARE_COVERAGE NUMBER COMMENT 'The total lifetime cost of healthcare services that were covered by Payers (i.e. what the insurance company paid).',
    INCOME NUMBER COMMENT 'Annual income for the Patient'
);

-- 2. ORGANIZATIONS Table - Provider organizations including hospitals
CREATE OR REPLACE TABLE ORGANIZATIONS (
    ID TEXT COMMENT 'Primary key of the Organization.',
    NAME TEXT COMMENT 'Name of the Organization.',
    ADDRESS TEXT COMMENT 'Organizations street address without commas or newlines.',
    CITY TEXT COMMENT 'Street address city.',
    STATE TEXT COMMENT 'Street address state abbreviation.',
    ZIP NUMBER COMMENT 'Street address zip or postal code.',
    LAT NUMBER COMMENT 'Latitude of Organizations address.',
    LON NUMBER COMMENT 'Longitude of Organizations address.',
    PHONE TEXT COMMENT 'Organizations phone number.',
    REVENUE NUMBER COMMENT 'The monetary revenue of the organization during the entire simulation.',
    UTILIZATION NUMBER COMMENT 'The number of Encounters performed by this Organization.'
);

-- 3. PROVIDERS Table - Clinicians that provide patient care
CREATE OR REPLACE TABLE PROVIDERS (
    ID TEXT COMMENT 'Primary key of the Provider/Clinician.',
    ORGANISATION TEXT COMMENT 'Foreign key to the Organization that employees this provider.',
    NAME TEXT COMMENT 'First and last name of the Provider.',
    GENDER TEXT COMMENT 'Gender. M is male, F is female.',
    SPECIALITY TEXT COMMENT 'Provider speciality.',
    ADDRESS TEXT COMMENT 'Providers street address without commas or newlines.',
    CITY TEXT COMMENT 'Street address city.',
    STATE TEXT COMMENT 'Street address state abbreviation.',
    ZIP NUMBER COMMENT 'Street address zip or postal code.',
    LAT NUMBER COMMENT 'Latitude of Providers address.',
    LON NUMBER COMMENT 'Longitude of Providers address.',
    ENCOUNTERS NUMBER COMMENT 'The number of Encounters performed by this provider.',
    PROCEDURES NUMBER COMMENT 'The number of Procedures performed by this provider.'
);

-- 4. PAYERS Table - Payer organization data
CREATE OR REPLACE TABLE PAYERS (
    ID TEXT COMMENT 'Primary key of the Payer (e.g. Insurance).',
    NAME TEXT COMMENT 'Name of the Payer.',
    OWNERSHIP TEXT COMMENT 'null',
    ADDRESS TEXT COMMENT 'Payers street address without commas or newlines.',
    CITY TEXT COMMENT 'Street address city.',
    STATE_HEADQUARTERED TEXT COMMENT 'Street address state abbreviation.',
    ZIP TEXT COMMENT 'Street address zip or postal code.',
    PHONE TEXT COMMENT 'Payers phone number.',
    AMOUNT_COVERED NUMBER COMMENT 'The monetary amount paid to Organizations during the entire simulation.',
    AMOUNT_UNCOVERED NUMBER COMMENT 'The monetary amount not paid to Organizations during the entire simulation, and covered out of pocket by patients.',
    REVENUE NUMBER COMMENT 'The monetary revenue of the Payer during the entire simulation.',
    COVERED_ENCOUNTERS NUMBER COMMENT 'The number of Encounters paid for by this Payer.',
    UNCOVERED_ENCOUNTERS NUMBER COMMENT 'The number of Encounters not paid for by this Payer, and paid out of pocket by patients.',
    COVERED_MEDICATIONS NUMBER COMMENT 'The number of Medications paid for by this Payer.',
    UNCOVERED_MEDICATIONS NUMBER COMMENT 'The number of Medications not paid for by this Payer, and paid out of pocket by patients.',
    COVERED_PROCEDURES NUMBER COMMENT 'The number of Procedures paid for by this Payer.',
    UNCOVERED_PROCEDURES NUMBER COMMENT 'The number of Procedures not paid for by this Payer, and paid out of pocket by patients.',
    COVERED_IMMUNIZATIONS NUMBER COMMENT 'The number of Immunizations paid for by this Payer.',
    UNCOVERED_IMMUNIZATIONS NUMBER COMMENT 'The number of Immunizations not paid for by this Payer, and paid out of pocket by patients.',
    UNIQUE_CUSTOMERS NUMBER COMMENT 'The number of unique patients enrolled with this Payer during the entire simulation.',
    QOLS_AVG NUMBER COMMENT 'The average Quality of Life Scores (QOLS) for all patients enrolled with this Payer during the entire simulation.',
    MEMBER_MONTHS NUMBER COMMENT 'The total number of months that patients were enrolled with this Payer during the simulation and paid monthly premiums (if any).'
);

-- 5. ENCOUNTERS Table - Patient encounter data
CREATE OR REPLACE TABLE ENCOUNTERS (
    ID TEXT COMMENT 'Primary Key. Unique Identifier of the encounter.',
    START_TIME TIMESTAMP_NTZ COMMENT 'The date and time the encounter started.',
    STOP_TIME TIMESTAMP_NTZ COMMENT 'The date and time the encounter concluded.',
    PATIENT TEXT COMMENT 'Foreign key to the Patient.',
    ORGANISATION TEXT COMMENT 'Foreign key to the Organization.',
    PROVIDER TEXT COMMENT 'Foreign key to the Provider.',
    PAYER TEXT COMMENT 'Foreign key to the Payer.',
    ENCOUNTERCLASS TEXT COMMENT 'The class of the encounter, such as ambulatory, emergency, inpatient, wellness, or urgentcare',
    CODE TEXT COMMENT 'Encounter code from SNOMED-CT',
    DESCRIPTION TEXT COMMENT 'Description of the type of encounter.',
    BASE_ENCOUNTER_COST NUMBER COMMENT 'The base cost of the encounter, not including any line item costs related to medications, immunizations, procedures, or other services.',
    TOTAL_CLAIM_COST NUMBER COMMENT 'The total cost of the encounter, including all line items.',
    PAYER_COVERAGE NUMBER COMMENT 'The amount of cost covered by the Payer.',
    REASONCODE TEXT COMMENT 'Diagnosis code from SNOMED-CT, only if this encounter targeted a specific condition.',
    REASONDESCRIPTION TEXT COMMENT 'Description of the reason code.'
);

-- 6. CONDITIONS Table - Patient conditions or diagnoses
CREATE OR REPLACE TABLE CONDITIONS (
    START_TIME DATE COMMENT 'The date the condition was diagnosed.',
    STOP_TIME DATE COMMENT 'The date the condition resolved, if applicable.',
    PATIENT TEXT COMMENT 'Foreign key to the Patient.',
    ENCOUNTER TEXT COMMENT 'Foreign key to the Encounter when the condition was diagnosed.',
    CODE TEXT COMMENT 'Diagnosis code from SNOMED-CT',
    DESCRIPTION TEXT COMMENT 'Description of the condition.',
    SYSTEM TEXT COMMENT 'null'
);

-- 7. OBSERVATIONS Table - Patient observations including vital signs and lab reports
CREATE OR REPLACE TABLE OBSERVATIONS (
    DATE TIMESTAMP_NTZ COMMENT 'The date and time the observation was performed.',
    PATIENT TEXT COMMENT 'Foreign key to the Patient.',
    ENCOUNTER TEXT COMMENT 'Foreign key to the Encounter where the observation was performed.',
    CATEGORY TEXT COMMENT 'Observation category.',
    CODE TEXT COMMENT 'Observation or Lab code from LOINC',
    DESCRIPTION TEXT COMMENT 'Description of the observation or lab.',
    VALUE TEXT COMMENT 'The recorded value of the observation.',
    UNITS TEXT COMMENT 'The units of measure for the value.',
    TYPE TEXT COMMENT 'The datatype of Value: text or numeric'
);

-- 8. PROCEDURES Table - Patient procedure data including surgeries
CREATE OR REPLACE TABLE PROCEDURES (
    START_TIME TIMESTAMP_NTZ COMMENT 'The date and time the procedure was performed.',
    STOP_TIME TIMESTAMP_NTZ COMMENT 'The date and time the procedure was completed, if applicable.',
    PATIENT TEXT COMMENT 'Foreign key to the Patient.',
    ENCOUNTER TEXT COMMENT 'Foreign key to the Encounter where the procedure was performed.',
    CODE TEXT COMMENT 'Procedure code from SNOMED-CT',
    DESCRIPTION TEXT COMMENT 'Description of the procedure.',
    BASE_COST NUMBER COMMENT 'The line item cost of the procedure.',
    REASONCODE NUMBER COMMENT 'Diagnosis code from SNOMED-CT specifying why this procedure was performed.',
    REASONDESCRIPTION TEXT COMMENT 'Description of the reason code.',
    SYSTEM TEXT COMMENT 'null'
);

-- 9. MEDICATIONS Table - Patient medication data
CREATE OR REPLACE TABLE MEDICATIONS (
    START_TIME TIMESTAMP_NTZ COMMENT 'The date and time the medication was prescribed.',
    STOP_TIME TIMESTAMP_NTZ COMMENT 'The date and time the prescription ended, if applicable.',
    PATIENT TEXT COMMENT 'Foreign key to the Patient.',
    PAYER TEXT COMMENT 'Foreign key to the Payer.',
    ENCOUNTER TEXT COMMENT 'Foreign key to the Encounter where the medication was prescribed.',
    CODE TEXT COMMENT 'Medication code from RxNorm.',
    DESCRIPTION TEXT COMMENT 'Description of the medication.',
    BASE_COST NUMBER COMMENT 'The line item cost of the medication.',
    PAYER_COVERAGE NUMBER COMMENT 'The amount covered or reimbursed by the Payer.',
    DISPENSES NUMBER COMMENT 'The number of times the prescription was filled.',
    TOTALCOST NUMBER COMMENT 'The total cost of the prescription, including all dispenses.',
    REASONCODE TEXT COMMENT 'Diagnosis code from SNOMED-CT specifying why this medication was prescribed.',
    REASONDESCRIPTION TEXT COMMENT 'Description of the reason code.'
);

-- 10. IMMUNIZATIONS Table - Patient immunization data
CREATE OR REPLACE TABLE IMMUNIZATIONS (
    DATE TIMESTAMP_NTZ COMMENT 'The date the immunization was administered.',
    PATIENT TEXT COMMENT 'Foreign key to the Patient.',
    ENCOUNTER TEXT COMMENT 'Foreign key to the Encounter where the immunization was administered.',
    CODE TEXT COMMENT 'Immunization code from CVX.',
    DESCRIPTION TEXT COMMENT 'Description of the immunization.',
    BASE_COST NUMBER COMMENT 'The line item cost of the immunization.'
);

-- 11. ALLERGIES Table - Patient allergy data
CREATE OR REPLACE TABLE ALLERGIES (
    START_TIME DATE COMMENT 'The date the allergy was diagnosed.',
    STOP_TIME TEXT COMMENT 'The date the allergy ended, if applicable.',
    PATIENT TEXT COMMENT 'Foreign key to the Patient.',
    ENCOUNTER TEXT COMMENT 'Foreign key to the Encounter when the allergy was diagnosed.',
    CODE TEXT COMMENT 'Allergy code',
    SYSTEM TEXT COMMENT 'Terminology system of the Allergy code. RxNorm if this is a medication allergy, otherwise SNOMED-CT.',
    DESCRIPTION TEXT COMMENT 'Description of the Allergy',
    TYPE TEXT COMMENT 'Identify entry as an allergy or intolerance.',
    CATEGORY TEXT COMMENT 'Identify the category as drug, medication, food, or environment.',
    REACTION1 NUMBER COMMENT 'Optional SNOMED code of the patients reaction.',
    DESCRIPTION1 TEXT COMMENT 'Optional description of the Reaction1 SNOMED code.',
    SEVERITY1 TEXT COMMENT 'Severity of the reaction: MILD, MODERATE, or SEVERE.',
    REACTION2 NUMBER COMMENT 'Optional SNOMED code of the patients second reaction.',
    DESCRIPTION2 TEXT COMMENT 'Optional description of the Reaction2 SNOMED code.',
    SEVERITY2 TEXT COMMENT 'Severity of the second reaction: MILD, MODERATE, or SEVERE.'
);

-- 12. CAREPLANS Table - Patient care plan data, including goals
CREATE OR REPLACE TABLE CAREPLANS (
    ID TEXT COMMENT 'Primary Key. Unique Identifier of the care plan.',
    START_TIME DATE COMMENT 'The date the care plan was initiated.',
    STOP_TIME DATE COMMENT 'The date the care plan ended, if applicable.',
    PATIENT TEXT COMMENT 'Foreign key to the Patient.',
    ENCOUNTER TEXT COMMENT 'Foreign key to the Encounter when the care plan was initiated.',
    CODE TEXT COMMENT 'Code from SNOMED-CT',
    DESCRIPTION TEXT COMMENT 'Description of the care plan.',
    REASONCODE TEXT COMMENT 'Diagnosis code from SNOMED-CT that this care plan addresses.',
    REASONDESCRIPTION TEXT COMMENT 'Description of the reason code.'
);

-- 13. DEVICES Table - Patient-affixed permanent and semi-permanent devices
CREATE OR REPLACE TABLE DEVICES (
    START_TIME TIMESTAMP_NTZ COMMENT 'The date and time the device was associated to the patient.',
    STOP_TIME TIMESTAMP_NTZ COMMENT 'The date and time the device was removed, if applicable.',
    PATIENT TEXT COMMENT 'Foreign key to the Patient.',
    ENCOUNTER TEXT COMMENT 'Foreign key to the Encounter when the device was associated.',
    CODE TEXT COMMENT 'Type of device, from SNOMED-CT',
    DESCRIPTION TEXT COMMENT 'Description of the device.',
    UDI TEXT COMMENT 'Unique Device Identifier for the device.'
);

-- 14. SUPPLIES Table - Supplies used in the provision of care
CREATE OR REPLACE TABLE SUPPLIES (
    DATE DATE COMMENT 'The date the supplies were used.',
    PATIENT TEXT COMMENT 'Foreign key to the Patient.',
    ENCOUNTER TEXT COMMENT 'Foreign key to the Encounter when the supplies were used.',
    CODE TEXT COMMENT 'Code for the type of supply used, from SNOMED-CT',
    DESCRIPTION TEXT COMMENT 'Description of supply used.',
    QUANTITY NUMBER COMMENT 'Quantity of supply used.'
);

-- 15. IMAGING_STUDIES Table - Patient imaging metadata
CREATE OR REPLACE TABLE IMAGING_STUDIES (
    ID TEXT COMMENT 'Non-unique identifier of the imaging study. An imaging study may have multiple rows.',
    DATE TIMESTAMP_NTZ COMMENT 'The date and time the imaging study was conducted.',
    PATIENT TEXT COMMENT 'Foreign key to the Patient.',
    ENCOUNTER TEXT COMMENT 'Foreign key to the Encounter where the imaging study was conducted.',
    SERIES_UID TEXT COMMENT 'Imaging Study series DICOM UID.',
    BODYSITE_CODE NUMBER COMMENT 'A SNOMED Body Structures code describing what part of the body the images in the series were taken of.',
    BODYSITE_DESCRIPTION TEXT COMMENT 'Description of the body site.',
    MODALITY_CODE TEXT COMMENT 'A DICOM-DCM code describing the method used to take the images.',
    MODALITY_DESCRIPTION TEXT COMMENT 'Description of the modality.',
    INSTANCE_UID TEXT COMMENT 'Imaging Study instance DICOM UID.',
    SOP_CODE TEXT COMMENT 'A DICOM-SOP code describing the Subject-Object Pair (SOP) that constitutes the image.',
    SOP_DESCRIPTION TEXT COMMENT 'Description of the SOP code.',
    PROCEDURE_CODE NUMBER COMMENT 'Procedure code from SNOMED-CT.'
);

-- 16. PAYER_TRANSITIONS Table - Payer Transition data (i.e. changes in health insurance)
CREATE OR REPLACE TABLE PAYER_TRANSITIONS (
    PATIENT TEXT COMMENT 'Foreign key to the Patient.',
    MEMBERID TEXT COMMENT 'Member ID for the Insurance Plan.',
    START_DATE TIMESTAMP_NTZ COMMENT 'The date the coverage started.',
    END_DATE TIMESTAMP_NTZ COMMENT 'The date the coverage ended .',
    PAYER TEXT COMMENT 'Foreign key to the Payer.',
    SECONDARY_PAYER TEXT COMMENT 'Foreign key to the Secondary Payer.',
    PLAN_OWNERSHIP TEXT COMMENT 'The owner of the insurance policy. Legal values: Guardian, Self, Spouse.',
    OWNER_NAME TEXT COMMENT 'The name of the insurance policy owner.'
);

-- 17. CLAIMS Table - Patient claim data
CREATE OR REPLACE TABLE CLAIMS (
    ID TEXT COMMENT 'Primary Key. Unique Identifier of the claim.',
    PATIENTID TEXT COMMENT 'Foreign key to the Patient.',
    PROVIDERID TEXT COMMENT 'Foreign key to the Provider.',
    PRIMARYPATIENTINSURANCEID TEXT COMMENT 'Foreign key to the primary Payer.',
    SECONDARYPATIENTINSURANCEID TEXT COMMENT 'Foreign key to the second Payer.',
    DEPARTMENTID NUMBER COMMENT 'Placeholder for department.',
    PATIENTDEPARTMENTID NUMBER COMMENT 'Placeholder for patient department.',
    DIAGNOSIS1 NUMBER COMMENT 'SNOMED-CT code corresponding to a diagnosis related to the claim.',
    DIAGNOSIS2 NUMBER COMMENT 'SNOMED-CT code corresponding to a diagnosis related to the claim.',
    DIAGNOSIS3 NUMBER COMMENT 'SNOMED-CT code corresponding to a diagnosis related to the claim.',
    DIAGNOSIS4 NUMBER COMMENT 'SNOMED-CT code corresponding to a diagnosis related to the claim.',
    DIAGNOSIS5 NUMBER COMMENT 'SNOMED-CT code corresponding to a diagnosis related to the claim.',
    DIAGNOSIS6 NUMBER COMMENT 'SNOMED-CT code corresponding to a diagnosis related to the claim.',
    DIAGNOSIS7 NUMBER COMMENT 'SNOMED-CT code corresponding to a diagnosis related to the claim.',
    DIAGNOSIS8 NUMBER COMMENT 'SNOMED-CT code corresponding to a diagnosis related to the claim.',
    REFERRINGPROVIDERID TEXT COMMENT 'Foreign key to the Provider who made the referral.',
    APPOINTMENTID TEXT COMMENT 'Foreign key to the Encounter.',
    CURRENTILLNESSDATE TIMESTAMP_NTZ COMMENT 'The date the patient experienced symptoms.',
    SERVICEDATE TIMESTAMP_NTZ COMMENT 'The date of the services on the claim.',
    SUPERVISINGPROVIDERID TEXT COMMENT 'Foreign key to the supervising Provider.',
    STATUS1 TEXT COMMENT 'Status of the claim from the Primary Insurance. BILLED or CLOSED.',
    STATUS2 TEXT COMMENT 'Status of the claim from the Secondary Insurance. BILLED or CLOSED.',
    STATUSP TEXT COMMENT 'Status of the claim from the Patient. BILLED or CLOSED.',
    OUTSTANDING1 NUMBER COMMENT 'Total amount of money owed by Primary Insurance.',
    OUTSTANDING2 NUMBER COMMENT 'Total amount of money owed by Secondary Insurance.',
    OUTSTANDINGP NUMBER COMMENT 'Total amount of money owed by Patient.',
    LASTBILLEDDATE1 TIMESTAMP_NTZ COMMENT 'Date the claim was sent to Primary Insurance.',
    LASTBILLEDDATE2 TIMESTAMP_NTZ COMMENT 'Date the claim was sent to Secondary Insurance.',
    LASTBILLEDDATEP TIMESTAMP_NTZ COMMENT 'Date the claim was sent to the Patient.',
    HEALTHCARECLAIMTYPEID1 NUMBER COMMENT 'Type of claim: 1 is professional, 2 is institutional.',
    HEALTHCARECLAIMTYPEID2 NUMBER COMMENT 'Type of claim: 1 is professional, 2 is institutional.'
);

-- 18. CLAIMS_TRANSACTIONS Table - Transactions per line item per claim
CREATE OR REPLACE TABLE CLAIMS_TRANSACTIONS (
    ID TEXT COMMENT 'Primary Key. Unique Identifier of the claim transaction.',
    CLAIMID TEXT COMMENT 'Foreign key to the Claim.',
    CHARGEID NUMBER COMMENT 'Charge ID.',
    PATIENTID TEXT COMMENT 'Foreign key to the Patient.',
    TYPE TEXT COMMENT 'CHARGE: original line item. PAYMENT: payment made against a charge by an insurance company (aka Payer) or patient. ADJUSTMENT: change in the charge without a payment, made by an insurance company. TRANSFERIN and TRANSFEROUT: transfer of the balance from one insurance company to another, or to a patient.',
    AMOUNT NUMBER COMMENT 'Dollar amount for a CHARGE or TRANSFERIN.',
    METHOD TEXT COMMENT 'Payment made by CASH, CHECK, ECHECK, COPAY, SYSTEM (adjustments without payment), or CC (credit card).',
    FROMDATE TIMESTAMP_NTZ COMMENT 'Transaction start date.',
    TODATE TIMESTAMP_NTZ COMMENT 'Transaction end date.',
    PLACEOFSERVICE TEXT COMMENT 'Foreign key to the Organization.',
    PROCEDURECODE NUMBER COMMENT 'SNOMED-CT or other code (e.g. CVX for Vaccines) for the service.',
    MODIFIER1 TEXT COMMENT 'Unused. Modifier on procedure code.',
    MODIFIER2 TEXT COMMENT 'Unused. Modifier on procedure code.',
    DIAGNOSISREF1 NUMBER COMMENT 'Number indicating which diagnosis code from the claim applies to this transaction, 1-8 are valid options.',
    DIAGNOSISREF2 NUMBER COMMENT 'Number indicating which diagnosis code from the claim applies to this transaction, 1-8 are valid options.',
    DIAGNOSISREF3 NUMBER COMMENT 'Number indicating which diagnosis code from the claim applies to this transaction, 1-8 are valid options.',
    DIAGNOSISREF4 NUMBER COMMENT 'Number indicating which diagnosis code from the claim applies to this transaction, 1-8 are valid options.',
    UNITS NUMBER COMMENT 'Number of units of the service.',
    UNITAMOUNT NUMBER COMMENT 'Cost per unit.',
    TRANSFERS NUMBER COMMENT 'Dollar amount of a transfer for a TRANSFERIN or TRANSFEROUT row.',
    OUTSTANDING NUMBER COMMENT 'Dollar amount left unpaid after this transaction was applied.',
    APPOINTMENTID TEXT COMMENT 'Foreign key to the Encounter.',
    LINENOTE TEXT COMMENT 'Note.',
    PATIENTINSURANCEID TEXT COMMENT 'Foreign key to the Payer Transitions table member ID.',
    FEESCHEDULEID NUMBER COMMENT 'Fixed to 1.',
    PROVIDERID TEXT COMMENT 'Foreign key to the Provider.',
    SUPERVISINGPROVIDERID TEXT COMMENT 'Foreign key to the supervising Provider.',
    DEPARTMENTID NUMBER COMMENT 'Placeholder for department.',
    NOTES TEXT COMMENT 'Description of the service or transaction.',
    UNITAMOUNT NUMBER COMMENT 'Cost per unit.',
    TRANSFEROUTID NUMBER COMMENT 'If the transaction is a TRANSFERIN, the Charge ID of the corresponding TRANSFEROUT row.',
    TRANSFERTYPE TEXT COMMENT '1 if transferred to the primary insurance, 2 if transferred to the secondary insurance, or p if transferred to the patient.',
    PAYMENTS NUMBER COMMENT 'Dollar amount of a payment for a PAYMENT row.',
    ADJUSTMENTS NUMBER COMMENT 'Dollar amount of an adjustment for an ADJUSTMENTS row.'
);

-- 19. V_PATIENT_ALLERGIES View - Patient allergies view (Note: This appears to be a view, not a table)
CREATE OR REPLACE VIEW V_PATIENT_ALLERGIES AS
SELECT 
    p.ID,
    p.BIRTHDATE,
    p.DEATHDATE,
    p.SSN,
    p.DRIVERS,
    p.PASSPORT,
    p.PREFIX,
    p.FIRST,
    p.MIDDLE,
    p.LAST,
    p.SUFFIX,
    p.MAIDEN,
    p.MARITAL,
    p.RACE,
    p.ETHNICITY,
    p.GENDER,
    p.BIRTHPLACE,
    p.ADDRESS,
    p.CITY,
    p.STATE,
    p.COUNTY,
    p.FIPS,
    p.ZIP,
    p.LAT,
    p.LON,
    p.HEALTHCARE_EXPENSES,
    p.HEALTHCARE_COVERAGE,
    p.INCOME,
    a.PATIENT,
    a.ENCOUNTER,
    a.CODE,
    a.SYSTEM,
    a.DESCRIPTION,
    a.TYPE,
    a.CATEGORY,
    a.REACTION1,
    a.DESCRIPTION1,
    a.SEVERITY1,
    a.REACTION2,
    a.DESCRIPTION2,
    a.SEVERITY2,
    a.START_TIME
FROM PATIENTS p
LEFT JOIN ALLERGIES a ON p.ID = a.PATIENT;

-- Script completed successfully
-- All 18 tables and 1 view have been created to match the SYNTHEA.SYNTHEA schema structure 