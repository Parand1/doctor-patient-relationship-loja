# Replication Package: Associated Factors of the Doctor-Patient Relationship: An Analysis of Healthcare Users in Loja

[![Python Version](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![License: Open Access](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

This repository contains the dataset, analysis scripts, tables, and figures for the empirical study:

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
* **Analytical Sample:** $n = 3,257$ complete adult outpatient records ($\ge 18$ years) retained after quality control and data cleaning from $3,426$ initially collected questionnaires ($130$ excluded due to subsequent visits within the same month and $39$ due to duplicate or incomplete entries).
* **Geographical Setting:** Loja Canton, southern Ecuador.
* **Institutional Coverage:** Thirty public healthcare facilities in Loja Canton operating under the Ministry of Public Health (MSP), comprising: 20 Type A health centers, 4 Type B centers, 4 health posts, 1 basic hospital, and 1 general hospital.
* **Primary Outcome:** Perceived physician–patient relationship evaluated using the unidimensional 9-item Spanish version of the **Patient-Doctor Relationship Questionnaire (PDRQ-9)** (validated by Fernández Castillo et al., derived from Van der Feltz-Cornelis et al.) and operationalized through the continuous **PDRQ-9 Overall Mean Score** (arithmetic mean across all 9 items, scale 1.00 to 5.00).

---

## Repository Structure

```text
repositorio_articulo/
├── README.md                                  # Study documentation and execution instructions
├── DATA_DICTIONARY.md                         # Codebook and variable definitions
├── requirements.txt                           # Python package dependencies
├── datos/
│   └── pdrq9_patients_data.xlsx               # Analytical database (n = 3,257)
├── scripts/
│   ├── 00_scale_reliability.py                # Psychometric internal consistency (Cronbach's alpha bootstrap)
│   ├── 01_sociodemographic.py                 # Table 1: Sociodemographic profile calculation
│   ├── 02_pdrq9_descriptive.py                # Table 2: PDRQ-9 item-level and overall descriptive statistics
│   ├── 03_normality_test.py                   # D'Agostino-Pearson & Shapiro-Wilk normality tests
│   ├── 03_normality_plot.py                   # Figure 0: Density histogram + KDE vs Gaussian & Q-Q Plot
│   ├── 04_inference_sex.py                    # Mann-Whitney U test, Z, Rosenthal's r, and rank-biserial
│   ├── 04_plot_sex.py                         # Figure 4: Boxplot by biological sex
│   ├── 05_inference_age.py                    # Kruskal-Wallis H test & Dunn-Bonferroni pairwise post-hoc (Age)
│   ├── 05_plot_age.py                         # Figure 1: Boxplot across patient age cohorts
│   ├── 06_inference_marital.py                # Kruskal-Wallis H test & Dunn-Bonferroni post-hoc (Marital status)
│   ├── 06_plot_marital.py                     # Figure 2: Boxplot across marital categories
│   ├── 07_inference_centers.py                # Kruskal-Wallis H, effect sizes & Dunn post-hoc across 30 facilities
│   ├── 07_table_centers.py                    # Table 3: Facility-level distribution & ceiling effect generator
│   ├── 07_plot_centers.py                     # Figure 3: Institutional ranking across the 30 healthcare facilities
│   ├── 08_multivariable_model.py              # Hierarchical regression (Models 1 & 2, Huber-White CRV1 SEs)
│   ├── 08_multivariable_table.py              # Table 4: Publication Excel generator (Models 1 & 2 side-by-side)
│   └── 09_sensitivity_analysis.py             # OLS diagnostics, Quantile (Median) regression & Tobit model
├── tablas/
│   ├── table_1_sociodemographic.xlsx          # Table 1: Sociodemographic profile
│   ├── table_2_pdrq9_descriptive.xlsx         # Table 2: PDRQ-9 item-level and overall statistics
│   ├── table_3_healthcare_facilities.xlsx     # Table 3: Distribution across 30 healthcare facilities
│   ├── table_4_multivariable_regression.xlsx  # Table 4: Hierarchical multivariable regression (Models 1 & 2)
│   └── table_s1_sensitivity_analysis.xlsx     # Supplementary Table: OLS vs. Median (LAD) vs. Tobit models
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
| `scipy` | $\ge 1.14.0$ | Parametric and non-parametric biostatistical testing & optimization |
| `statsmodels` | $\ge 0.14.0$ | Hierarchical OLS, Huber–White CRV1 cluster-robust SEs, and Quantile regression |
| `matplotlib` | $\ge 3.9.0$ | Graphic rendering and figure generation |
| `seaborn` | $\ge 0.13.0$ | Statistical visualization |
| `openpyxl` | $\ge 3.1.0$ | Reading and writing Excel spreadsheets |
| `numpy` | $\ge 1.26.0$ | Numerical computing and matrix operations |

---

## Execution Guide & Analytical Workflow

All scripts are self-contained and run using relative directory paths. You can execute them individually from the repository root:

### 1. Scale Reliability and Psychometrics
```bash
python scripts/00_scale_reliability.py
```
* **Output:** Cronbach's alpha $\alpha = 0.940$ (95% Bootstrap CI: $[0.934 - 0.945]$), corrected item-total correlations ($0.73 - 0.79$).

### 2. Descriptive Tables (Tables 1 & 2)
```bash
python scripts/01_sociodemographic.py
python scripts/02_pdrq9_descriptive.py
```
* **Output:** Table 1 frequencies and percentages (Sex, Age, Marital status); Table 2 parametric (Mean, SD) and non-parametric (Median, IQR, $[Q1-Q3]$) metrics for all 9 PDRQ-9 items and the overall mean score ($\text{Mean} = 4.36, \text{SD} = 0.74; \text{Median} = 4.56, \text{IQR} = 1.00 [4.00-5.00]$).

### 3. Normality Diagnostics
```bash
python scripts/03_normality_test.py
python scripts/03_normality_plot.py
```
* **Output:** D'Agostino-Pearson $K^2 = 1120.61, p < 0.001$; Shapiro-Wilk $W = 0.8185, p < 0.001$; skewness = $-1.76$, excess kurtosis = $3.81$. Generates `imagenes/figure_0_normality.png`.

### 4. Bivariate Inferential Hypotheses & Facility Profiling (Table 3 & Figures 1–4)
```bash
python scripts/04_inference_sex.py
python scripts/04_plot_sex.py
python scripts/05_inference_age.py
python scripts/05_plot_age.py
python scripts/06_inference_marital.py
python scripts/06_plot_marital.py
python scripts/07_inference_centers.py
python scripts/07_table_centers.py
python scripts/07_plot_centers.py
```
* **Output:** 
  * Sex: Mann-Whitney $U = 1,122,588.50, Z = -0.114, p = 0.910$, Rosenthal $r = 0.002$, $r_{rb} = 0.002$ (`figure_4_sex.png`).
  * Age: Kruskal-Wallis $H(4) = 84.82, p < 0.001, \eta^2_H = 0.025$. Over 60 years vs. all younger cohorts $p_{adj} < 0.001$ (`figure_1_age.png`).
  * Marital Status: Kruskal-Wallis $H(4) = 20.78, p < 0.001, \eta^2_H = 0.005$ (`figure_2_marital_status.png`).
  * Healthcare Facilities: Kruskal-Wallis $H(29) = 1034.91, p < 0.001, \eta^2_H = 0.312, \varepsilon^2 = 0.318$, Dunn post-hoc comparisons (Bonferroni and Benjamini-Hochberg FDR), Table 3 (`tablas/table_3_healthcare_facilities.xlsx`), and Figure 3 (`figure_3_healthcare_centers.png`).

### 5. Multivariable Modeling & Institutional Cluster-Robust Adjustment (Table 4)
```bash
python scripts/08_multivariable_model.py
python scripts/08_multivariable_table.py
```
* **Output:**
  * **Model 1 (Sociodemographic OLS):** $R^2 = 2.89\%, \text{Adjusted } R^2 = 2.62\%, F(9, 3247) = 10.73, p < 0.001$.
  * **Model 2 (Facility Fixed Effects + Cluster-Robust SEs):** Incorporates fixed-effect indicators for all 30 healthcare facilities (29 indicator variables) with standard errors estimated via the Huber–White cluster-robust sandwich covariance estimator (`CRV1`, $G = 30$ clusters), finite-sample degrees-of-freedom correction $[G / (G - 1)] \times [(N - 1) / (N - k)]$ ($G = 30, N = 3,257, k = 39$), and standard normal ($z$) reference distribution.
  * **Model Fit Comparison:** Adding healthcare facility indicators increased the model $R^2$ from $2.89\%$ to $35.66\%$ ($\text{Adjusted } R^2$ from $2.62\%$ to $34.90\%$), corresponding to a descriptive increase of $+32.77$ percentage points in explained variance.
  * **Facility-Adjusted Sociodemographic Associations:**
    * Age $>60$ years (vs. 18–30 years): $\beta = +0.286, 95\% \text{ CI}: [+0.176, +0.395], z = 5.11, p < 0.001$.
    * Divorced (vs. Married): $\beta = -0.183, 95\% \text{ CI}: [-0.304, -0.062], z = -2.96, p = 0.003$.
    * Female (vs. Male): $\beta = +0.061, 95\% \text{ CI}: [-0.012, +0.134], z = 1.65, p = 0.100$ (not statistically significant).
  * **Table 4:** Generated in Excel at `tablas/table_4_multivariable_regression.xlsx`.

### 6. OLS Diagnostics & Sensitivity Analyses
```bash
python scripts/09_sensitivity_analysis.py
```
* **Output:**
  * **OLS Diagnostics:** All sociodemographic VIFs $\le 1.66$ ($< 5.0$ threshold); Breusch-Pagan test $\text{LM} = 122.49, p < 0.001$; maximum Cook's distance $= 0.0241 < 1.0$; residual skewness $= -1.95$, excess kurtosis $= 7.71$.
  * **Sensitivity Analysis 1 (Quantile / Median Regression, $q = 0.50$):** Over 60 years ($\beta = +0.111, p < 0.001$), Divorced ($\beta = -0.111, p < 0.001$), Female ($\beta = 0.000, p = 1.000$).
  * **Sensitivity Analysis 2 (Upper-Censored Tobit Model at 5.00):** Over 60 years ($\beta = +0.443$), Divorced ($\beta = -0.245$), Female ($\beta = +0.083$).
  * **Supplementary Table:** Exported to `tablas/table_s1_sensitivity_analysis.xlsx`.

---

## Correspondence with Manuscript Elements

| Manuscript Element | Analytical Script | Figure / Output File |
| :--- | :--- | :--- |
| **Methods / Psychometrics** | `00_scale_reliability.py` | Console report ($\alpha = 0.940$) |
| **Table 1** (Sociodemographics) | `01_sociodemographic.py` | `tablas/table_1_sociodemographic.xlsx` |
| **Table 2** (PDRQ-9 Descriptives) | `02_pdrq9_descriptive.py` | `tablas/table_2_pdrq9_descriptive.xlsx` |
| **Normality Assessment** | `03_normality_test.py`, `03_normality_plot.py` | `imagenes/figure_0_normality.png` |
| **Figure 1** (Age comparison) | `05_inference_age.py`, `05_plot_age.py` | `imagenes/figure_1_age.png` |
| **Figure 2** (Marital status) | `06_inference_marital.py`, `06_plot_marital.py` | `imagenes/figure_2_marital_status.png` |
| **Table 3 & Figure 3** (Healthcare facilities) | `07_inference_centers.py`, `07_table_centers.py`, `07_plot_centers.py` | `tablas/table_3_healthcare_facilities.xlsx` & `imagenes/figure_3_healthcare_centers.png` |
| **Figure 4** (Sex comparison) | `04_inference_sex.py`, `04_plot_sex.py` | `imagenes/figure_4_sex.png` |
| **Table 4** (Hierarchical Regression) | `08_multivariable_model.py`, `08_multivariable_table.py` | `tablas/table_4_multivariable_regression.xlsx` |
| **OLS Diagnostics & Sensitivity** | `09_sensitivity_analysis.py` | `tablas/table_s1_sensitivity_analysis.xlsx` |

---

## Citation and Licensing

* **Code License:** [MIT License](https://opensource.org/licenses/MIT).
* **Data License:** [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
* **Citation:** When utilizing or replicating this codebase, please cite the original published manuscript and this replication repository.
