# Data Dictionary and Codebook

**Study Title:** Associated factors of the doctor-patient relationship: An Analysis of Healthcare Users in Loja  
**Authors:** Research Team  
**Institution:** Universidad Técnica Particular de Loja (UTPL), Loja, Ecuador  
**Analytical Dataset:** `datos/pdrq9_patients_data.xlsx`  
**Sample Size:** n = 3,257 adult outpatients across 30 public healthcare facilities  
**Format:** Excel Spreadsheet (.xlsx)  

---

## 1. Overview of Variables

| Variable Name | Data Type | Role | Description | Value Range / Categories |
| :--- | :--- | :--- | :--- | :--- |
| `patient_id` | String | Identifier | Anonymized unique patient record identifier | Alphanumeric code |
| `health_center` | Categorical | Institutional Factor | Institutional code of the healthcare facility | 30 unique facility codes (see Section 4) |
| `sex` | Integer | Sociodemographic Covariate | Biological sex of the patient | 1 = Male, 2 = Female |
| `age_group` | Integer | Sociodemographic Covariate | Categorical age bracket of the patient | 1 to 5 (see Section 2) |
| `marital_status` | Integer | Sociodemographic Covariate | Marital / civil status of the patient | 1 to 5 (see Section 2) |
| `pdrq_item1` | Integer | Psychometric Item | Item 1: My physician helps me | 1 to 5 (Likert scale) |
| `pdrq_item2` | Integer | Psychometric Item | Item 2: My physician has enough time for me | 1 to 5 (Likert scale) |
| `pdrq_item3` | Integer | Psychometric Item | Item 3: I trust my physician | 1 to 5 (Likert scale) |
| `pdrq_item4` | Integer | Psychometric Item | Item 4: My physician understands me | 1 to 5 (Likert scale) |
| `pdrq_item5` | Integer | Psychometric Item | Item 5: My physician is dedicated to helping me | 1 to 5 (Likert scale) |
| `pdrq_item6` | Integer | Psychometric Item | Item 6: Agreement on the nature of symptoms | 1 to 5 (Likert scale) |
| `pdrq_item7` | Integer | Psychometric Item | Item 7: I can talk to my physician | 1 to 5 (Likert scale) |
| `pdrq_item8` | Integer | Psychometric Item | Item 8: Satisfied with the treatment | 1 to 5 (Likert scale) |
| `pdrq_item9` | Integer | Psychometric Item | Item 9: My physician is available to me | 1 to 5 (Likert scale) |

---

## 2. Sociodemographic Variables Coding

### Biological Sex (`sex`)
* **1 = Male:** n = 995 (30.55%)
* **2 = Female:** n = 2,262 (69.45%)

### Age Groups (`age_group`)
* **1 = 18–30 years:** n = 938 (28.80%) [Reference category in multivariable regression]
* **2 = 31–40 years:** n = 708 (21.74%)
* **3 = 41–50 years:** n = 646 (19.83%)
* **4 = 51–60 years:** n = 599 (18.39%)
* **5 = Over 60 years:** n = 366 (11.24%)

### Marital Status (`marital_status`)
* **1 = Married:** n = 1,369 (42.03%) [Reference category in multivariable regression]
* **2 = Divorced:** n = 257 (7.89%)
* **3 = Widowed:** n = 168 (5.16%)
* **4 = Single:** n = 1,017 (31.23%)
* **5 = Common-law union:** n = 446 (13.69%)

---

## 3. Patient-Doctor Relationship Questionnaire (PDRQ-9)

The PDRQ-9 is a 9-item psychometrically validated instrument assessing patient perception of the therapeutic relationship in primary care consultations.

### Likert Response Scale
Responses to all 9 items (`pdrq_item1` to `pdrq_item9`) are scored on a 5-point Likert scale:
* **1 = Strongly disagree** (Totalmente en desacuerdo)
* **2 = Disagree** (En desacuerdo)
* **3 = Neutral / Indifferent** (Indiferente)
* **4 = Agree** (De acuerdo)
* **5 = Strongly agree** (Totalmente de acuerdo)

### Primary Outcome: PDRQ-9 Overall Mean Score
* **Operationalization:** The continuous composite score calculated as the unweighted arithmetic mean across all 9 items for each individual participant:
  $$\text{PDRQ-9 Overall Mean Score} = \frac{1}{9} \sum_{i=1}^{9} \text{pdrq\_item}_i$$
* **Theoretical Range:** 1.00 to 5.00 points.
* **Methodological Rationale:** Due to a pronounced ceiling effect across raw item responses (median = 5.00 for all 9 items), computing the overall mean score restores decimal variability (sample median = 4.56, mean = 4.36, SD = 0.74), capturing subtle perceptual differences across healthcare facilities and enabling parametric multivariable linear modeling.

---

## 4. Healthcare Facilities Catalog (`health_center`)

The study included all 30 public healthcare facilities in Loja Canton operating under the Ministry of Public Health (MSP), comprising 20 Type A health centers, 4 Type B centers, 4 health posts, 1 basic hospital, and 1 general hospital:

| Code | Official Facility Name | Facility Type / Level |
| :--- | :--- | :--- |
| **CS1** | Centro de Salud No. 1 | Health Center Type B |
| **CS2** | Centro de Salud No. 2 | Health Center Type B |
| **CS3** | Centro de Salud No. 3 | Health Center Type B |
| **CSA** | Aguangora | Health Center Type A |
| **CSB** | Belén | Health Center Type A |
| **CSCA** | Carigán | Health Post |
| **CSCH** | Chuquiribamba | Health Center Type A |
| **CSCHO** | Chontacruz | Health Center Type A |
| **CSCO** | Comunidades | Health Post |
| **CSCON** | Consacola | Health Center Type A |
| **CSEC** | El Cisne | Health Center Type A |
| **CSG** | Gualel | Health Post |
| **CSHDC** | Héroes del Cenepa | Health Center Type A |
| **CSJ** | Jimbilla | Health Center Type A |
| **CSM** | Malacatos | Health Center Type A |
| **CSMI** | Miraflores | Health Center Type A |
| **CSMO** | Motupe | Health Center Type A |
| **CSO** | Obrapía | Health Center Type A |
| **CSP** | Pichic | Health Post |
| **CSS** | Santiago | Health Center Type A |
| **CSSC** | San Cayetano | Health Center Type A |
| **CSSL** | San Lucas | Health Center Type A |
| **CST** | Taquil | Health Center Type B |
| **CSTC** | Tierras Coloradas | Health Center Type A |
| **CSUL** | Unión Lojana | Health Center Type A |
| **CSY** | Yangana | Health Center Type A |
| **CSZH** | Zamora Huaico | Health Center Type A |
| **HBV** | Hospital Básico Vilcabamba | Basic Hospital |
| **HGIA** | Hospital General Isidro Ayora | General Hospital (Provincial Reference) |
| **UAV** | Unidad Anidada Vilcabamba | Health Center Type A (Nested Unit) |
