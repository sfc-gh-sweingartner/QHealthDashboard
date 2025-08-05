-- =====================================================
-- Quantium Healthcare Analytics Demo Platform
-- Reference Data Population
-- Task 1.2: Realistic Data Generation - Core Dimensions
-- =====================================================

USE DATABASE QUANTIUM_HEALTHCARE_DEMO;

-- =====================================================
-- GEOGRAPHY REFERENCE DATA
-- =====================================================
USE SCHEMA QUANTIUM_HEALTHCARE_DEMO;

INSERT INTO DIM_GEOGRAPHY (PROVINCE, REGION, COUNTRY) VALUES
-- South African Provinces and Major Cities
('Gauteng', 'Johannesburg', 'ZA'),
('Gauteng', 'Pretoria', 'ZA'),
('Gauteng', 'Ekurhuleni', 'ZA'),
('Gauteng', 'Randburg', 'ZA'),
('Gauteng', 'Midrand', 'ZA'),
('Western Cape', 'Cape Town', 'ZA'),
('Western Cape', 'Stellenbosch', 'ZA'),
('Western Cape', 'Paarl', 'ZA'),
('Western Cape', 'George', 'ZA'),
('KwaZulu-Natal', 'Durban', 'ZA'),
('KwaZulu-Natal', 'Pietermaritzburg', 'ZA'),
('KwaZulu-Natal', 'Newcastle', 'ZA'),
('Eastern Cape', 'Port Elizabeth', 'ZA'),
('Eastern Cape', 'East London', 'ZA'),
('Eastern Cape', 'Grahamstown', 'ZA'),
('Free State', 'Bloemfontein', 'ZA'),
('Free State', 'Welkom', 'ZA'),
('Mpumalanga', 'Nelspruit', 'ZA'),
('Mpumalanga', 'Witbank', 'ZA'),
('Limpopo', 'Polokwane', 'ZA'),
('Limpopo', 'Thohoyandou', 'ZA'),
('North West', 'Rustenburg', 'ZA'),
('North West', 'Mahikeng', 'ZA'),
('Northern Cape', 'Kimberley', 'ZA'),
('Northern Cape', 'Upington', 'ZA');

-- =====================================================
-- MEDICAL SCHEMES REFERENCE DATA
-- =====================================================

INSERT INTO DIM_MEDICAL_SCHEMES (SCHEME_NAME, PLAN_GROUP, PLAN_TYPE) VALUES
-- Major South African Medical Schemes
('Discovery Health Medical Scheme', 'Comprehensive', 'Executive'),
('Discovery Health Medical Scheme', 'Comprehensive', 'Classic'),
('Discovery Health Medical Scheme', 'Savings', 'Saver'),
('Discovery Health Medical Scheme', 'Priority', 'Smart'),
('Bonitas Medical Fund', 'Comprehensive', 'Standard'),
('Bonitas Medical Fund', 'Hospital', 'Select'),
('Bonitas Medical Fund', 'Primary', 'Primary'),
('Momentum Health', 'Comprehensive', 'Custom'),
('Momentum Health', 'Ingwe', 'Ingwe'),
('Anglo Medical Scheme', 'Comprehensive', 'Option 1'),
('Anglo Medical Scheme', 'Comprehensive', 'Option 2'),
('Medshield Medical Scheme', 'MediCore', 'MediCore'),
('Medshield Medical Scheme', 'MediElite', 'MediElite'),
('Gems Medical Scheme', 'Onyx', 'Onyx'),
('Gems Medical Scheme', 'Ruby', 'Ruby'),
('Gems Medical Scheme', 'Emerald', 'Emerald'),
('Fedhealth Medical Scheme', 'Comprehensive', 'maxima EXEC'),
('Fedhealth Medical Scheme', 'Savings', 'maxima SAVE'),
('Profmed Medical Scheme', 'Comprehensive', 'Comp Plus'),
('Profmed Medical Scheme', 'Hospital', 'Pinnacle');

-- =====================================================
-- PROVIDERS REFERENCE DATA
-- =====================================================

