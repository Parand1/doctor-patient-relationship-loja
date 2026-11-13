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
covariance adjustment evaluating factors associated with the perceived physician-patient
relationship (PDRQ-9 Overall Mean Score):
  1. Model 1 (Sociodemographic): Evaluates the joint association of Sex, Age Group, and
     Marital Status using conventional ordinary least squares (OLS).
  2. Model 2 (Facility-Adjusted Fixed Effects + Cluster-Robust SEs): Incorporates institutional
     fixed-effect indicators across all 30 healthcare facilities (29 indicator variables) and
     estimates standard errors using the Huber-White cluster-robust sandwich covariance
     estimator (CRV1, G = 30 clusters) with the finite-sample degrees-of-freedom correction
     [G / (G - 1)] * [(N - 1) / (N - k)] (G = 30, N = 3,257, k = 39) and the standard normal (z)
     reference distribution.
  3. Model fit comparison between Model 1 and Model 2 is evaluated descriptively via R²
     (from 2.89% to 35.66%, ΔR² = +32.77 percentage points) and adjusted R² (from 2.62% to 34.90%).
Outputs:
  - Console: Complete statistical output for Model 1 and Model 2, exact covariance specification,
    z-statistics, two-tailed p-values, 95% CIs, and descriptive R² comparison.
  - Table generation: Run 08_multivariable_table.py to export Table 4 to Excel.
