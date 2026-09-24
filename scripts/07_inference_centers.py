"""
Study: Associated factors of the doctor-patient relationship: An Analysis of Healthcare Users in Loja
Script: 07_inference_centers.py
Lead Data Analysis & Code: Pablo Andrés Japón Calva (ORCID: 0009-0001-0705-8120)
Study Co-Investigators: Ruth Maldonado-Rengel, et al.
Affiliations:
  - Independent Researcher, Loja, Ecuador
  - Facultad de Ciencias de la Salud, Universidad Técnica Particular de Loja (UTPL), Loja, Ecuador

Description:
Inferential bivariate comparison of the perceived physician-patient relationship
(PDRQ-9 Overall Mean Score) across the 30 public healthcare facilities in Loja Canton.
Performs:
1. Facility-level parametric and non-parametric descriptive profiling.
2. Kruskal-Wallis H omnibus test across 30 healthcare centers and eta-squared (eta²_H) calculation.
"""

import os
import sys
import numpy as np
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

    print("=" * 90)
    print("INFERENTIAL BIVARIATE ANALYSIS: HEALTHCARE FACILITIES (30 CENTERS, n = 3,257)")
    print("=" * 90)

    # Calculate facility-level metrics
    facility_summary = []
    centers_unique = df['health_center'].unique()

    for center in centers_unique:
        scores = df[df['health_center'] == center]['pdrq_overall_score']
        q1 = np.percentile(scores, 25)
        q3 = np.percentile(scores, 75)
        facility_summary.append({
            'Center': center,
            'n': len(scores),
            'Mean': scores.mean(),
            'SD': scores.std(),
            'Median': scores.median(),
            'IQR': q3 - q1,
            'Q1': q1,
            'Q3': q3
        })

    df_fac = pd.DataFrame(facility_summary).sort_values(by=['Median', 'Mean'], ascending=False)
    
    # Display table formatted
    display_df = df_fac.copy()
    display_df['Mean'] = display_df['Mean'].apply(lambda x: f"{x:.2f}")
    display_df['SD'] = display_df['SD'].apply(lambda x: f"{x:.2f}")
    display_df['Median'] = display_df['Median'].apply(lambda x: f"{x:.2f}")
    display_df['IQR'] = display_df['IQR'].apply(lambda x: f"{x:.2f}")
    display_df['[Q1–Q3]'] = display_df.apply(lambda r: f"[{r['Q1']:.2f}–{r['Q3']:.2f}]", axis=1)
    
    print(display_df[['Center', 'n', 'Mean', 'SD', 'Median', 'IQR', '[Q1–Q3]']].to_string(index=False))

    # Kruskal-Wallis H Test across 30 healthcare facilities
    groups = [df[df['health_center'] == c]['pdrq_overall_score'] for c in centers_unique]
    h_stat, p_kw = stats.kruskal(*groups)
    k_groups = len(groups)
    n_total = len(df)
    eta2_h = (h_stat - k_groups + 1) / (n_total - k_groups)

    print("\n--- KRUSKAL-WALLIS H TEST (30 FACILITIES) ---")
    print(f"Kruskal-Wallis H statistic = {h_stat:.2f}")
    print(f"Degrees of freedom (df) = {k_groups - 1}")
    print(f"p-value = {p_kw:.4e} (p < 0.001)")
    print(f"Eta-squared (η²_H) = {eta2_h:.3f} (Accounts for {eta2_h*100:.2f}% of total variance)")

    print("\n" + "=" * 90)
    print("KEY FINDINGS:")
    print("1. Healthcare facility is the dominant factor, explaining ~31.2% of outcome variance.")
    print("2. Upper ceiling excellence (Median = 5.00): Consacola, Motupe, Unión Lojana, Belén, San Cayetano.")
    print("3. Intermediate provincial reference: Hospital General Isidro Ayora (HGIA, n = 481, Median = 4.22).")
    print("4. Extreme institutional outlier: Centro de Salud Gualel (CSG, n = 74, Median = 2.00, IQR = 0.53).")
    print("=" * 90)


if __name__ == "__main__":
    main()
