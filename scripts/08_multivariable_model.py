"""
Study: Associated factors of the doctor-patient relationship: An Analysis of Healthcare Users in Loja
Script: 08_multivariable_model.py
Lead Data Analysis & Code: Pablo Andrés Japón Calva (ORCID: 0009-0001-0705-8120)
Study Co-Investigators: Ruth Maldonado-Rengel, et al.
Affiliations:
  - Independent Researcher, Loja, Ecuador
  - Facultad de Ciencias de la Salud, Universidad Técnica Particular de Loja (UTPL), Loja, Ecuador

Description:
Computes the two-stage hierarchical multivariable linear regression and cluster-robust
covariance adjustment evaluating factors associated with perceived physician-patient
relationship quality (PDRQ-9 Overall Mean Score):
  1. Model 1 (Sociodemographic): Evaluates joint impact of Sex, Age cohort, and Marital Status.
  2. Model 2 (Facility-Adjusted Fixed Effects): Adds 30 healthcare facilities to quantify
     incremental explained variance (Delta R²) and nested ANOVA F-change test.
  3. Model 3 (Cluster-Robust Standard Errors): Formally adjusts standard errors for institutional
     clustering across all 30 healthcare facilities using Huber-White cluster-robust covariance.
Outputs:
  - Console: Complete statistical output for all models, parameter tables, ANOVA F-change,
    cluster-robust standard errors, z-scores, p-values, 95% CIs, and variance decomposition.
  - Table generation: Run 08_multivariable_table.py to export Table 3 to Excel.
"""