INSERT INTO DIM_PROVIDERS (PROVIDER_NAME, PROVIDER_GROUP, PROVIDER_CATEGORY, PROVIDER_TYPE, PROVINCE, REGION) VALUES
-- Hospital Groups
('Life Fourways Hospital', 'Life Healthcare', 'Hospitals', 'Hospital', 'Gauteng', 'Johannesburg'),
('Life Groenkloof Hospital', 'Life Healthcare', 'Hospitals', 'Hospital', 'Gauteng', 'Pretoria'),
('Life Vincent Pallotti Hospital', 'Life Healthcare', 'Hospitals', 'Hospital', 'Western Cape', 'Cape Town'),
('Netcare Milpark Hospital', 'Netcare', 'Hospitals', 'Hospital', 'Gauteng', 'Johannesburg'),
('Netcare Christiaan Barnard Memorial Hospital', 'Netcare', 'Hospitals', 'Hospital', 'Western Cape', 'Cape Town'),
('Netcare St Augustine''s Hospital', 'Netcare', 'Hospitals', 'Hospital', 'KwaZulu-Natal', 'Durban'),
('Mediclinic Sandton', 'Mediclinic', 'Hospitals', 'Hospital', 'Gauteng', 'Johannesburg'),
('Mediclinic Cape Town', 'Mediclinic', 'Hospitals', 'Hospital', 'Western Cape', 'Cape Town'),
('Mediclinic Durbanville', 'Mediclinic', 'Hospitals', 'Hospital', 'Western Cape', 'Cape Town'),

-- Pharmacy Chains
('Clicks Pharmacy Sandton', 'Clicks', 'Pharmacy', 'Pharmacy', 'Gauteng', 'Johannesburg'),
('Clicks Pharmacy V&A Waterfront', 'Clicks', 'Pharmacy', 'Pharmacy', 'Western Cape', 'Cape Town'),
('Clicks Pharmacy Durban', 'Clicks', 'Pharmacy', 'Pharmacy', 'KwaZulu-Natal', 'Durban'),
('Dis-Chem Pharmacy Fourways', 'Dis-Chem', 'Pharmacy', 'Pharmacy', 'Gauteng', 'Johannesburg'),
('Dis-Chem Pharmacy Canal Walk', 'Dis-Chem', 'Pharmacy', 'Pharmacy', 'Western Cape', 'Cape Town'),
('Dis-Chem Pharmacy Gateway', 'Dis-Chem', 'Pharmacy', 'Pharmacy', 'KwaZulu-Natal', 'Durban'),
('Pick n Pay Pharmacy Rosebank', 'Pick n Pay', 'Pharmacy', 'Pharmacy', 'Gauteng', 'Johannesburg'),
('Pick n Pay Pharmacy Claremont', 'Pick n Pay', 'Pharmacy', 'Pharmacy', 'Western Cape', 'Cape Town'),

-- Independent Pharmacies
('Script Wise Pharmacy', 'Independent Pharmacy', 'Pharmacy', 'Pharmacy', 'Gauteng', 'Pretoria'),
('Southern Rx Pharmacy', 'Independent Pharmacy', 'Pharmacy', 'Pharmacy', 'Western Cape', 'Cape Town'),
('Alpha Pharm', 'Independent Pharmacy', 'Pharmacy', 'Pharmacy', 'KwaZulu-Natal', 'Durban'),
('MediRite Pharmacy', 'Independent Pharmacy', 'Pharmacy', 'Pharmacy', 'Eastern Cape', 'Port Elizabeth'),

-- Specialists
('Cardiologist Practice Sandton', 'NHN', 'Cardiologist', 'Specialist', 'Gauteng', 'Johannesburg'),
('Dermatologist Practice Cape Town', 'Independent', 'Dermatologist', 'Specialist', 'Western Cape', 'Cape Town'),
('Neurologist Practice Durban', 'NHN', 'Neurologist', 'Specialist', 'KwaZulu-Natal', 'Durban'),
('Oncologist Practice Pretoria', 'Independent', 'Oncologist', 'Specialist', 'Gauteng', 'Pretoria'),
('General Practitioner Clinic', 'Independent', 'General Practitioner', 'GP', 'Gauteng', 'Johannesburg'),

-- Sub-acute Facilities
('Care At Midstream Sub Acute Facility', 'Life Healthcare', 'Sub-Acute', 'Hospital', 'Gauteng', 'Midrand'),
('Rehabilitation Centre Cape Town', 'Mediclinic', 'Rehabilitation', 'Hospital', 'Western Cape', 'Cape Town');

-- =====================================================
-- TIME DIMENSION DATA (2017-2024)
-- =====================================================

