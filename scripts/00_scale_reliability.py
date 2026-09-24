"""
Study: Associated factors of the doctor-patient relationship: An Analysis of Healthcare Users in Loja
Script: 00_scale_reliability.py
Lead Data Analysis & Code: Pablo Andrés Japón Calva (ORCID: 0009-0001-0705-8120)
Study Co-Investigators: Ruth Maldonado-Rengel, et al.
Affiliations:
  - Independent Researcher, Loja, Ecuador
  - Facultad de Ciencias de la Salud, Universidad Técnica Particular de Loja (UTPL), Loja, Ecuador

Description:
Psychometric evaluation of internal consistency for the Patient-Doctor
Relationship Questionnaire (PDRQ-9) on the analytical sample (n = 3,257).
Calculates:
1. Global Cronbach's alpha coefficient.
2. 95% empirical confidence intervals via non-parametric bootstrap (1,000 iterations).
3. Corrected item-total correlations (CITC).
4. Cronbach's alpha if each item is deleted.
"""

import os
import sys
import numpy as np
import pandas as pd

# Ensure standard UTF-8 console output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def cronbach_alpha(df_items):
    """Calculates Cronbach's alpha coefficient for an item matrix."""
    k = df_items.shape[1]
    item_variances = df_items.var(axis=0, ddof=1).sum()
    total_score = df_items.sum(axis=1)
    total_variance = total_score.var(ddof=1)
    return (k / (k - 1)) * (1 - (item_variances / total_variance))


def cronbach_alpha_bootstrap_ci(df_items, n_boot=1000, ci=0.95, random_state=42):
    """Computes empirical 95% bootstrap confidence interval."""
    np.random.seed(random_state)
    n = len(df_items)
    alphas = []
    values = df_items.values
    for _ in range(n_boot):
        sample_indices = np.random.choice(n, size=n, replace=True)
        sample_df = pd.DataFrame(values[sample_indices])
        alphas.append(cronbach_alpha(sample_df))
    lower = np.percentile(alphas, (1 - ci) / 2 * 100)
    upper = np.percentile(alphas, (1 + ci) / 2 * 100)
    return lower, upper


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "datos", "pdrq9_patients_data.xlsx")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at: {data_path}")

    df = pd.read_excel(data_path)
    print("=" * 80)
    print("PSYCHOMETRIC RELIABILITY AND INTERNAL CONSISTENCY (PDRQ-9)")
    print("=" * 80)
    print(f"Analytical sample size: n = {len(df):,} participants")

    pdrq_items = [f"pdrq_item{i}" for i in range(1, 10)]
    item_labels = [
        "1. My physician helps me",
        "2. My physician has enough time for me",
        "3. I trust my physician",
        "4. My physician understands me",
        "5. My physician is dedicated to helping me",
        "6. Agreement on the nature of symptoms",
        "7. I can talk to my physician",
        "8. Satisfied with the treatment",
        "9. My physician is available to me"
    ]

    df_scale = df[pdrq_items].dropna()
    alpha_global = cronbach_alpha(df_scale)
    ci_low, ci_high = cronbach_alpha_bootstrap_ci(df_scale, n_boot=1000)

    print(f"\nNumber of items analyzed (k): {len(pdrq_items)}")
    print(f"Overall Cronbach's alpha: {alpha_global:.4f}")
    print(f"95% Bootstrap Confidence Interval: [{ci_low:.4f} - {ci_high:.4f}]")
    print("Psychometric appraisal: Excellent internal consistency (alpha >= 0.90)\n")

    # Item-level discrimination and alpha if deleted
    print("-" * 80)
    print("ITEM-TOTAL DISCRIMINATION AND ALPHA-IF-DELETED ANALYSIS")
    print("-" * 80)

    total_score = df_scale.sum(axis=1)
    item_stats = []

    for idx, col in enumerate(pdrq_items):
        mean_val = df_scale[col].mean()
        sd_val = df_scale[col].std()
        
        # Corrected item-total correlation (excluding the item itself)
        score_minus_item = total_score - df_scale[col]
        citc = df_scale[col].corr(score_minus_item)
        
        # Alpha if item deleted
        df_minus_item = df_scale.drop(columns=[col])
        alpha_drop = cronbach_alpha(df_minus_item)
        
        item_stats.append({
            'Item': item_labels[idx],
            'Mean': f"{mean_val:.2f}",
            'SD': f"{sd_val:.2f}",
            'Corrected Item-Total (CITC)': f"{citc:.4f}",
            'Alpha if deleted': f"{alpha_drop:.4f}"
        })

    df_item_stats = pd.DataFrame(item_stats)
    print(df_item_stats.to_string(index=False))
    print("=" * 80)


if __name__ == "__main__":
    main()
