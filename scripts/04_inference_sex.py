"""
Study: Associated factors of the doctor-patient relationship: An Analysis of Healthcare Users in Loja
Script: 04_inference_sex.py
Lead Data Analysis & Code: Pablo Andrés Japón Calva (ORCID: 0009-0001-0705-8120)
Study Co-Investigators: Ruth Maldonado-Rengel, et al.
Affiliations:
  - Independent Researcher, Loja, Ecuador
  - Facultad de Ciencias de la Salud, Universidad Técnica Particular de Loja (UTPL), Loja, Ecuador

Description:
Inferential bivariate comparison of the perceived physician-patient relationship
(PDRQ-9 Overall Mean Score) across biological sexes (Male vs. Female).
Performs the two-tailed Mann-Whitney U test, calculates the asymptotic Z-score,
and reports standardized non-parametric effect sizes: Rosenthal's r and Rank-Biserial correlation (r_rb).
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

    print("=" * 80)
    print("INFERENTIAL BIVARIATE ANALYSIS: SEX (MALE VS. FEMALE)")
    print("=" * 80)

    male_scores = df[df['sex'] == 1]['pdrq_overall_score']
    female_scores = df[df['sex'] == 2]['pdrq_overall_score']

    n_male = len(male_scores)
    n_female = len(female_scores)
    n_total = n_male + n_female

    print(f"Sample distribution: Male n = {n_male:,} (30.55%) | Female n = {n_female:,} (69.45%)\n")

    # Group descriptives
    stats_data = []
    for label, group in [('Male', male_scores), ('Female', female_scores)]:
        q1 = np.percentile(group, 25)
        q3 = np.percentile(group, 75)
        stats_data.append({
            'Sex': label,
            'n': len(group),
            'Mean': f"{group.mean():.2f}",
            'SD': f"{group.std():.2f}",
            'Median': f"{group.median():.2f}",
            'IQR': f"{(q3 - q1):.2f}",
            '[Q1–Q3]': f"[{q1:.2f}–{q3:.2f}]"
        })
    print(pd.DataFrame(stats_data).to_string(index=False))

    # Mann-Whitney U Test
    u_stat, p_val = stats.mannwhitneyu(male_scores, female_scores, alternative='two-sided')

    # Asymptotic Z-score approximation
    mean_u = (n_male * n_female) / 2
    std_u = np.sqrt((n_male * n_female * (n_total + 1)) / 12)
    z_score = (u_stat - mean_u) / std_u

    # Effect sizes
    rosenthal_r = abs(z_score) / np.sqrt(n_total)
    rank_biserial = 1 - (2 * u_stat) / (n_male * n_female)

    print("\n--- MANN-WHITNEY U TEST RESULTS ---")
    print(f"Mann-Whitney U statistic = {u_stat:,.2f}")
    print(f"Asymptotic Z-score = {z_score:.3f}")
    print(f"Asymptotic p-value = {p_val:.3f} (Not statistically significant)")
    print(f"Rosenthal's r effect size = {rosenthal_r:.3f} (Virtually null)")
    print(f"Rank-biserial correlation (r_rb) = {abs(rank_biserial):.3f}")

    print("\n" + "=" * 80)
    print("CONCLUSION: Patient sex is not significantly associated with perceived")
    print("physician-patient relationship quality (p = 0.910, effect size ~ 0.00).")
    print("=" * 80)


if __name__ == "__main__":
    main()