-- Generate time dimension for date range
INSERT INTO DIM_TIME (DATE_KEY, YEAR, MONTH_NO, MONTH_KEY, QUARTER, DAY_OF_WEEK, WEEK_OF_YEAR, IS_WEEKEND)
WITH date_range AS (
  SELECT 
    DATEADD(day, seq4(), '2017-01-01') AS date_key,
    seq4() as row_num
  FROM TABLE(GENERATOR(rowcount => 2922)) -- 8 years * 365.25 days
  WHERE date_key <= '2024-12-31'
)
SELECT 
  date_key,
  EXTRACT(YEAR FROM date_key) AS YEAR,
  EXTRACT(MONTH FROM date_key) AS MONTH_NO,
  EXTRACT(YEAR FROM date_key) * 100 + EXTRACT(MONTH FROM date_key) AS MONTH_KEY,
  EXTRACT(QUARTER FROM date_key) AS QUARTER,
  EXTRACT(DOW FROM date_key) AS DAY_OF_WEEK,
  EXTRACT(WEEK FROM date_key) AS WEEK_OF_YEAR,
  CASE WHEN EXTRACT(DOW FROM date_key) IN (0,6) THEN TRUE ELSE FALSE END AS IS_WEEKEND
FROM date_range;

-- =====================================================
-- CHECKUP_LITE PRODUCT HIERARCHY
-- =====================================================

INSERT INTO DIM_PRODUCTS (NAPPI9, MANUFACTURER, HIGH_LEVEL_1, HIGH_LEVEL_2, HIGH_LEVEL_3, HIGH_LEVEL_4, TR_LEVEL_1, LEVELS_CONCAT_TILL_2, ALL_LEVELS_CONCAT, ALL_LEVELS_CONCAT_4) VALUES
-- Wound Management Products
(227044001, 'Systagenix Wound Management (Pty) Ltd', 'WouM: Wound Management', 'WouM-SynD: Synthetic Dressing', 'WouM-SynD-SiliD: Silicone Dressing', 'WouM-SynD-SiliD-SiliD: Silicone Dressing', 'Wound Management', 'Wound Management | Synthetic Dressing', 'Wound Management | Synthetic Dressing | Silicone Dressing', 'Wound Management | Synthetic Dressing | Silicone Dressing | Silicone Dressing'),
(227044002, 'Smith & Nephew', 'WouM: Wound Management', 'WouM-FoaD: Foam Dressing', 'WouM-FoaD-PolyF: Polyurethane Foam', 'WouM-FoaD-PolyF-AbsF: Absorbent Foam', 'Wound Management', 'Wound Management | Foam Dressing', 'Wound Management | Foam Dressing | Polyurethane Foam', 'Wound Management | Foam Dressing | Polyurethane Foam | Absorbent Foam'),
(227044003, 'ConvaTec', 'WouM: Wound Management', 'WouM-HydD: Hydrocolloid Dressing', 'WouM-HydD-AdhH: Adhesive Hydrocolloid', 'WouM-HydD-AdhH-SteH: Sterile Hydrocolloid', 'Wound Management', 'Wound Management | Hydrocolloid Dressing', 'Wound Management | Hydrocolloid Dressing | Adhesive Hydrocolloid', 'Wound Management | Hydrocolloid Dressing | Adhesive Hydrocolloid | Sterile Hydrocolloid'),

-- Sutures
(454018001, 'Ethicon', 'Sut: Sutures', 'Sut-Abs: Absorbable Sutures', 'Sut-Abs-PglaS: PGLA Sutures', 'Sut-Abs-PglaS-VicS: Vicryl Sutures', 'Sutures', 'Sutures | Absorbable Sutures', 'Sutures | Absorbable Sutures | PGLA Sutures', 'Sutures | Absorbable Sutures | PGLA Sutures | Vicryl Sutures'),
(454018002, 'Ethicon', 'Sut: Sutures', 'Sut-NonA: Non-Absorbable Sutures', 'Sut-NonA-SilkS: Silk Sutures', 'Sut-NonA-SilkS-BraidS: Braided Silk', 'Sutures', 'Sutures | Non-Absorbable Sutures', 'Sutures | Non-Absorbable Sutures | Silk Sutures', 'Sutures | Non-Absorbable Sutures | Silk Sutures | Braided Silk'),
(454018003, 'B. Braun', 'Sut: Sutures', 'Sut-Abs: Absorbable Sutures', 'Sut-Abs-MonoS: Monofilament Sutures', 'Sut-Abs-MonoS-PdsS: PDS Sutures', 'Sutures', 'Sutures | Absorbable Sutures', 'Sutures | Absorbable Sutures | Monofilament Sutures', 'Sutures | Absorbable Sutures | Monofilament Sutures | PDS Sutures'),

