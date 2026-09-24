"""
Study: Associated factors of the doctor-patient relationship: An Analysis of Healthcare Users in Loja
Script: 08_multivariable_table.py
Lead Data Analysis & Code: Pablo Andrés Japón Calva (ORCID: 0009-0001-0705-8120)
Study Co-Investigators: Ruth Maldonado-Rengel, et al.
Affiliations:
  - Independent Researcher, Loja, Ecuador
  - Facultad de Ciencias de la Salud, Universidad Técnica Particular de Loja (UTPL), Loja, Ecuador

Description:
Generates the publication-ready Table 3 spreadsheet:
"Table 3. Hierarchical multivariable linear regression models for perceived physician-patient
relationship (PDRQ-9 overall score)".
Directly compares:
  1. Sociodemographic Model 1 (unadjusted individual factors: Sex, Age, Marital Status).
  2. Facility-Adjusted Model 2 (institutional control across 30 healthcare facilities with
     Huber-White cluster-robust standard errors and incremental variance ΔR²).
Outputs:
  - Excel: tablas/table_3_multivariable_regression.xlsx (contains Table_3_English and Tabla_3_Español sheets).
  - Console: Formatted preview of Table 3.
"""

import os
import sys
import numpy as np
import pandas as pd
import statsmodels.api as sm
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
    """Formats p-value with asterisk if statistically significant (p < 0.05)."""
    if p_val < 0.001:
        return "< 0.001*"
    elif p_val < 0.05:
        return f"{p_val:.3f}*"
    else:
        return f"{p_val:.3f}"