import os
import sys
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Ensure standard UTF-8 console output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def run_multivariable_model(data_path):
    print("=" * 105)
    print("HIERARCHICAL MULTIVARIABLE MODELING & INSTITUTIONAL CLUSTER-ROBUST ADJUSTMENT")
    print("=" * 105)

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at: {data_path}")

    df = pd.read_excel(data_path)
    total_n = len(df)
    print(f"Analytical sample size: n = {total_n:,} patients across 30 healthcare facilities.\n")

    pdrq_items = [f"pdrq_item{i}" for i in range(1, 10)]
    df['pdrq9_score'] = df[pdrq_items].mean(axis=1)

    # Categorical recoding with explicit reference levels matching manuscript
    sex_map = {1: 'Male (Ref)', 2: 'Female'}
    age_map = {
        1: '18–30 years (Ref)',
        2: '31–40 years',
        3: '41–50 years',
        4: '51–60 years',
        5: 'Over 60 years'
    }
    marital_map = {
        1: 'Married (Ref)',
        2: 'Divorced',
        3: 'Widowed',
        4: 'Single',
        5: 'Common-law union'
    }

    df['sex_cat'] = pd.Categorical(
        df['sex'].map(sex_map),
        categories=['Male (Ref)', 'Female'],
        ordered=False
    )
    df['age_cat'] = pd.Categorical(
        df['age_group'].map(age_map),
        categories=['18–30 years (Ref)', '31–40 years', '41–50 years', '51–60 years', 'Over 60 years'],
        ordered=False
    )
    df['marital_cat'] = pd.Categorical(
        df['marital_status'].map(marital_map),
        categories=['Married (Ref)', 'Single', 'Common-law union', 'Divorced', 'Widowed'],
        ordered=False
    )
    df['center_cat'] = pd.Categorical(df['health_center'].astype(str))

    # =========================================================================
    # MODEL 1: SOCIODEMOGRAPHIC REGRESSION (WITHOUT INSTITUTIONAL ADJUSTMENT)
    # =========================================================================
    print("-" * 105)
    print("MODEL 1: INDIVIDUAL SOCIODEMOGRAPHIC FACTORS (OLS UNADJUSTED FOR FACILITIES)")
    print("-" * 105)
    formula_m1 = "pdrq9_score ~ sex_cat + age_cat + marital_cat"
    model_m1 = smf.ols(formula_m1, data=df).fit()

    r2_m1 = model_m1.rsquared
    r2_adj_m1 = model_m1.rsquared_adj
    f_stat_m1 = model_m1.fvalue
    p_f_m1 = model_m1.f_pvalue

    print(f"R² = {r2_m1:.4f} ({r2_m1 * 100:.2f}% of total variance explained)")
    print(f"Adjusted R² = {r2_adj_m1:.4f}")
    print(f"Overall Model F-test: F({model_m1.df_model:.0f}, {model_m1.df_resid:.0f}) = {f_stat_m1:.2f}, p = {p_f_m1:.4e}")
    print("\nModel 1 Parameter Estimates:")
    summary_m1 = model_m1.summary2().tables[1]
    summary_m1.columns = ['Coef (β)', 'Std Err', 't', 'p-value', '95% CI Lower', '95% CI Upper']
    print(summary_m1.round(4).to_string())

    # =========================================================================
    # MODEL 2: FACILITY FIXED EFFECTS (FULL INSTITUTIONAL MODEL)
    # =========================================================================
    print("\n" + "-" * 105)
    print("MODEL 2: COMPLETE MODEL WITH INSTITUTIONAL FIXED EFFECTS (SOCIODEMOGRAPHIC + HEALTH CENTERS)")
    print("-" * 105)
    formula_m2 = "pdrq9_score ~ sex_cat + age_cat + marital_cat + center_cat"
    model_m2 = smf.ols(formula_m2, data=df).fit()

    r2_m2 = model_m2.rsquared
    r2_adj_m2 = model_m2.rsquared_adj
    delta_r2 = r2_m2 - r2_m1
    pct_var_centers = (delta_r2 / r2_m2) * 100

    # Nested ANOVA comparison (F-test for Delta R²)
    anova_comp = sm.stats.anova_lm(model_m1, model_m2)
    f_change = anova_comp['F'].iloc[1]
    p_f_change = anova_comp['Pr(>F)'].iloc[1]

    print(f"Complete Model R² = {r2_m2:.4f} ({r2_m2 * 100:.2f}% of total variance explained)")
    print(f"Adjusted R² = {r2_adj_m2:.4f}")
    print(f"Incremental Explained Variance (ΔR²): {delta_r2:.4f} ({delta_r2 * 100:.2f}% variance gain from facilities)")
    print(f"Proportion of explainable variance attributable to centers: {pct_var_centers:.2f}%")
    print(f"Nested ANOVA F-change Test: F({model_m2.df_model - model_m1.df_model:.0f}, {model_m2.df_resid:.0f}) = {f_change:.2f}, p = {p_f_change:.4e}")

    print("\nModel 2 Parameter Estimates (Sociodemographic Factors and Facility Fixed Effects):")
    summary_m2 = model_m2.summary2().tables[1]
    summary_m2.columns = ['Coef (β)', 'Std Err', 't', 'p-value', '95% CI Lower', '95% CI Upper']
    print(summary_m2.round(4).to_string())

    # =========================================================================
    # MODEL 3: CLUSTER-ROBUST STANDARD ERRORS (ACCOUNTING FOR 30 FACILITIES)
    # =========================================================================
    print("\n" + "=" * 105)
    print("MODEL 3: CLUSTER-ROBUST STANDARD ERRORS (HUBER-WHITE CLUSTER COVARIANCE ADJUSTMENT)")
    print("Formal correction for nested patient clustering across all 30 healthcare facilities")
    print("=" * 105)

    model_m3 = smf.ols(formula_m1, data=df).fit(
        cov_type='cluster',
        cov_kwds={'groups': df['health_center']}
    )

    ci_m3 = model_m3.conf_int()
    summary_m3 = pd.DataFrame({
        'Coef (β)': model_m3.params,
        'Cluster SE': model_m3.bse,
        'z': model_m3.tvalues,
        'p-value': model_m3.pvalues,
        '95% CI Lower': ci_m3[0],
        '95% CI Upper': ci_m3[1]
    })
    print(summary_m3.round(4).to_string())

    # =========================================================================
    # PARAMETER INTERPRETATION REPORT
    # =========================================================================
    print("\n" + "=" * 105)
    print("SUMMARY OF ADJUSTED PARAMETERS (CLUSTER-ROBUST ESTIMATION):")
    print("=" * 105)

    def format_param_report(param_key, label, ref_label):
        beta = model_m3.params[param_key]
        se = model_m3.bse[param_key]
        z = model_m3.tvalues[param_key]
        p = model_m3.pvalues[param_key]
        ci_l = ci_m3.loc[param_key, 0]
        ci_u = ci_m3.loc[param_key, 1]
        p_str = "< 0.001" if p < 0.001 else f"= {p:.4f}"
        sig_str = "Statistically Significant (p < 0.05)" if p < 0.05 else "Not Significant (p >= 0.05)"
        return f"   - {label} (vs {ref_label}): β = {beta:+.4f}, 95% CI: [{ci_l:+.4f}, {ci_u:+.4f}], z = {z:.2f}, p {p_str} [{sig_str}]"

    print("A. Biological Sex:")
    print(format_param_report('sex_cat[T.Female]', 'Female', 'Male'))

    print("\nB. Age Cohorts (Reference: 18–30 years):")
    for age_key, age_lbl in [
        ('age_cat[T.31–40 years]', '31–40 years'),
        ('age_cat[T.41–50 years]', '41–50 years'),
        ('age_cat[T.51–60 years]', '51–60 years'),
        ('age_cat[T.Over 60 years]', 'Over 60 years')
    ]:
        print(format_param_report(age_key, age_lbl, '18–30 years'))

    print("\nC. Marital Status (Reference: Married):")
    for civ_key, civ_lbl in [
        ('marital_cat[T.Single]', 'Single'),
        ('marital_cat[T.Common-law union]', 'Common-law union'),
        ('marital_cat[T.Divorced]', 'Divorced'),
        ('marital_cat[T.Widowed]', 'Widowed')
    ]:
        print(format_param_report(civ_key, civ_lbl, 'Married'))

    print("\nD. Variance Decomposition Summary:")
    print(f"   - Model 1 R² (Individual Sociodemographic factors): {r2_m1 * 100:.2f}%")
    print(f"   - Model 2 R² (Complete with Healthcare Facilities): {r2_m2 * 100:.2f}%")
    print(f"   - Institutional Variance Gain (ΔR²): {delta_r2 * 100:.2f}% (F = {f_change:.2f}, p < 0.001)")
    print(f"   - Proportion of total explainable variance attributable to facilities: {pct_var_centers:.2f}%")
    print("=" * 105)


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(base_dir, "datos", "pdrq9_patients_data.xlsx")
    run_multivariable_model(data_file)