"""

import os
import sys
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

# Ensure standard UTF-8 console output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def run_multivariable_model(data_path):
    print("=" * 105)
    print("HIERARCHICAL MULTIVARIABLE MODELING & INSTITUTIONAL CLUSTER-ROBUST ADJUSTMENT (TABLE 4)")
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
    # MODEL 1: SOCIODEMOGRAPHIC REGRESSION (CONVENTIONAL OLS)
    # =========================================================================
    print("-" * 105)
    print("MODEL 1: INDIVIDUAL SOCIODEMOGRAPHIC FACTORS (CONVENTIONAL OLS, UNADJUSTED FOR FACILITIES)")
    print("-" * 105)
    formula_m1 = "pdrq9_score ~ sex_cat + age_cat + marital_cat"
    model_m1 = smf.ols(formula_m1, data=df).fit()

    r2_m1 = model_m1.rsquared
    r2_adj_m1 = model_m1.rsquared_adj
    f_stat_m1 = model_m1.fvalue
    p_f_m1 = model_m1.f_pvalue

    print(f"R²          = {r2_m1:.4f} ({r2_m1 * 100:.2f}%)")
    print(f"Adjusted R² = {r2_adj_m1:.4f} ({r2_adj_m1 * 100:.2f}%)")
    print(f"Overall Model F-test: F({model_m1.df_model:.0f}, {model_m1.df_resid:.0f}) = {f_stat_m1:.2f}, p = {p_f_m1:.4e}")
    print("\nModel 1 Parameter Estimates:")
    summary_m1 = model_m1.summary2().tables[1]
    summary_m1.columns = ['Coef (β)', 'Std Err', 't', 'p-value', '95% CI Lower', '95% CI Upper']
    print(summary_m1.round(4).to_string())

    # =========================================================================
    # MODEL 2: FACILITY FIXED EFFECTS + HUBER-WHITE CLUSTER-ROBUST SE (CRV1)
    # =========================================================================
    print("\n" + "-" * 105)
    print("MODEL 2: FACILITY-ADJUSTED FIXED EFFECTS + HUBER-WHITE CLUSTER-ROBUST SE (CRV1, G = 30)")
    print("-" * 105)
    formula_m2 = "pdrq9_score ~ sex_cat + age_cat + marital_cat + center_cat"
    model_m2 = smf.ols(formula_m2, data=df).fit(
        cov_type='cluster',
        cov_kwds={'groups': df['health_center'], 'use_correction': True, 'use_t': False}
    )

    G = df['health_center'].nunique()
    k_params = len(model_m2.params)
    finite_sample_factor = (G / (G - 1)) * ((total_n - 1) / (total_n - k_params))

    r2_m2 = model_m2.rsquared
    r2_adj_m2 = model_m2.rsquared_adj
    delta_r2 = r2_m2 - r2_m1

    print("Covariance & Inference Specification:")
    print(f"  - Estimator:                Huber-White cluster-robust sandwich estimator (CRV1)")
    print(f"  - Clustering variable:      Healthcare facility (G = {G} clusters)")
    print(f"  - Sample & parameter count: N = {total_n:,} observations, k = {k_params} parameters")
    print(f"  - Finite-sample correction: [G / (G - 1)] * [(N - 1) / (N - k)] = ({G}/{G-1}) * ({total_n-1}/{total_n-k_params}) = {finite_sample_factor:.5f}")
    print("  - Reference distribution:   Standard normal (z) distribution")

    print("\nModel Fit & Descriptive Comparison:")
    print(f"  - Model 1 R²:               {r2_m1 * 100:.2f}% (Adjusted R² = {r2_adj_m1 * 100:.2f}%)")
    print(f"  - Model 2 R²:               {r2_m2 * 100:.2f}% (Adjusted R² = {r2_adj_m2 * 100:.2f}%)")
    print(f"  - Incremental ΔR²:          +{delta_r2 * 100:.2f} percentage points in explained variance")

    sociodemo_keys = [k for k in model_m1.params.index]
    ci_m2 = model_m2.conf_int()
    summary_m2_socio = pd.DataFrame({
        'Coef (β)': model_m2.params[sociodemo_keys],
        'Cluster SE (CRV1)': model_m2.bse[sociodemo_keys],
        'z': model_m2.tvalues[sociodemo_keys],
        'p-value': model_m2.pvalues[sociodemo_keys],
        '95% CI Lower': ci_m2.loc[sociodemo_keys, 0],
        '95% CI Upper': ci_m2.loc[sociodemo_keys, 1]
    })

    print("\nModel 2 Sociodemographic Parameter Estimates (Adjusted for 30 Healthcare Facilities):")
    print(summary_m2_socio.round(4).to_string())

    # =========================================================================
    # PARAMETER INTERPRETATION REPORT
    # =========================================================================
    print("\n" + "=" * 105)
    print("SUMMARY OF FACILITY-ADJUSTED SOCIODEMOGRAPHIC PARAMETERS (MODEL 2, CRV1):")
    print("=" * 105)

    def format_param_report(param_key, label, ref_label):
        beta = model_m2.params[param_key]
        z = model_m2.tvalues[param_key]
        p = model_m2.pvalues[param_key]
        ci_l = ci_m2.loc[param_key, 0]
        ci_u = ci_m2.loc[param_key, 1]
        p_str = "< 0.001" if p < 0.001 else f"= {p:.3f}"
        sig_str = "Statistically Significant (p < 0.05)" if p < 0.05 else "Not Significant (p >= 0.05)"
        return f"   - {label} (vs {ref_label}): β = {beta:+.3f}, 95% CI: [{ci_l:+.3f}, {ci_u:+.3f}], z = {z:.2f}, p {p_str} [{sig_str}]"

    print("A. Biological Sex:")
    print(format_param_report('sex_cat[T.Female]', 'Female', 'Male'))

    print("\nB. Age Groups (Reference: 18–30 years):")
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

    print("\nD. Model Fit Summary:")
    print(f"   - Adding healthcare facility indicators increased the model R² from {r2_m1 * 100:.2f}% to {r2_m2 * 100:.2f}%")
    print(f"     (adjusted R² from {r2_adj_m1 * 100:.2f}% to {r2_adj_m2 * 100:.2f}%), corresponding to an increase of")
    print(f"     {delta_r2 * 100:.2f} percentage points in explained variance.")
    print("=" * 105)


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(base_dir, "datos", "pdrq9_patients_data.xlsx")
    run_multivariable_model(data_file)