-- Syringes
(123456001, 'BD Medical', 'Syr: Syringes', 'Syr-DisSyr: Disposable Syringes', 'Syr-DisSyr-PlasS: Plastic Syringes', 'Syr-DisSyr-PlasS-LuerS: Luer Lock Syringes', 'Syringes', 'Syringes | Disposable Syringes', 'Syringes | Disposable Syringes | Plastic Syringes', 'Syringes | Disposable Syringes | Plastic Syringes | Luer Lock Syringes'),
(123456002, 'Terumo', 'Syr: Syringes', 'Syr-PreS: Pre-filled Syringes', 'Syr-PreS-GlasS: Glass Syringes', 'Syr-PreS-GlasS-SafeS: Safety Syringes', 'Syringes', 'Syringes | Pre-filled Syringes', 'Syringes | Pre-filled Syringes | Glass Syringes', 'Syringes | Pre-filled Syringes | Glass Syringes | Safety Syringes'),

-- Diagnostic Equipment
(789012001, 'Roche Diagnostics', 'Diag: Diagnostics', 'Diag-BloodT: Blood Testing', 'Diag-BloodT-GlucM: Glucose Monitoring', 'Diag-BloodT-GlucM-DigM: Digital Meter', 'Diagnostics', 'Diagnostics | Blood Testing', 'Diagnostics | Blood Testing | Glucose Monitoring', 'Diagnostics | Blood Testing | Glucose Monitoring | Digital Meter'),
(789012002, 'Abbott', 'Diag: Diagnostics', 'Diag-RapidT: Rapid Testing', 'Diag-RapidT-AntT: Antigen Testing', 'Diag-RapidT-AntT-CovidT: COVID Testing', 'Diagnostics', 'Diagnostics | Rapid Testing', 'Diagnostics | Rapid Testing | Antigen Testing', 'Diagnostics | Rapid Testing | Antigen Testing | COVID Testing'),

-- Surgical Instruments
(345678001, 'Johnson & Johnson', 'SurgI: Surgical Instruments', 'SurgI-CuttI: Cutting Instruments', 'SurgI-CuttI-ScalpB: Scalpel Blades', 'SurgI-CuttI-ScalpB-DispB: Disposable Blades', 'Surgical Instruments', 'Surgical Instruments | Cutting Instruments', 'Surgical Instruments | Cutting Instruments | Scalpel Blades', 'Surgical Instruments | Cutting Instruments | Scalpel Blades | Disposable Blades'),
(345678002, 'Medtronic', 'SurgI: Surgical Instruments', 'SurgI-ElecI: Electrocautery', 'SurgI-ElecI-MonoE: Monopolar Electrocautery', 'SurgI-ElecI-MonoE-PencE: Electrocautery Pencil', 'Surgical Instruments', 'Surgical Instruments | Electrocautery', 'Surgical Instruments | Electrocautery | Monopolar Electrocautery', 'Surgical Instruments | Electrocautery | Monopolar Electrocautery | Electrocautery Pencil'),

-- Orthopedic Devices
(567890001, 'DePuy Synthes', 'Orth: Orthopedics', 'Orth-ImpD: Implant Devices', 'Orth-ImpD-HipI: Hip Implants', 'Orth-ImpD-HipI-TitI: Titanium Implants', 'Orthopedics', 'Orthopedics | Implant Devices', 'Orthopedics | Implant Devices | Hip Implants', 'Orthopedics | Implant Devices | Hip Implants | Titanium Implants'),
(567890002, 'Stryker', 'Orth: Orthopedics', 'Orth-Fix: Fixation Devices', 'Orth-Fix-ScrP: Screw Plates', 'Orth-Fix-ScrP-MetP: Metal Plates', 'Orthopedics', 'Orthopedics | Fixation Devices', 'Orthopedics | Fixation Devices | Screw Plates', 'Orthopedics | Fixation Devices | Screw Plates | Metal Plates');

-- =====================================================
-- DOSE ATC HIERARCHY
-- =====================================================

