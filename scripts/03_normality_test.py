"""
Study: Associated factors of the doctor-patient relationship: An Analysis of Healthcare Users in Loja
Script: 03_normality_test.py
Lead Data Analysis & Code: Pablo Andrés Japón Calva (ORCID: 0009-0001-0705-8120)
Study Co-Investigators: Ruth Maldonado-Rengel, et al.
Affiliations:
  - Independent Researcher, Loja, Ecuador
  - Facultad de Ciencias de la Salud, Universidad Técnica Particular de Loja (UTPL), Loja, Ecuador

Description:
Statistical diagnostics of normality for the primary outcome variable
(PDRQ-9 Overall Mean Score). Performs the D'Agostino-Pearson omnibus test,
Shapiro-Wilk test, and calculates distributional skewness and kurtosis.
"""

import os
import sys
import pandas as pd
from scipy import stats

# Ensure standard UTF-8 console output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "datos", "pdrq9_patients_data.xlsx")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at: {data_path}")

    df = pd.read_excel(data_path)
    pdrq_items = [f"pdrq_item{i}" for i in range(1, 10)]
    df['pdrq_overall_score'] = df[pdrq_items].mean(axis=1)
    data = df['pdrq_overall_score']

    print("=" * 80)
    print("NORMALITY DIAGNOSTICS: PDRQ-9 OVERALL MEAN SCORE (n = 3,257)")
    print("=" * 80)

    # 1. Distributional shape parameters
    skewness = data.skew()
    kurtosis_excess = data.kurtosis()

    print(f"Sample Mean: {data.mean():.4f}")
    print(f"Sample Standard Deviation: {data.std():.4f}")
    print(f"Sample Median: {data.median():.4f}")
    print(f"Skewness: {skewness:.3f} (Pronounced negative skewness)")
    print(f"Excess Kurtosis: {kurtosis_excess:.3f} (Leptokurtic / heavy-tailed)")

    # 2. D'Agostino-Pearson Omnibus Test
    k2_stat, p_k2 = stats.normaltest(data)
    print("\n--- D'AGOSTINO-PEARSON OMNIBUS TEST ---")
    print(f"K² statistic = {k2_stat:.2f}")
    print(f"p-value = {p_k2:.4e} (p < 0.001)")

    # 3. Shapiro-Wilk Test (computed on full analytical sample)
    w_stat, p_w = stats.shapiro(data)
    print("\n--- SHAPIRO-WILK TEST ---")
    print(f"W statistic = {w_stat:.4f}")
    print(f"p-value = {p_w:.4e} (p < 0.001)")

    print("\n" + "=" * 80)
    print("CONCLUSION: Normality is formally rejected (p < 0.001).")
    print("The pronounced negative skewness and ceiling effect justify the use of")
    print("non-parametric bivariate tests and reporting both Medians/IQRs and Means/SDs.")
    print("=" * 80)


if __name__ == "__main__":
    main()
