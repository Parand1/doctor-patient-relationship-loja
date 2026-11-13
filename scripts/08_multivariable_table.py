"""
Study: Associated factors of the doctor-patient relationship: An Analysis of Healthcare Users in Loja
Script: 08_multivariable_table.py
Lead Data Analysis & Code: Pablo Andrés Japón Calva (ORCID: 0009-0001-0705-8120)
Study Co-Investigators: Ruth Maldonado-Rengel, et al.
Affiliations:
  - Independent Researcher, Loja, Ecuador
  - Facultad de Ciencias de la Salud, Universidad Técnica Particular de Loja (UTPL), Loja, Ecuador

Description:
Generates the publication-ready Table 4 spreadsheet:
"Table 4. Hierarchical multivariable linear regression models for perceived physician-patient
relationship (PDRQ-9 overall score)".
Directly compares:
  1. Sociodemographic Model (1): Conventional OLS regression with Sex, Age Group, and Marital Status.
  2. Facility-Adjusted Model (2): Multivariable linear regression incorporating fixed-effect
     indicators for all 30 healthcare facilities, with standard errors adjusted using the
     Huber-White Cluster-Robust Variance estimator (CRV1, G = 30 clusters) incorporating the
     finite-sample correction [G / (G - 1)] * [(N - 1) / (N - k)] (G = 30, N = 3,257, k = 39)
     and standard normal (z) reference distribution.
Outputs:
  - Excel: tablas/table_4_multivariable_regression.xlsx
  - Console: Formatted preview of Table 4.
"""

import os
import sys
import pandas as pd
import statsmodels.formula.api as smf
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Ensure standard UTF-8 console output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def format_ci(beta, ci_low, ci_high):
    """Formats coefficient and 95% confidence interval."""
    return f"{beta:+.3f} [{ci_low:+.3f}, {ci_high:+.3f}]"


def format_p(p_val):
    """Formats p-value with significance asterisks (* p < 0.05, ** p < 0.01, *** p < 0.001)."""
    if p_val < 0.001:
        return "< 0.001***"
    elif p_val < 0.01:
        return f"{p_val:.3f}**"
    elif p_val < 0.05:
        return f"{p_val:.3f}*"
    else:
        return f"{p_val:.3f}"


def build_sheet_data(model_m1, ci_m1, model_m2, ci_m2, delta_r2, n_total):
    """Constructs the exact Table 4 rows matching the final manuscript."""
    col_cat = "Variable / Category"
    col_m1_beta = "Sociodemographic Model (1) β [95% CI]"
    col_m1_p = "p-value (1)"
    col_m2_beta = "Facility-Adjusted Model (2) β [95% CI]"
    col_m2_p = "p-value (2)"

    ref_text = "0.00 [Reference]"

    blocks = [
        ("SEX", [
            ("  Male (Reference)", None, True),
            ("  Female", "sex_cat[T.Female]", False)
        ]),
        ("AGE GROUP", [
            ("  18–30 years (Reference)", None, True),
            ("  31–40 years", "age_cat[T.31–40 years]", False),
            ("  41–50 years", "age_cat[T.41–50 years]", False),
            ("  51–60 years", "age_cat[T.51–60 years]", False),
            ("  Over 60 years", "age_cat[T.Over 60 years]", False)
        ]),
        ("MARITAL STATUS", [
            ("  Married (Reference)", None, True),
            ("  Single", "marital_cat[T.Single]", False),
            ("  Common-law union", "marital_cat[T.Common-law union]", False),
            ("  Divorced", "marital_cat[T.Divorced]", False),
            ("  Widowed", "marital_cat[T.Widowed]", False)
        ])
    ]

    rows = []
    for var_title, categories in blocks:
        rows.append({
            col_cat: var_title,
            col_m1_beta: "",
            col_m1_p: "",
            col_m2_beta: "",
            col_m2_p: ""
        })
        for cat_label, var_key, is_ref in categories:
            if is_ref:
                rows.append({
                    col_cat: cat_label,
                    col_m1_beta: ref_text,
                    col_m1_p: "—",
                    col_m2_beta: ref_text,
                    col_m2_p: "—"
                })
            else:
                b1 = model_m1.params[var_key]
                ci1_l = ci_m1.loc[var_key, 0]
                ci1_u = ci_m1.loc[var_key, 1]
                p1 = model_m1.pvalues[var_key]

                b2 = model_m2.params[var_key]
                ci2_l = ci_m2.loc[var_key, 0]
                ci2_u = ci_m2.loc[var_key, 1]
                p2 = model_m2.pvalues[var_key]

                rows.append({
                    col_cat: cat_label,
                    col_m1_beta: format_ci(b1, ci1_l, ci1_u),
                    col_m1_p: format_p(p1),
                    col_m2_beta: format_ci(b2, ci2_l, ci2_u),
                    col_m2_p: format_p(p2)
                })

    # Model fit and institutional adjustment rows
    rows.append({
        col_cat: "MODEL FIT AND INSTITUTIONAL ADJUSTMENT",
        col_m1_beta: "",
        col_m1_p: "",
        col_m2_beta: "",
        col_m2_p: ""
    })
    rows.append({
        col_cat: "  Healthcare Facility Fixed Effects (30 centers)",
        col_m1_beta: "No",
        col_m1_p: "—",
        col_m2_beta: "Yes (30 centers)",
        col_m2_p: "—"
    })
    rows.append({
        col_cat: "  Standard Error Adjustment for Clustering",
        col_m1_beta: "No (Conventional OLS)",
        col_m1_p: "—",
        col_m2_beta: "Yes (Huber-White CRV1, G=30, z-test)",
        col_m2_p: "—"
    })
    rows.append({
        col_cat: "  Coefficient of Determination (R²)",
        col_m1_beta: f"{model_m1.rsquared * 100:.2f}%",
        col_m1_p: "—",
        col_m2_beta: f"{model_m2.rsquared * 100:.2f}%",
        col_m2_p: "—"
    })
    rows.append({
        col_cat: "  Adjusted R²",
        col_m1_beta: f"{model_m1.rsquared_adj * 100:.2f}%",
        col_m1_p: "—",
        col_m2_beta: f"{model_m2.rsquared_adj * 100:.2f}%",
        col_m2_p: "—"
    })
    rows.append({
        col_cat: "  Incremental Variance Explained (ΔR²)",
        col_m1_beta: "—",
        col_m1_p: "—",
        col_m2_beta: f"+{delta_r2 * 100:.2f} percentage points",
        col_m2_p: "—"
    })
    rows.append({
        col_cat: "  Total Sample Size (n)",
        col_m1_beta: f"{n_total:,}",
        col_m1_p: "—",
        col_m2_beta: f"{n_total:,}",
        col_m2_p: "—"
    })

    return pd.DataFrame(rows)


