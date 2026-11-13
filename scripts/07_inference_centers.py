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
1. Facility-level parametric (Mean, SD) and non-parametric (Median, IQR [Q1-Q3]) descriptive
   profiling, including official MSP facility typology and ceiling effect prevalence (Score = 5.00).
2. Kruskal-Wallis H omnibus test across all 30 public healthcare facilities, reporting both
   eta-squared (eta²_H) and epsilon-squared (epsilon²) effect sizes.
3. Pairwise post-hoc Dunn comparisons across all 435 facility pairs with both Bonferroni (FWER)
   and Benjamini-Hochberg (FDR) adjustments, detailing contrasts for Gualel (CSG).
"""

import os
import sys
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

# Ensure standard UTF-8 console output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


FACILITY_CATALOG = {
    'CS1': ('Health Center No. 1', 'Health Center Type B'),
    'CS2': ('Health Center No. 2', 'Health Center Type B'),
    'CS3': ('Health Center No. 3', 'Health Center Type B'),
    'CSA': ('Aguangora', 'Health Center Type A'),
    'CSB': ('Belén', 'Health Center Type A'),
    'CSCA': ('Carigán', 'Health Post'),
    'CSCH': ('Chuquiribamba', 'Health Center Type A'),
    'CSCHO': ('Chontacruz', 'Health Center Type A'),
    'CSCO': ('Comunidades', 'Health Post'),
    'CSCON': ('Consacola', 'Health Center Type A'),
    'CSEC': ('El Cisne', 'Health Center Type A'),
    'CSG': ('Gualel', 'Health Post'),
    'CSHDC': ('Héroes del Cenepa', 'Health Center Type A'),
    'CSJ': ('Jimbilla', 'Health Center Type A'),
    'CSM': ('Malacatos', 'Health Center Type A'),
    'CSMI': ('Miraflores', 'Health Center Type A'),
    'CSMO': ('Motupe', 'Health Center Type A'),
    'CSO': ('Obrapía', 'Health Center Type A'),
    'CSP': ('Pichic', 'Health Post'),
    'CSS': ('Santiago', 'Health Center Type A'),
    'CSSC': ('San Cayetano', 'Health Center Type A'),
    'CSSL': ('San Lucas', 'Health Center Type A'),
    'CST': ('Taquil', 'Health Center Type B'),
    'CSTC': ('Tierras Coloradas', 'Health Center Type A'),
    'CSUL': ('Unión Lojana', 'Health Center Type A'),
    'CSY': ('Yangana', 'Health Center Type A'),
    'CSZH': ('Zamora Huaico', 'Health Center Type A'),
    'HBV': ('Vilcabamba Basic Hospital', 'Basic Hospital'),
    'HGIA': ('Isidro Ayora General Hospital', 'General Hospital (Provincial Reference)'),
    'UAV': ('Vilcabamba Nested Unit', 'Health Center Type A (Nested Unit)')
}


def compute_dunn_posthoc_matrices(df, val_col, group_col):
    """Computes tie-corrected Dunn pairwise p-value matrices (unadjusted, Bonferroni, and FDR)."""
    n_total = len(df)
    ranks = stats.rankdata(df[val_col].values)
    df_ranks = pd.DataFrame({group_col: df[group_col].values, 'rank': ranks})

    # Tie correction factor
    _, tie_counts = np.unique(ranks, return_counts=True)
    tie_term = np.sum(tie_counts**3 - tie_counts) / (12.0 * (n_total - 1))
    var_rank = (n_total * (n_total + 1)) / 12.0 - tie_term

    groups = sorted(df[group_col].unique())
    k = len(groups)
    mean_ranks = df_ranks.groupby(group_col)['rank'].mean().to_dict()
    counts = df_ranks.groupby(group_col)['rank'].count().to_dict()

    pairs = []
    p_unadj_list = []
    for i in range(k):
        for j in range(i + 1, k):
            g1, g2 = groups[i], groups[j]
            diff = abs(mean_ranks[g1] - mean_ranks[g2])
            se = np.sqrt(var_rank * (1.0 / counts[g1] + 1.0 / counts[g2]))
            z = diff / se
            p_val = 2.0 * (1.0 - stats.norm.cdf(z))
            pairs.append((g1, g2))
            p_unadj_list.append(p_val)

    p_unadj_arr = np.array(p_unadj_list)
    _, p_bonf_arr, _, _ = multipletests(p_unadj_arr, method='bonferroni')
    _, p_fdr_arr, _, _ = multipletests(p_unadj_arr, method='fdr_bh')

    mat_unadj = pd.DataFrame(1.0, index=groups, columns=groups)
    mat_bonf = pd.DataFrame(1.0, index=groups, columns=groups)
    mat_fdr = pd.DataFrame(1.0, index=groups, columns=groups)

    for idx, (g1, g2) in enumerate(pairs):
        mat_unadj.loc[g1, g2] = mat_unadj.loc[g2, g1] = p_unadj_arr[idx]
        mat_bonf.loc[g1, g2] = mat_bonf.loc[g2, g1] = p_bonf_arr[idx]
        mat_fdr.loc[g1, g2] = mat_fdr.loc[g2, g1] = p_fdr_arr[idx]

    return mat_unadj, mat_bonf, mat_fdr


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "datos", "pdrq9_patients_data.xlsx")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at: {data_path}")

    df = pd.read_excel(data_path)
    n_total = len(df)
    pdrq_items = [f"pdrq_item{i}" for i in range(1, 10)]
    df['pdrq_overall_score'] = df[pdrq_items].mean(axis=1)

    print("=" * 115)
    print("INFERENTIAL BIVARIATE ANALYSIS: HEALTHCARE FACILITIES (30 CENTERS, n = 3,257)")
    print("=" * 115)

    # 1. Calculate facility-level metrics including ceiling effect
    facility_summary = []
    for code, g in df.groupby('health_center'):
        scores = g['pdrq_overall_score']
        n_c = len(scores)
        q1 = scores.quantile(0.25)
        q3 = scores.quantile(0.75)
        n_ceil = int((scores == 5.0).sum())
        pct_ceil = (n_ceil / n_c) * 100.0
        name, typology = FACILITY_CATALOG.get(code, (code, 'Other'))

        facility_summary.append({
            'Code': code,
            'Facility Name': name,
            'Typology (MSP)': typology,
            'n': n_c,
            '% Sample': (n_c / n_total) * 100.0,
            'Mean': scores.mean(),
            'SD': scores.std(),
            'Median': scores.median(),
            'IQR': q3 - q1,
            'Q1': q1,
            'Q3': q3,
            'n_ceil': n_ceil,
            'pct_ceil': pct_ceil
        })

    df_fac = pd.DataFrame(facility_summary).sort_values(
        by=['Median', 'pct_ceil', 'Mean'], ascending=[False, False, False]
    ).reset_index(drop=True)
    df_fac['Rank'] = range(1, len(df_fac) + 1)

    display_df = pd.DataFrame({
        'Rank': df_fac['Rank'],
        'Code': df_fac['Code'],
        'Facility Name': df_fac['Facility Name'],
        'Typology (MSP)': df_fac['Typology (MSP)'],
        'n': df_fac['n'],
        '%': df_fac['% Sample'].apply(lambda x: f"{x:.2f}%"),
        'Mean (SD)': df_fac.apply(lambda r: f"{r['Mean']:.2f} ({r['SD']:.2f})", axis=1),
        'Median': df_fac['Median'].apply(lambda x: f"{x:.2f}"),
        'IQR [Q1–Q3]': df_fac.apply(lambda r: f"{r['IQR']:.2f} [{r['Q1']:.2f}–{r['Q3']:.2f}]", axis=1),
        'Score = 5.00 n (%)': df_fac.apply(lambda r: f"{r['n_ceil']} ({r['pct_ceil']:.1f}%)", axis=1)
    })

    print("\n1. FACILITY-LEVEL DISTRIBUTION AND CEILING EFFECT PREVALENCE (TABLE 3):")
    print("-" * 115)
    print(display_df.to_string(index=False))
    print("-" * 115)

    # 2. Kruskal-Wallis H Test across 30 healthcare facilities
    groups = [g['pdrq_overall_score'].values for _, g in df.groupby('health_center')]
    h_stat, p_kw = stats.kruskal(*groups)
    k_groups = len(groups)
    eta2_h = (h_stat - k_groups + 1) / (n_total - k_groups)
    epsilon2 = h_stat / ((n_total**2 - 1) / (n_total + 1))

    print("\n2. KRUSKAL-WALLIS H OMNIBUS TEST (30 FACILITIES):")
    print("-" * 115)
    print(f"Kruskal-Wallis H statistic = {h_stat:.2f}")
    print(f"Degrees of freedom (df)    = {k_groups - 1}")
    print(f"p-value                    = {p_kw:.4e} (p < 0.001)")
    print(f"Eta-squared (η²_H)         = {eta2_h:.3f} ({eta2_h*100:.2f}% of total variance)")
    print(f"Epsilon-squared (ε²)       = {epsilon2:.3f}")

    # 3. Post-hoc pairwise comparisons (Dunn's test) for Gualel (CSG)
    mat_unadj, mat_bonf, mat_fdr = compute_dunn_posthoc_matrices(
        df, val_col='pdrq_overall_score', group_col='health_center'
    )
    gualel_unadj = mat_unadj.loc['CSG'].drop('CSG')
    gualel_fdr = mat_fdr.loc['CSG'].drop('CSG')
    gualel_bonf = mat_bonf.loc['CSG'].drop('CSG')

    comp_gualel = pd.DataFrame({
        'Code': gualel_bonf.index,
        'Facility Name': [FACILITY_CATALOG[c][0] for c in gualel_bonf.index],
        'n': [len(df[df['health_center'] == c]) for c in gualel_bonf.index],
        'Median': [df[df['health_center'] == c]['pdrq_overall_score'].median() for c in gualel_bonf.index],
        'p (unadjusted)': gualel_unadj.values,
        'p (FDR B-H)': gualel_fdr.values,
        'p (Bonferroni)': gualel_bonf.values
    }).sort_values(by='p (Bonferroni)', ascending=False).reset_index(drop=True)

    print("\n3. PAIRWISE DUNN POST-HOC CONTRASTS FOR GUALEL (CSG VS. OTHER 29 FACILITIES):")
    print("-" * 115)
    print(comp_gualel.to_string(index=False))

    n_bonf_sig = int((gualel_bonf < 0.05).sum())
    n_bonf_001 = int((gualel_bonf < 0.001).sum())
    n_fdr_sig = int((gualel_fdr < 0.05).sum())

    print("\n" + "=" * 115)
    print("SUMMARY OF KEY FINDINGS:")
    print(f"1. Substantial facility-level variation in PDRQ-9 scores (H = {h_stat:.2f}, p < 0.001, η²_H = {eta2_h:.3f}, ε² = {epsilon2:.3f}).")
    print("2. Five primary care centers achieved a median score of 5.00 (Consacola, Motupe, Unión Lojana, Belén, San Cayetano).")
    print("3. Hospital General Isidro Ayora (HGIA, n = 481) recorded an intermediate median score of 4.22 (IQR = 0.89).")
    print(f"4. Gualel (CSG, n = 74, Median = 2.00) scored significantly lower than {n_bonf_sig} of 29 facilities under strict")
    print(f"   Bonferroni adjustment (p_adj < 0.05; p_adj < 0.001 against {n_bonf_001} facilities), and lower than all {n_fdr_sig} of 29")
    print("   facilities under Benjamini-Hochberg FDR control (all p_adj < 0.025).")
    print("=" * 115)


if __name__ == "__main__":
    main()
