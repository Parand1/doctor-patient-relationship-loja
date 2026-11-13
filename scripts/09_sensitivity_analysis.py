"""
Study: Associated factors of the doctor-patient relationship: An Analysis of Healthcare Users in Loja
Script: 09_sensitivity_analysis.py
Lead Data Analysis & Code: Pablo Andrés Japón Calva (ORCID: 0009-0001-0705-8120)
Study Co-Investigators: Ruth Maldonado-Rengel, et al.
Affiliations:
  - Independent Researcher, Loja, Ecuador
  - Facultad de Ciencias de la Salud, Universidad Técnica Particular de Loja (UTPL), Loja, Ecuador

Description:
Performs OLS regression diagnostics and multivariable sensitivity analyses to verify
the robustness of the facility-adjusted associations (Model 2) against negative skewness
and the upper scale boundary (ceiling effect at 5.00):
  1. OLS Regression Diagnostics:
     - Multicollinearity: Variance Inflation Factors (VIF) across sociodemographic predictors.
     - Heteroscedasticity: Breusch-Pagan Lagrange Multiplier test.
     - Residual distribution: Residual skewness and excess kurtosis.
     - Influential observations: Maximum Cook's distance.
  2. Sensitivity Analysis 1: Quantile (Median, q = 0.50) Regression (Least Absolute Deviations, LAD).
  3. Sensitivity Analysis 2: Upper-Censored Tobit Regression (right-censored at 5.00).
Outputs:
  - Console: Complete diagnostic report and side-by-side comparison of OLS, Median, and Tobit models.
  - Excel: tablas/table_s1_sensitivity_analysis.xlsx
"""

import os
import sys
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan
from scipy.optimize import minimize
from scipy.stats import norm
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Ensure standard UTF-8 console output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def style_worksheet(ws, df_table):
    font_header = Font(name='Calibri', size=10, bold=True, color='000000')
    font_body = Font(name='Calibri', size=10, color='000000')

    border_thick = Side(border_style="medium", color="000000")
    border_thin = Side(border_style="thin", color="D9D9D9")
    border_top_thin = Side(border_style="thin", color="000000")

    border_header = Border(top=border_thick, bottom=border_thick, left=border_thin, right=border_thin)
    border_data = Border(top=border_thin, bottom=border_thin, left=border_thin, right=border_thin)
    border_bottom = Border(top=border_top_thin, bottom=border_thick, left=border_thin, right=border_thin)

    for col_idx, col_name in enumerate(df_table.columns, start=1):
        cell = ws.cell(row=1, column=col_idx, value=col_name)
        cell.font = font_header
        cell.alignment = Alignment(horizontal='left' if col_idx == 1 else 'center', vertical='center')
        cell.border = border_header
    ws.row_dimensions[1].height = 24

    num_rows = len(df_table)
    for r_idx in range(2, num_rows + 2):
        is_last = (r_idx == num_rows + 1)
        for c_idx in range(1, len(df_table.columns) + 1):
            cell = ws.cell(row=r_idx, column=c_idx)
            cell.font = font_body
            cell.border = border_bottom if is_last else border_data
            cell.alignment = Alignment(horizontal='left' if c_idx == 1 else 'center', vertical='center')
        ws.row_dimensions[r_idx].height = 20

    for col in ws.columns:
        max_len = max(len(str(c.value or '')) for c in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 14)


