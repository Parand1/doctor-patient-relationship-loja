"""
Study: Associated factors of the doctor-patient relationship: An Analysis of Healthcare Users in Loja
Script: 07_table_centers.py
Lead Data Analysis & Code: Pablo Andrés Japón Calva (ORCID: 0009-0001-0705-8120)
Study Co-Investigators: Ruth Maldonado-Rengel, et al.
Affiliations:
  - Independent Researcher, Loja, Ecuador
  - Facultad de Ciencias de la Salud, Universidad Técnica Particular de Loja (UTPL), Loja, Ecuador

Description:
Generates publication Table 3:
"Table 3. Facility-level distribution of perceived doctor-patient relationship (PDRQ-9) across
30 public healthcare facilities in Loja (n = 3,257)".
Includes official MSP facility typology (20 Type A centers, 4 Type B centers, 4 health posts,
1 basic hospital, and 1 general hospital), parametric (Mean, SD) and non-parametric
(Median, IQR [Q1–Q3]) metrics, and ceiling effect prevalence (Score = 5.00, n (%)).
Outputs:
  - Excel: tablas/table_3_healthcare_facilities.xlsx
  - Console: Formatted preview of Table 3.
"""

import os
import sys
import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Ensure standard UTF-8 console output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


FACILITY_CATALOG_EN = {
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


def build_facility_table(df):
    n_total = len(df)
    rows = []

    for code, g in df.groupby('health_center'):
        scores = g['pdrq_overall_score']
        n_c = len(scores)
        q25 = scores.quantile(0.25)
        q75 = scores.quantile(0.75)
        n_ceil = int((scores == 5.0).sum())
        pct_ceil = (n_ceil / n_c) * 100.0
        name, typology = FACILITY_CATALOG_EN.get(code, (code, 'Other'))

        rows.append({
            'code': code,
            'name': name,
            'setting': typology,
            'n': n_c,
            'pct_sample': (n_c / n_total) * 100.0,
            'mean': scores.mean(),
            'std': scores.std(),
            'median': scores.median(),
            'iqr': q75 - q25,
            'q25': q25,
            'q75': q75,
            'n_ceiling': n_ceil,
            'pct_ceiling': pct_ceil
        })

    table_df = pd.DataFrame(rows).sort_values(
        by=['median', 'pct_ceiling', 'mean'], ascending=[False, False, False]
    ).reset_index(drop=True)
    table_df['rank'] = range(1, len(table_df) + 1)

    formatted_rows = []
    for _, r in table_df.iterrows():
        formatted_rows.append({
            'Rank': r['rank'],
            'Code': r['code'],
            'Healthcare Facility Name': r['name'],
            'Facility Typology (MSP)': r['setting'],
            'n': r['n'],
            '% of Sample': f"{r['pct_sample']:.2f}%",
            'Mean (SD)': f"{r['mean']:.2f} ({r['std']:.2f})",
            'Median': f"{r['median']:.2f}",
            'IQR [Q1–Q3]': f"{r['iqr']:.2f} [{r['q25']:.2f}–{r['q75']:.2f}]",
            'Score = 5.00 n (%)': f"{r['n_ceiling']} ({r['pct_ceiling']:.1f}%)"
        })

    total_scores = df['pdrq_overall_score']
    total_q25 = total_scores.quantile(0.25)
    total_q75 = total_scores.quantile(0.75)
    total_n_ceil = int((total_scores == 5.0).sum())
    total_pct_ceil = (total_n_ceil / n_total) * 100.0

    formatted_rows.append({
        'Rank': '—',
        'Code': 'TOTAL',
        'Healthcare Facility Name': 'All 30 Public Healthcare Facilities',
        'Facility Typology (MSP)': '20 Type A, 4 Type B, 4 Health Posts, 1 Basic Hosp, 1 General Hosp',
        'n': n_total,
        '% of Sample': '100.00%',
        'Mean (SD)': f"{total_scores.mean():.2f} ({total_scores.std():.2f})",
        'Median': f"{total_scores.median():.2f}",
        'IQR [Q1–Q3]': f"{total_q75 - total_q25:.2f} [{total_q25:.2f}–{total_q75:.2f}]",
        'Score = 5.00 n (%)': f"{total_n_ceil} ({total_pct_ceil:.1f}%)"
    })

    return pd.DataFrame(formatted_rows)


def style_worksheet(ws, df_table):
    font_header = Font(name='Calibri', size=10, bold=True, color='000000')
    font_bold = Font(name='Calibri', size=10, bold=True, color='000000')
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
        cell.alignment = Alignment(horizontal='left' if col_idx in [3, 4] else 'center', vertical='center')
        cell.border = border_header
    ws.row_dimensions[1].height = 24

    num_rows = len(df_table)
    for r_idx in range(2, num_rows + 2):
        is_last = (r_idx == num_rows + 1)
        for c_idx in range(1, len(df_table.columns) + 1):
            cell = ws.cell(row=r_idx, column=c_idx)
            cell.font = font_bold if is_last else font_body
            cell.border = border_bottom if is_last else border_data
            cell.alignment = Alignment(horizontal='left' if c_idx in [3, 4] else 'center', vertical='center')
        ws.row_dimensions[r_idx].height = 20

    for col in ws.columns:
        max_len = max(len(str(c.value or '')) for c in col)
        col_letter = get_column_letter(col[0].column)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 12)


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "datos", "pdrq9_patients_data.xlsx")
    tables_dir = os.path.join(base_dir, "tablas")
    os.makedirs(tables_dir, exist_ok=True)
    output_excel_path = os.path.join(tables_dir, "table_3_healthcare_facilities.xlsx")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at: {data_path}")

    df = pd.read_excel(data_path)
    pdrq_items = [f"pdrq_item{i}" for i in range(1, 10)]
    df['pdrq_overall_score'] = df[pdrq_items].mean(axis=1)

    df_table3 = build_facility_table(df)

    with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
        df_table3.to_excel(writer, sheet_name='Table_3_Facilities', index=False)
        style_worksheet(writer.sheets['Table_3_Facilities'], df_table3)

    print("=" * 115)
    print("Table 3. Facility-level distribution of perceived doctor-patient relationship (PDRQ-9) across 30 facilities (n = 3,257).")
    print("=" * 115)
    print(df_table3.to_string(index=False))
    print("=" * 115)
    print(f"[OK] Excel table successfully generated at: {output_excel_path}\n")


if __name__ == "__main__":
    main()