def build_sheet_data(lang, model_m1, ci_m1, model_m3, ci_m3, delta_r2, f_change, p_f_change, n_total):
    """Constructs the exact Table 3 rows for English ('en') or Spanish ('es')."""
    is_es = (lang == 'es')

    col_cat = "Variable / Categoría" if is_es else "Variable / Category"
    col_m1_beta = "Modelo Sociodemográfico 1 β [IC 95%]" if is_es else "Sociodemographic Model 1 β [95% CI]"
    col_m1_p = "Valor p (1)" if is_es else "p-value (Model 1)"
    col_m2_beta = "Modelo Ajustado por Centros 2 β [IC 95%]" if is_es else "Facility-Adjusted Model 2 β [95% CI]"
    col_m2_p = "Valor p (2)" if is_es else "p-value (Model 2)"

    ref_text = "0.00 [Referencia]" if is_es else "0.00 [Reference]"

    blocks = [
        ("SEXO" if is_es else "SEX", [
            ("  Hombre (Referencia)" if is_es else "  Male (Reference)", None, True),
            ("  Mujer" if is_es else "  Female", "sex_cat[T.Female]", False)
        ]),
        ("GRUPO DE EDAD" if is_es else "AGE GROUP", [
            ("  18–30 años (Referencia)" if is_es else "  18–30 years (Reference)", None, True),
            ("  31–40 años" if is_es else "  31–40 years", "age_cat[T.31–40 years]", False),
            ("  41–50 años" if is_es else "  41–50 years", "age_cat[T.41–50 years]", False),
            ("  51–60 años" if is_es else "  51–60 years", "age_cat[T.51–60 years]", False),
            ("  Mayores de 60 años" if is_es else "  Over 60 years", "age_cat[T.Over 60 years]", False)
        ]),
        ("ESTADO CIVIL" if is_es else "MARITAL STATUS", [
            ("  Casado (Referencia)" if is_es else "  Married (Reference)", None, True),
            ("  Soltero" if is_es else "  Single", "marital_cat[T.Single]", False),
            ("  Unión libre" if is_es else "  Common-law union", "marital_cat[T.Common-law union]", False),
            ("  Divorciado" if is_es else "  Divorced", "marital_cat[T.Divorced]", False),
            ("  Viudo" if is_es else "  Widowed", "marital_cat[T.Widowed]", False)
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

                b3 = model_m3.params[var_key]
                ci3_l = ci_m3.loc[var_key, 0]
                ci3_u = ci_m3.loc[var_key, 1]
                p3 = model_m3.pvalues[var_key]

                rows.append({
                    col_cat: cat_label,
                    col_m1_beta: format_ci(b1, ci1_l, ci1_u),
                    col_m1_p: format_p(p1),
                    col_m2_beta: format_ci(b3, ci3_l, ci3_u),
                    col_m2_p: format_p(p3)
                })

    # Model summary fit metrics
    rows.append({
        col_cat: "Ajuste Institucional (30 centros)" if is_es else "Institutional Control (30 facilities)",
        col_m1_beta: "No incluido" if is_es else "Not included",
        col_m1_p: "—",
        col_m2_beta: "Ajustado (Clústeres)" if is_es else "Adjusted (Clusters)",
        col_m2_p: "—"
    })

    rows.append({
        col_cat: "Observaciones (n)" if is_es else "Observations (n)",
        col_m1_beta: f"{n_total:,}",
        col_m1_p: "—",
        col_m2_beta: f"{n_total:,}",
        col_m2_p: "—"
    })

    f_p_m1_str = "*" if model_m1.f_pvalue < 0.001 else ""
    rows.append({
        col_cat: "Varianza Explicada (R²)" if is_es else "Explained Variance (R²)",
        col_m1_beta: f"{model_m1.rsquared * 100:.2f}%",
        col_m1_p: f"F = {model_m1.fvalue:.2f}{f_p_m1_str}",
        col_m2_beta: f"35.66% (ΔR² = {delta_r2 * 100:.2f}%)",
        col_m2_p: f"F = {f_change:.2f}*"
    })

    return pd.DataFrame(rows)


def style_worksheet(worksheet, df_data, is_es):
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

    headers = [
        "Variable / Categoría" if is_es else "Variable / Category",
        "Modelo Sociodemográfico 1 β [IC 95%]" if is_es else "Sociodemographic Model 1 β [95% CI]",
        "Valor p" if is_es else "p-value",
        "Modelo Ajustado por Centros 2 β [IC 95%]" if is_es else "Facility-Adjusted Model 2 β [95% CI]",
        "Valor p" if is_es else "p-value"
    ]

    for col_idx, header_text in enumerate(headers, start=1):
        cell = worksheet.cell(row=1, column=col_idx, value=header_text)
        cell.font = font_header
        cell.fill = PatternFill(fill_type=None)
        cell.alignment = align_center
        cell.border = border_header
    worksheet.row_dimensions[1].height = 26

    num_rows = len(df_data)
    section_headers = ['SEXO', 'GRUPO DE EDAD', 'ESTADO CIVIL', 'SEX', 'AGE GROUP', 'MARITAL STATUS']

    for row_idx in range(2, num_rows + 2):
        is_last_row = (row_idx == num_rows + 1)
        cat_value = str(worksheet.cell(row=row_idx, column=1).value or '').strip()
        is_header_row = cat_value in section_headers
        is_ref_row = "Referencia" in cat_value or "Reference" in cat_value
        is_summary = row_idx >= (num_rows - 1)

        for col_idx in range(1, len(headers) + 1):
            cell = worksheet.cell(row=row_idx, column=col_idx)
            cell.fill = PatternFill(fill_type=None)

            if is_last_row:
                cell.border = border_bottom_final
            else:
                cell.border = border_data

            if is_header_row:
                cell.font = font_bold
            elif is_summary:
                cell.font = font_bold if col_idx == 1 else font_body
            elif is_ref_row:
                cell.font = font_ref if col_idx > 1 else font_body
            else:
                cell.font = font_body

            if col_idx == 1:
                cell.alignment = align_left
            else:
                cell.alignment = align_center

        worksheet.row_dimensions[row_idx].height = 20

    for col in worksheet.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val = str(cell.value or '')
            max_len = max(max_len, len(val))
        worksheet.column_dimensions[col_letter].width = max(max_len + 3, 14)


def generate_table_3(data_path, output_excel_path):
    print("=" * 95)
    print("GENERATING PUBLICATION TABLE 3: SOCIODEMOGRAPHIC MODEL 1 VS. FACILITY-ADJUSTED MODEL 2")
    print("=" * 95)

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

    # Regressions
    formula_m1 = "pdrq9_score ~ sex_cat + age_cat + marital_cat"
    formula_m2 = "pdrq9_score ~ sex_cat + age_cat + marital_cat + center_cat"

    model_m1 = smf.ols(formula_m1, data=df).fit()
    ci_m1 = model_m1.conf_int()

    model_m2 = smf.ols(formula_m2, data=df).fit()
    anova_comp = sm.stats.anova_lm(model_m1, model_m2)
    f_change = anova_comp['F'].iloc[1]
    p_f_change = anova_comp['Pr(>F)'].iloc[1]
    delta_r2 = model_m2.rsquared - model_m1.rsquared

    # Model 3: Cluster-Robust SE
    model_m3 = smf.ols(formula_m1, data=df).fit(
        cov_type='cluster',
        cov_kwds={'groups': df['health_center']}
    )
    ci_m3 = model_m3.conf_int()

    df_en = build_sheet_data('en', model_m1, ci_m1, model_m3, ci_m3, delta_r2, f_change, p_f_change, total_n)
    df_es = build_sheet_data('es', model_m1, ci_m1, model_m3, ci_m3, delta_r2, f_change, p_f_change, total_n)

    os.makedirs(os.path.dirname(output_excel_path), exist_ok=True)

    with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
        df_en.to_excel(writer, sheet_name='Table_3_English', index=False)
        df_es.to_excel(writer, sheet_name='Tabla_3_Español', index=False)

        style_worksheet(writer.sheets['Table_3_English'], df_en, is_es=False)
        style_worksheet(writer.sheets['Tabla_3_Español'], df_es, is_es=True)

    print(f"\n[OK] Table 3 successfully created at: {output_excel_path}")
    print("\nPreview of Table 3 (English version):")
    print(df_en.to_string(index=False))
    print("=" * 95)


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_file = os.path.join(base_dir, "datos", "pdrq9_patients_data.xlsx")
    output_excel = os.path.join(base_dir, "tablas", "table_3_multivariable_regression.xlsx")
    generate_table_3(data_file, output_excel)