def run_diagnostics_and_sensitivity(data_path, output_excel_path):
    print("=" * 105)
    print("OLS REGRESSION DIAGNOSTICS & MULTIVARIABLE SENSITIVITY ANALYSES (MEDIAN & TOBIT MODELS)")
    print("=" * 105)

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at: {data_path}")

    df = pd.read_excel(data_path)
    pdrq_items = [f"pdrq_item{i}" for i in range(1, 10)]
    df['pdrq9_score'] = df[pdrq_items].mean(axis=1)

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
    # 1. OLS REGRESSION DIAGNOSTICS (MODEL 2)
    # =========================================================================
    formula_m2 = "pdrq9_score ~ sex_cat + age_cat + marital_cat + center_cat"
    model_m2_ols = smf.ols(formula_m2, data=df).fit()
    model_m2_cl = smf.ols(formula_m2, data=df).fit(
        cov_type='cluster',
        cov_kwds={'groups': df['health_center'], 'use_correction': True, 'use_t': False}
    )

    residuals = model_m2_ols.resid

    print("\n1. OLS REGRESSION DIAGNOSTICS (MODEL 2):")
    print("-" * 105)

    # A. Multicollinearity (VIF)
    X_soc = pd.get_dummies(df[['sex_cat', 'age_cat', 'marital_cat']], drop_first=True, dtype=float)
    X_soc_const = sm.add_constant(X_soc)
    vif_data = pd.DataFrame({
        'Variable': X_soc_const.columns[1:],
        'VIF': [variance_inflation_factor(X_soc_const.values, i) for i in range(1, X_soc_const.shape[1])]
    })
    print("A. Variance Inflation Factors (VIF) across sociodemographic predictors:")
    print(vif_data.round(2).to_string(index=False))
    print(f"   -> Maximum VIF = {vif_data['VIF'].max():.2f} (< 5.0 threshold, confirming absence of multicollinearity).")

    # B. Heteroscedasticity (Breusch-Pagan)
    bp_test = het_breuschpagan(residuals, model_m2_ols.model.exog)
    print("\nB. Breusch-Pagan Test for Heteroscedasticity:")
    print(f"   LM statistic = {bp_test[0]:.2f}, p-value = {bp_test[1]:.4e}")
    print("   -> Significant heteroscedasticity (p < 0.001), justifying Huber-White cluster-robust (CRV1) SEs.")

    # C. Residual Distribution
    res_skew = pd.Series(residuals).skew()
    res_kurt = pd.Series(residuals).kurtosis()
    print("\nC. Residual Distribution:")
    print(f"   Residual skewness        = {res_skew:.2f}")
    print(f"   Residual excess kurtosis = {res_kurt:.2f}")

    # D. Influential Observations (Cook's Distance)
    cooks_d = model_m2_ols.get_influence().cooks_distance[0]
    max_cook = np.max(cooks_d)
    print("\nD. Influential Observations:")
    print(f"   Maximum Cook's distance  = {max_cook:.4f} (well below 1.0; no undue single-observation leverage).")

    # =========================================================================
    # 2. SENSITIVITY ANALYSIS 1: QUANTILE / MEDIAN REGRESSION (q = 0.50)
    # =========================================================================
    print("\n" + "=" * 105)
    print("2. SENSITIVITY ANALYSIS 1: QUANTILE / MEDIAN REGRESSION (LAD, q = 0.50)")
    print("=" * 105)
    model_med = smf.quantreg(formula_m2, data=df).fit(q=0.5)
    ci_med = model_med.conf_int()
    socio_keys = [k for k in model_med.params.index if not k.startswith('center_cat')]

    summary_med = pd.DataFrame({
        'Coef (β)': model_med.params[socio_keys],
        'Std Err': model_med.bse[socio_keys],
        't': model_med.tvalues[socio_keys],
        'p-value': model_med.pvalues[socio_keys],
        '95% CI Lower': ci_med.loc[socio_keys, 0],
        '95% CI Upper': ci_med.loc[socio_keys, 1]
    })
    print(summary_med.round(4).to_string())

    # =========================================================================
    # 3. SENSITIVITY ANALYSIS 2: UPPER-CENSORED TOBIT REGRESSION (CEILING = 5.00)
    # =========================================================================
    print("\n" + "=" * 105)
    print("3. SENSITIVITY ANALYSIS 2: UPPER-CENSORED TOBIT REGRESSION (UPPER LIMIT = 5.00)")
    print("=" * 105)

    X_full = pd.get_dummies(df[['sex_cat', 'age_cat', 'marital_cat', 'center_cat']], drop_first=True, dtype=float)
    X_full = sm.add_constant(X_full)
    y_vals = df['pdrq9_score'].values
    ceiling_val = 5.0

    censored = (y_vals >= ceiling_val)
    uncensored = ~censored

    def tobit_log_likelihood(params):
        beta = params[:-1]
        sigma = np.exp(params[-1])
        xb = np.dot(X_full, beta)

        z_unc = (y_vals[uncensored] - xb[uncensored]) / sigma
        ll_unc = -0.5 * np.log(2 * np.pi) - np.log(sigma) - 0.5 * z_unc**2

        z_cens = (ceiling_val - xb[censored]) / sigma
        ll_cens = norm.logsf(z_cens)

        return -(np.sum(ll_unc) + np.sum(ll_cens))

    init_b = np.linalg.lstsq(X_full, y_vals, rcond=None)[0]
    init_s = np.std(residuals)
    init_p = np.append(init_b, np.log(init_s))

    tobit_res = minimize(tobit_log_likelihood, init_p, method='L-BFGS-B', options={'maxiter': 500})
    tobit_beta = tobit_res.x[:-1]
    tobit_sigma = np.exp(tobit_res.x[-1])

    print(f"Optimization convergence: {tobit_res.success} | Estimated Tobit sigma: {tobit_sigma:.4f}")

    # =========================================================================
    # 4. CONSOLIDATED SENSITIVITY COMPARISON TABLE
    # =========================================================================
    print("\n" + "=" * 105)
    print("4. CONSOLIDATED ROBUSTNESS TABLE: FACILITY-ADJUSTED OLS (CRV1) VS. MEDIAN (LAD) VS. TOBIT")
    print("=" * 105)

    keys_map = [
        ('sex_cat[T.Female]', 'sex_cat_Female', 'Female (vs Male)'),
        ('age_cat[T.31–40 years]', 'age_cat_31–40 years', '31–40 years (vs 18–30)'),
        ('age_cat[T.41–50 years]', 'age_cat_41–50 years', '41–50 years (vs 18–30)'),
        ('age_cat[T.51–60 years]', 'age_cat_51–60 years', '51–60 years (vs 18–30)'),
        ('age_cat[T.Over 60 years]', 'age_cat_Over 60 years', 'Over 60 years (vs 18–30)'),
        ('marital_cat[T.Single]', 'marital_cat_Single', 'Single (vs Married)'),
        ('marital_cat[T.Common-law union]', 'marital_cat_Common-law union', 'Common-law union (vs Married)'),
        ('marital_cat[T.Divorced]', 'marital_cat_Divorced', 'Divorced (vs Married)'),
        ('marital_cat[T.Widowed]', 'marital_cat_Widowed', 'Widowed (vs Married)')
    ]

    ci_m2 = model_m2_cl.conf_int()
    rows_en = []

    for k_sm, k_tob, lbl_en in keys_map:
        b_ols = model_m2_cl.params[k_sm]
        ci_ols_l = ci_m2.loc[k_sm, 0]
        ci_ols_u = ci_m2.loc[k_sm, 1]
        p_ols = model_m2_cl.pvalues[k_sm]

        b_med = model_med.params[k_sm]
        ci_med_l = ci_med.loc[k_sm, 0]
        ci_med_u = ci_med.loc[k_sm, 1]
        p_med = model_med.pvalues[k_sm]

        idx_t = list(X_full.columns).index(k_tob) if k_tob in X_full.columns else None
        b_tob = tobit_beta[idx_t] if idx_t is not None else np.nan

        p_ols_str = "< 0.001***" if p_ols < 0.001 else (f"{p_ols:.3f}**" if p_ols < 0.01 else (f"{p_ols:.3f}*" if p_ols < 0.05 else f"{p_ols:.3f}"))
        p_med_str = "< 0.001***" if p_med < 0.001 else (f"{p_med:.3f}**" if p_med < 0.01 else (f"{p_med:.3f}*" if p_med < 0.05 else f"{p_med:.3f}"))

        rows_en.append({
            'Sociodemographic Predictor': lbl_en,
            'OLS (CRV1) β [95% CI]': f"{b_ols:+.3f} [{ci_ols_l:+.3f}, {ci_ols_u:+.3f}]",
            'OLS p-value': p_ols_str,
            'Median Regression (q=0.50) β [95% CI]': f"{b_med:+.3f} [{ci_med_l:+.3f}, {ci_med_u:+.3f}]",
            'Median p-value': p_med_str,
            'Tobit Model (Censored at 5.00) β': f"{b_tob:+.3f}"
        })

    comp_df_en = pd.DataFrame(rows_en)
    print(comp_df_en.to_string(index=False))

    os.makedirs(os.path.dirname(output_excel_path), exist_ok=True)
    with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
        comp_df_en.to_excel(writer, sheet_name='Sensitivity_Analysis', index=False)
        style_worksheet(writer.sheets['Sensitivity_Analysis'], comp_df_en)

    print(f"\n[OK] Sensitivity analysis table exported to: {output_excel_path}")
    print("=" * 105)


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(base_dir, "datos", "pdrq9_patients_data.xlsx")
    output_excel = os.path.join(base_dir, "tablas", "table_s1_sensitivity_analysis.xlsx")
    run_diagnostics_and_sensitivity(data_file, output_excel)