INSERT INTO DIM_ATC_HIERARCHY (ATC_CODE, ATC_DESCRIPTION, ATC_LEVEL_DESC_1, ATC_LEVEL_DESC_2, ATC_LEVEL_DESC_3, ATC_LEVEL_DESC_4, ATC_LEVEL_DESC_5) VALUES
-- Immunosuppressants and Immunomodulating Agents
('L04AA27', 'FINGOLIMOD', 'L - Antineoplastic And Immunomodulating Agents', 'L04 - Immunosuppressants', 'L04A - Immunosuppressants', 'L04AA - Selective Immunosuppressants', 'L04AA27 - Fingolimod'),
('L03AX13', 'GLATIRAMER ACETATE', 'L - Antineoplastic And Immunomodulating Agents', 'L03 - Immunostimulants', 'L03A - Immunostimulants', 'L03AX - Other Immunostimulants', 'L03AX13 - Glatiramer Acetate'),
('L04AB01', 'INTERFERON BETA-1A', 'L - Antineoplastic And Immunomodulating Agents', 'L04 - Immunosuppressants', 'L04A - Immunosuppressants', 'L04AB - Tumor Necrosis Factor Alpha Inhibitors', 'L04AB01 - Etanercept'),

-- Cardiovascular System
('C09AA02', 'ENALAPRIL', 'C - Cardiovascular System', 'C09 - Agents Acting On The Renin-Angiotensin System', 'C09A - ACE Inhibitors, Plain', 'C09AA - ACE Inhibitors, Plain', 'C09AA02 - Enalapril'),
('C07AB07', 'BISOPROLOL', 'C - Cardiovascular System', 'C07 - Beta Blocking Agents', 'C07A - Beta Blocking Agents', 'C07AB - Beta Blocking Agents, Selective', 'C07AB07 - Bisoprolol'),
('C03CA01', 'FUROSEMIDE', 'C - Cardiovascular System', 'C03 - Diuretics', 'C03C - High-Ceiling Diuretics', 'C03CA - Sulfonamides, Plain', 'C03CA01 - Furosemide'),

-- Nervous System
('N05BA12', 'ALPRAZOLAM', 'N - Nervous System', 'N05 - Psycholeptics', 'N05B - Anxiolytics', 'N05BA - Benzodiazepine Derivatives', 'N05BA12 - Alprazolam'),
('N06AB10', 'ESCITALOPRAM', 'N - Nervous System', 'N06 - Psychoanaleptics', 'N06A - Antidepressants', 'N06AB - Selective Serotonin Reuptake Inhibitors', 'N06AB10 - Escitalopram'),
('N02AA01', 'MORPHINE', 'N - Nervous System', 'N02 - Analgesics', 'N02A - Opioids', 'N02AA - Natural Opium Alkaloids', 'N02AA01 - Morphine'),

-- Respiratory System
('R03AC02', 'SALBUTAMOL', 'R - Respiratory System', 'R03 - Drugs For Obstructive Airway Diseases', 'R03A - Adrenergics, Inhalants', 'R03AC - Selective Beta-2-Adrenoreceptor Agonists', 'R03AC02 - Salbutamol'),
('R06AE07', 'CETIRIZINE', 'R - Respiratory System', 'R06 - Antihistamines For Systemic Use', 'R06A - Antihistamines For Systemic Use', 'R06AE - Piperazine Derivatives', 'R06AE07 - Cetirizine'),

-- Alimentary Tract and Metabolism
('A10BA02', 'METFORMIN', 'A - Alimentary Tract And Metabolism', 'A10 - Drugs Used In Diabetes', 'A10B - Blood Glucose Lowering Drugs, Excl. Insulins', 'A10BA - Biguanides', 'A10BA02 - Metformin'),
('A02BC01', 'OMEPRAZOLE', 'A - Alimentary Tract And Metabolism', 'A02 - Drugs For Acid Related Disorders', 'A02B - Drugs For Peptic Ulcer And GORD', 'A02BC - Proton Pump Inhibitors', 'A02BC01 - Omeprazole'),

-- Antibiotics  
('J01CR02', 'AMOXICILLIN/CLAVULANIC ACID', 'J - Antiinfectives For Systemic Use', 'J01 - Antibacterials For Systemic Use', 'J01C - Beta-Lactam Antibacterials, Penicillins', 'J01CR - Combinations Of Penicillins, Incl. Beta-Lactamase Inhibitors', 'J01CR02 - Amoxicillin And Beta-Lactamase Inhibitor'),
('J01FA09', 'CLARITHROMYCIN', 'J - Antiinfectives For Systemic Use', 'J01 - Antibacterials For Systemic Use', 'J01F - Macrolides, Lincosamides And Streptogramins', 'J01FA - Macrolides', 'J01FA09 - Clarithromycin');

