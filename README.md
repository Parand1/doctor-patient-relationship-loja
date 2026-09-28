# Replication Package: Associated Factors of the Doctor-Patient Relationship: An Analysis of Healthcare Users in Loja

[![Python Version](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![License: Open Access](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

This repository contains the dataset, analysis scripts, and figures for the empirical study:

> **Associated factors of the doctor-patient relationship: An Analysis of Healthcare Users in Loja**  
> *Ruth Maldonado-Rengel, Angélica Arrobo-Rodas, Patricia Díaz Guzmán, Michelle Domínguez, Diana Carolina Sarmiento Peñarreta, Camila Elizabeth Monroy Morillo, Mikaela Milena Cadena Vásconez, Jessie Scarlet Patiño Armijos, Edith Lisbeth Pardo Correa, Daniela Carolina Hurtado Costa, Pablo Andrés Japón Calva.*

---

## Authorship and Scientific Contributions

* **Lead Data Analyst & Statistical Programmer:**  
  **Pablo Andrés Japón Calva**  
  *Independent Researcher, Loja, Ecuador*  
  ORCID: [0009-0001-0705-8120](https://orcid.org/0009-0001-0705-8120)

* **Principal Investigators & Clinical Research Team:**  
  *Facultad de Ciencias de la Salud, Universidad Técnica Particular de Loja (UTPL), Loja, Ecuador*

* **Corresponding Author:**  
  **Ruth Maldonado-Rengel** (`remaldonado6@utpl.edu.ec`)  
  *Universidad Técnica Particular de Loja (UTPL), Loja, Ecuador*

---

## Study Overview

* **Design:** A descriptive, cross-sectional, and quantitative research design.
* **Analytical Sample:** $n = 3,257$ adult patients ($\ge 18$ years) who received outpatient medical consultations.
* **Geographical Setting:** Loja Canton, southern Ecuador.
* **Institutional Coverage:** Thirty public healthcare facilities in Loja Canton operating under the Ministry of Public Health (MSP), comprising: 20 Type A health centers, 4 Type B centers, 4 health posts, 1 general hospital, and 1 basic hospital.
* **Primary Outcome:** Perceived physician–patient relationship evaluated using the **Patient-Doctor Relationship Questionnaire (PDRQ-9)** and operationalized through the continuous **PDRQ-9 Overall Mean Score** (scale 1.00 to 5.00).

---

## Repository Structure

```text
repositorio_articulo/
├── README.md                      # Study documentation and execution instructions
├── DATA_DICTIONARY.md             # Codebook and variable definitions
├── requirements.txt               # Python package dependencies
├── datos/
│   └── pdrq9_patients_data.xlsx   # Analytical database (n = 3,257)
├── scripts/
│   ├── 00_scale_reliability.py    # Psychometric internal consistency (Cronbach's alpha bootstrap)
│   ├── 01_sociodemographic.py     # Table 1: Sociodemographic profile calculation
│   ├── 02_pdrq9_descriptive.py    # Table 2: PDRQ-9 item-level and overall descriptive statistics
│   ├── 03_normality_test.py       # D'Agostino-Pearson omnibus normality test & shape parameters
│   ├── 03_normality_plot.py       # Figure 0: Density histogram + KDE vs Gaussian & Q-Q Plot
│   ├── 04_inference_sex.py        # Mann-Whitney U test, Z, Rosenthal's r, and rank-biserial
│   ├── 04_plot_sex.py             # Figure 4: Boxplot by biological sex
│   ├── 05_inference_age.py        # Kruskal-Wallis H test & Dunn-Bonferroni pairwise post-hoc (Age)
│   ├── 05_plot_age.py             # Figure 1: Boxplot across patient age cohorts
│   ├── 06_inference_marital.py    # Kruskal-Wallis H test & Dunn-Bonferroni post-hoc (Marital status)
│   ├── 06_plot_marital.py         # Figure 2: Boxplot across marital categories
│   ├── 07_inference_centers.py    # Kruskal-Wallis H test across all 30 healthcare facilities
│   ├── 07_plot_centers.py         # Figure 3: Institutional ranking across the 30 healthcare facilities
│   ├── 08_multivariable_model.py  # Hierarchical regression calculations (Models 1 & 2, Cluster-SE, ANOVA)
│   └── 08_multivariable_table.py  # Table 3: Publication Excel generator (Models 1 & 2 side-by-side)
├── tablas/
│   ├── table_1_sociodemographic.xlsx          # Table 1: Sociodemographic profile
│   ├── table_2_pdrq9_descriptive.xlsx         # Table 2: PDRQ-9 item-level and overall statistics
│   └── table_3_multivariable_regression.xlsx  # Table 3: Hierarchical multivariable regression
└── imagenes/
    ├── figure_0_normality.png
    ├── figure_1_age.png
    ├── figure_2_marital_status.png
    ├── figure_3_healthcare_centers.png
    └── figure_4_sex.png
```

---

## Environment Setup and Requirements

This replication pipeline was developed and tested in **Python v3.12**.

### Installation

Clone the repository and install required dependencies using `pip`:

```bash
git clone <repository-url>
cd repositorio_articulo
pip install -r requirements.txt
```

### Core Libraries

| Library | Version | Purpose |
| :--- | :--- | :--- |
| `pandas` | $\ge 2.2.0$ | Data manipulation and tabular management |
| `scipy` | $\ge 1.14.0$ | Parametric and non-parametric biostatistical testing |
| `statsmodels` | $\ge 0.14.0$ | Hierarchical OLS regression and cluster-robust standard errors |
| `matplotlib` | $\ge 3.9.0$ | Graphic rendering and figure generation |
| `seaborn` | $\ge 0.13.0$ | Statistical visualization |
| `openpyxl` | $\ge 3.1.0$ | Reading and writing Excel spreadsheets |

---

## Execution Guide & Analytical Workflow

All scripts are self-contained and run using relative directory paths. You can execute them individually from the `scripts/` directory or sequentially:

### 1. Scale Reliability and Psychometrics
```bash
python scripts/00_scale_reliability.py
```
* **Output:** Cronbach's alpha $\alpha = 0.940$ (95% Bootstrap CI: $[0.934 - 0.945]$), corrected item-total correlations ($0.73 - 0.79$).

### 2. Descriptive Tables
```bash
python scripts/01_sociodemographic.py
python scripts/02_pdrq9_descriptive.py
```
* **Output:** Table 1 frequencies and percentages (Sex, Age, Marital status); Table 2 parametric (Mean, SD) and non-parametric (Median, IQR, $[Q1-Q3]$) metrics for all 9 PDRQ-9 items and the overall score.

### 3. Normality Diagnostics
```bash
python scripts/03_normality_test.py
python scripts/03_normality_plot.py
```
* **Output:** D'Agostino-Pearson $K^2 = 1120.61, p < 0.001$, skewness = $-1.76$, kurtosis = $3.81$. Generates `imagenes/figure_0_normality.png`.

### 4. Bivariate Inferential Hypotheses
```bash
python scripts/04_inference_sex.py
python scripts/04_plot_sex.py
python scripts/05_inference_age.py
python scripts/05_plot_age.py
python scripts/06_inference_marital.py
python scripts/06_plot_marital.py
python scripts/07_inference_centers.py
python scripts/07_plot_centers.py
```
* **Output:** 
  * Sex: Mann-Whitney $U = 1,122,588.50, p = 0.910$, Rosenthal $r = 0.002$ (`figure_4_sex.png`).
  * Age: Kruskal-Wallis $H = 84.82, p < 0.001, \eta^2_H = 0.025$. Over 60 yrs vs all younger cohorts $p_{adj} < 0.001$ (`figure_1_age.png`).
  * Marital Status: Kruskal-Wallis $H = 20.78, p < 0.001, \eta^2_H = 0.005$ (`figure_2_marital_status.png`).
  * Healthcare Facilities: Kruskal-Wallis $H = 1034.91, p < 0.001, \eta^2_H = 0.312$ (`figure_3_healthcare_centers.png`).

### 5. Multivariable Modeling & Cluster Control
```bash
python scripts/08_multivariable_model.py
python scripts/08_multivariable_table.py
```
* **Output:**
  * Model 1 (Sociodemographics): $R^2 = 2.89\%, F(9, 3247) = 10.73, p < 0.001$.
  * Model 2 (Facility-Adjusted): $R^2 = 35.66\%, \Delta R^2 = 32.77\%, F(29, 3218) = 56.52, p < 0.001$ (Facilities explain 91.90% of explainable variance).
  * Cluster-Robust Adjustment: Age $>60$ years is the sole sociodemographic factor with an independent positive association ($\beta = +0.357, 95\% \text{ CI}: +0.225 \text{ to } +0.489, z = 5.31, p < 0.001$).
  * Table 3: Generated in Excel at `tablas/table_3_multivariable_regression.xlsx` with clean publication formatting.

---

## Correspondence with Manuscript Elements

| Manuscript Element | Analytical Script | Figure / Output File |
| :--- | :--- | :--- |
| **Methods / Psychometrics** | `00_scale_reliability.py` | Console report ($\alpha = 0.940$) |
| **Table 1** (Sociodemographics) | `01_sociodemographic.py` | Console Table 1 & `tablas/table_1_sociodemographic.xlsx` |
| **Table 2** (PDRQ-9 Descriptives) | `02_pdrq9_descriptive.py` | Console Table 2 & `tablas/table_2_pdrq9_descriptive.xlsx` |
| **Normality Assessment** | `03_normality_test.py`, `03_normality_plot.py` | `imagenes/figure_0_normality.png` |
| **Figure 1** (Age comparison) | `05_inference_age.py`, `05_plot_age.py` | `imagenes/figure_1_age.png` |
| **Figure 2** (Marital status) | `06_inference_marital.py`, `06_plot_marital.py` | `imagenes/figure_2_marital_status.png` |
| **Figure 3** (Healthcare facilities) | `07_inference_centers.py`, `07_plot_centers.py` | `imagenes/figure_3_healthcare_centers.png` |
| **Figure 4** (Sex comparison) | `04_inference_sex.py`, `04_plot_sex.py` | `imagenes/figure_4_sex.png` |
| **Table 3** (Hierarchical Regression) | `08_multivariable_model.py`, `08_multivariable_table.py` | Console model statistics & `tablas/table_3_multivariable_regression.xlsx` |

---

## Citation and Licensing

* **Code License:** [MIT License](https://opensource.org/licenses/MIT).
* **Data License:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
* **Citation:** When utilizing or replicating this codebase, please cite the original published manuscript and this replication repository.