def style_worksheet(worksheet, df_data):
    """Applies clean academic styling (APA/medical journal standard)."""
    font_header = Font(name='Calibri', size=10, bold=True, color='000000')
    align_center = Alignment(horizontal='center', vertical='center')
    align_left = Alignment(horizontal='left', vertical='center')

    font_body = Font(name='Calibri', size=10, color='000000')
    font_bold = Font(name='Calibri', size=10, bold=True, color='000000')
    font_ref = Font(name='Calibri', size=9, italic=True, color='595959')

    border_thick = Side(border_style="medium", color="000000")
    border_thin = Side(border_style="thin", color="000000")
    border_gray = Side(border_style="thin", color="D9D9D9")

    border_header = Border(top=border_thick, bottom=border_thick, left=border_gray, right=border_gray)
    border_data = Border(top=border_gray, bottom=border_gray, left=border_gray, right=border_gray)
    border_bottom_final = Border(top=border_thin, bottom=border_thick, left=border_gray, right=border_gray)

    headers = list(df_data.columns)
    for col_idx, header_text in enumerate(headers, start=1):
        cell = worksheet.cell(row=1, column=col_idx, value=header_text)
        cell.font = font_header
        cell.fill = PatternFill(fill_type=None)
        cell.alignment = align_center
        cell.border = border_header
    worksheet.row_dimensions[1].height = 26

    num_rows = len(df_data)
    section_headers = ['SEX', 'AGE GROUP', 'MARITAL STATUS', 'MODEL FIT AND INSTITUTIONAL ADJUSTMENT']

    for row_idx in range(2, num_rows + 2):
        is_last_row = (row_idx == num_rows + 1)
        cat_value = str(worksheet.cell(row=row_idx, column=1).value or '').strip()
        is_header_row = cat_value in section_headers
        is_ref_row = "Reference" in cat_value

        for col_idx in range(1, len(headers) + 1):
            cell = worksheet.cell(row=row_idx, column=col_idx)
            cell.fill = PatternFill(fill_type=None)

            if is_last_row:
                cell.border = border_bottom_final
            else:
                cell.border = border_data

            if is_header_row:
                cell.font = font_bold
            elif is_ref_row:
                cell.font = font_ref if col_idx > 1 else font_body
            else:
                cell.font = font_body

            cell.alignment = align_left if col_idx == 1 else align_center

        worksheet.row_dimensions[row_idx].height = 20

    for col in worksheet.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        worksheet.column_dimensions[col_letter].width = max(max_len + 3, 14)


def generate_table_4(data_path, output_excel_path):
    print("=" * 100)
    print("GENERATING PUBLICATION TABLE 4: SOCIODEMOGRAPHIC MODEL (1) VS. FACILITY-ADJUSTED MODEL (2)")
    print("=" * 100)

    df = pd.read_excel(data_path)
    total_n = len(df)

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

    formula_m1 = "pdrq9_score ~ sex_cat + age_cat + marital_cat"
    formula_m2 = "pdrq9_score ~ sex_cat + age_cat + marital_cat + center_cat"

    model_m1 = smf.ols(formula_m1, data=df).fit()
    ci_m1 = model_m1.conf_int()

    model_m2 = smf.ols(formula_m2, data=df).fit(
        cov_type='cluster',
        cov_kwds={'groups': df['health_center'], 'use_correction': True, 'use_t': False}
    )
    ci_m2 = model_m2.conf_int()
    delta_r2 = model_m2.rsquared - model_m1.rsquared

    df_en = build_sheet_data(model_m1, ci_m1, model_m2, ci_m2, delta_r2, total_n)

    os.makedirs(os.path.dirname(output_excel_path), exist_ok=True)

    with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
        df_en.to_excel(writer, sheet_name='Table_4_Regression', index=False)
        style_worksheet(writer.sheets['Table_4_Regression'], df_en)

    print(f"\n[OK] Table 4 successfully created at: {output_excel_path}")
    print("\nPreview of Table 4:")
    print(df_en.to_string(index=False))
    print("=" * 100)


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(base_dir, "datos", "pdrq9_patients_data.xlsx")
    output_excel = os.path.join(base_dir, "tablas", "table_4_multivariable_regression.xlsx")
    generate_table_4(data_file, output_excel)
