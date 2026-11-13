# Data Dictionary and Codebook

**Study Title:** Associated factors of the doctor-patient relationship: An Analysis of Healthcare Users in Loja  
**Lead Data Analyst & Code:** Pablo Andrés Japón Calva (ORCID: [0009-0001-0705-8120](https://orcid.org/0009-0001-0705-8120))  
**Study Co-Investigators:** Ruth Maldonado-Rengel, et al.  
**Institution:** Universidad Técnica Particular de Loja (UTPL), Loja, Ecuador  
**Analytical Dataset:** `datos/pdrq9_patients_data.xlsx`  
**Sample Size:** $n = 3,257$ complete adult outpatient records across 30 public healthcare facilities  
**Format:** Excel Spreadsheet (`.xlsx`)  

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
* **1 = Male:** $n = 995$ ($30.55\%$) [Reference category in multivariable regression]
* **2 = Female:** $n = 2,262$ ($69.45\%$)

### Age Groups (`age_group`)
* **1 = 18–30 years:** $n = 938$ ($28.80\%$) [Reference category in multivariable regression]
* **2 = 31–40 years:** $n = 708$ ($21.74\%$)
* **3 = 41–50 years:** $n = 646$ ($19.83\%$)
* **4 = 51–60 years:** $n = 599$ ($18.39\%$)
* **5 = Over 60 years:** $n = 366$ ($11.24\%$)

### Marital Status (`marital_status`)
* **1 = Married:** $n = 1,369$ ($42.03\%$) [Reference category in multivariable regression]
* **2 = Divorced:** $n = 257$ ($7.89\%$)
* **3 = Widowed:** $n = 168$ ($5.16\%$)
* **4 = Single:** $n = 1,017$ ($31.23\%$)
* **5 = Common-law union:** $n = 446$ ($13.69\%$)

---

## 3. Patient-Doctor Relationship Questionnaire (PDRQ-9)

The study administered the full 9-item Spanish version of the PDRQ-9 validated by Fernández Castillo et al. (derived from the original 9-item PDRQ-9 by Van der Feltz-Cornelis et al.), without modifications, adaptations, or new translations. The PDRQ-9 is validated and analyzed as a single unidimensional construct assessing patients' subjective perceptions of their clinical relationship with the physician.

### Likert Response Scale
Responses to all 9 items (`pdrq_item1` to `pdrq_item9`) are scored on a 5-point Likert scale:
* **1 = Strongly disagree** (Totalmente en desacuerdo)
* **2 = Disagree** (En desacuerdo)
* **3 = Neutral** (Indiferente / Neutral)
* **4 = Agree** (De acuerdo)
* **5 = Strongly agree** (Totalmente de acuerdo)

### Primary Outcome: PDRQ-9 Overall Mean Score
* **Operationalization:** The continuous composite score calculated as the unweighted arithmetic mean across all 9 items for each participant:
  $$\text{PDRQ-9 Overall Mean Score} = \frac{1}{9} \sum_{i=1}^{9} \text{pdrq\_item}_i$$
* **Theoretical Range:** $1.00$ to $5.00$ points.
* **Missing Data Handling:** Only fully completed questionnaires were retained in the analytical sample ($n = 3,257$); there are zero missing item-level responses and no data imputation was performed.
* **Distributional Properties:** Because individual items exhibit a ceiling effect (median $= 5.00$ across all 9 items; $29.2\%$ of participants scored the maximum $5.00$ across all items), computing the overall mean score preserves continuous decimal granularity ($\text{sample median} = 4.56, \text{IQR} = 1.00 [4.00-5.00]; \text{mean} = 4.36, \text{SD} = 0.74$) for both non-parametric bivariate comparisons and multivariable modeling (verified via quantile and upper-censored Tobit sensitivity analyses).

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