-- =====================================================
-- DOSE PHARMACEUTICAL PRODUCTS
-- =====================================================

INSERT INTO DIM_PHARMACEUTICALS (NAPPI9, PRODUCT_NAME, NAPPI_MANUFACTURER, STRENGTH, SCHEDULE, PACK_SIZE, DOSAGE_FORM, ATC_CODE) VALUES
-- Multiple Sclerosis Medications
(720446001, 'Tuvigin', 'Sandoz SA (PTY) LTD', '0.5 - MG', 4, 28, 'CAP', 'L04AA27'),
(708286001, 'Copaxone pre-filled syringe 1ml', 'Teva Pharmaceuticals', '20 - MG/1ML', 4, 28, 'INJ', 'L03AX13'),
(720446002, 'Gilenya', 'Novartis', '0.5 - MG', 4, 28, 'CAP', 'L04AA27'),
(708286002, 'Copaxone', 'Teva Pharmaceuticals', '40 - MG/1ML', 4, 12, 'INJ', 'L03AX13'),

-- Cardiovascular Medications
(701234001, 'Renitec', 'MSD', '10 - MG', 4, 30, 'TAB', 'C09AA02'),
(701234002, 'Concor', 'Merck', '5 - MG', 4, 30, 'TAB', 'C07AB07'),
(701234003, 'Lasix', 'Sanofi', '40 - MG', 4, 30, 'TAB', 'C03CA01'),

-- Nervous System Medications
(702345001, 'Xanor', 'Adcock Ingram', '0.5 - MG', 5, 30, 'TAB', 'N05BA12'),
(702345002, 'Lexamil', 'Lundbeck', '10 - MG', 4, 30, 'TAB', 'N06AB10'),
(702345003, 'Morphine Sulphate', 'Aspen Pharmacare', '10 - MG/1ML', 6, 5, 'INJ', 'N02AA01'),

-- Respiratory Medications
(703456001, 'Ventolin', 'GSK', '100 - MCG/DOSE', 2, 1, 'INH', 'R03AC02'),
(703456002, 'Zyrtec', 'Johnson & Johnson', '10 - MG', 2, 30, 'TAB', 'R06AE07'),

-- Diabetes and Gastrointestinal
(704567001, 'Glucophage', 'Merck', '500 - MG', 4, 60, 'TAB', 'A10BA02'),
(704567002, 'Losec', 'AstraZeneca', '20 - MG', 4, 30, 'CAP', 'A02BC01'),

-- Antibiotics
(705678001, 'Augmentin', 'GSK', '625 - MG', 4, 21, 'TAB', 'J01CR02'),
(705678002, 'Klacid', 'Abbott', '500 - MG', 4, 14, 'TAB', 'J01FA09');

-- =====================================================
-- VALIDATION QUERIES
-- =====================================================

-- Verify reference data counts
SELECT 'Geography' as table_name, COUNT(*) as record_count FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.DIM_GEOGRAPHY
UNION ALL
SELECT 'Medical Schemes', COUNT(*) FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.DIM_MEDICAL_SCHEMES
UNION ALL  
SELECT 'Providers', COUNT(*) FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.DIM_PROVIDERS
UNION ALL
SELECT 'Time Dimension', COUNT(*) FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.DIM_TIME
UNION ALL
SELECT 'CheckUp Products', COUNT(*) FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.DIM_PRODUCTS
UNION ALL
SELECT 'ATC Hierarchy', COUNT(*) FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.DIM_ATC_HIERARCHY
UNION ALL
SELECT 'Pharmaceuticals', COUNT(*) FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.DIM_PHARMACEUTICALS;

-- Sample data verification
SELECT * FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.DIM_GEOGRAPHY LIMIT 5;
SELECT * FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.DIM_MEDICAL_SCHEMES LIMIT 5;
SELECT * FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.DIM_PRODUCTS LIMIT 5;
SELECT * FROM QUANTIUM_HEALTHCARE_DEMO.QUANTIUM_HEALTHCARE_DEMO.DIM_PHARMACEUTICALS LIMIT 5;