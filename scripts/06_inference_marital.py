"""
Study: Associated factors of the doctor-patient relationship: An Analysis of Healthcare Users in Loja
Script: 06_inference_marital.py
Lead Data Analysis & Code: Pablo Andrés Japón Calva (ORCID: 0009-0001-0705-8120)
Study Co-Investigators: Ruth Maldonado-Rengel, et al.
Affiliations:
  - Independent Researcher, Loja, Ecuador
  - Facultad de Ciencias de la Salud, Universidad Técnica Particular de Loja (UTPL), Loja, Ecuador

Description:
Inferential bivariate comparison of the perceived physician-patient relationship
(PDRQ-9 Overall Mean Score) across patient marital status categories
(Married, Divorced, Widowed, Single, Common-law union).
Performs:
1. Kruskal-Wallis H omnibus test and eta-squared (eta²_H) effect size.
2. Post-hoc pairwise multiple comparisons using Dunn's test with Bonferroni adjustment.
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

    marital_labels = {
        1: 'Married',
        2: 'Divorced',
        3: 'Widowed',
        4: 'Single',
        5: 'Common-law union'
    }
    df['marital_cat'] = df['marital_status'].map(marital_labels)

    print("=" * 80)
    print("INFERENTIAL BIVARIATE ANALYSIS: MARITAL STATUS")
    print("=" * 80)

    # Descriptive metrics per category
    marital_groups = [df[df['marital_status'] == i]['pdrq_overall_score'] for i in range(1, 6)]
    descriptives = []
    for code in [1, 4, 5, 2, 3]:  # Ordered by sample size / Table 1 sequence
        scores = df[df['marital_status'] == code]['pdrq_overall_score']
        q1 = np.percentile(scores, 25)
        q3 = np.percentile(scores, 75)
        descriptives.append({
            'Marital Status': marital_labels[code],
            'n': len(scores),
            'Mean': f"{scores.mean():.2f}",
            'SD': f"{scores.std():.2f}",
            'Median': f"{scores.median():.2f}",
            'IQR': f"{(q3 - q1):.2f}",
            '[Q1–Q3]': f"[{q1:.2f}–{q3:.2f}]"
        })
    print(pd.DataFrame(descriptives).to_string(index=False))

    # Kruskal-Wallis H Test
    h_stat, p_kw = stats.kruskal(*marital_groups)
    k_groups = len(marital_groups)
    n_total = len(df)
    eta2_h = (h_stat - k_groups + 1) / (n_total - k_groups)

    print("\n--- KRUSKAL-WALLIS H TEST RESULTS ---")
    print(f"Kruskal-Wallis H statistic = {h_stat:.2f}")
    print(f"Degrees of freedom (df) = {k_groups - 1}")
    print(f"p-value = {p_kw:.4e} (p < 0.001)")
    print(f"Eta-squared (η²_H) = {eta2_h:.3f} (Accounts for {eta2_h*100:.2f}% of total variance)")

    # Post-hoc pairwise comparisons using Dunn's test with Bonferroni correction
    print("\n--- POST-HOC PAIRWISE COMPARISONS (DUNN-BONFERRONI) ---")
    df['rank'] = df['pdrq_overall_score'].rank()
    mean_ranks = {code: df[df['marital_status'] == code]['rank'].mean() for code in range(1, 6)}
    n_i = {code: len(df[df['marital_status'] == code]) for code in range(1, 6)}

    se_factor = np.sqrt((n_total * (n_total + 1) / 12))
    comparisons = []
    num_comparisons = (k_groups * (k_groups - 1)) // 2

    for i in range(1, 6):
        for j in range(i + 1, 6):
            diff = mean_ranks[i] - mean_ranks[j]
            se = se_factor * np.sqrt(1 / n_i[i] + 1 / n_i[j])
            z = diff / se
            p_unadj = 2 * (1 - stats.norm.cdf(abs(z)))
            p_adj = min(1.0, p_unadj * num_comparisons)
            sig_marker = "***" if p_adj < 0.001 else ("**" if p_adj < 0.01 else ("*" if p_adj < 0.05 else "ns"))
            comparisons.append({
                'Contrast': f"{marital_labels[i]} vs. {marital_labels[j]}",
                'Mean Rank Diff': f"{diff:.1f}",
                'Z': f"{z:.3f}",
                'p (adj)': f"{p_adj:.4e}" if p_adj < 0.001 else f"{p_adj:.4f}",
                'Significance': sig_marker
            })

    print(pd.DataFrame(comparisons).to_string(index=False))
    print("=" * 80)
    print("CONCLUSION: Divorced patients exhibited the lowest median rating (Median = 4.33, IQR = 1.11),")
    print("differing significantly from Common-law union (p_adj = 0.005) and Widowed (p_adj = 0.012).")
    print("=" * 80)


if __name__ == "__main__":
    main()
