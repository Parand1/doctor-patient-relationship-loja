"""
Study: Associated factors of the doctor-patient relationship: An Analysis of Healthcare Users in Loja
Script: 01_sociodemographic.py
Lead Data Analysis & Code: Pablo Andrés Japón Calva (ORCID: 0009-0001-0705-8120)
Study Co-Investigators: Ruth Maldonado-Rengel, et al.
Affiliations:
  - Independent Researcher, Loja, Ecuador
  - Facultad de Ciencias de la Salud, Universidad Técnica Particular de Loja (UTPL), Loja, Ecuador

Description:
Calculates descriptive frequencies and percentages for patient sociodemographic
characteristics (Sex, Age groups, Marital status), corresponding to Table 1 of the manuscript.
Outputs:
  - Console: Formatted Table 1 summary.
  - Excel: tablas/table_1_sociodemographic.xlsx with publication styling.
"""

import os
import sys
import pandas as pd
from openpyxl.styles import Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Ensure standard UTF-8 console output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "datos", "pdrq9_patients_data.xlsx")
    tables_dir = os.path.join(base_dir, "tablas")
    os.makedirs(tables_dir, exist_ok=True)
    output_excel_path = os.path.join(tables_dir, "table_1_sociodemographic.xlsx")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at: {data_path}")

    df = pd.read_excel(data_path)
    total_n = len(df)

    # 1. Biological Sex
    sex_counts = df['sex'].value_counts()
    data_sex = [
        ['SEX', '', ''],
        ['  Male', sex_counts.get(1, 0), round((sex_counts.get(1, 0) / total_n) * 100, 2)],
        ['  Female', sex_counts.get(2, 0), round((sex_counts.get(2, 0) / total_n) * 100, 2)]
    ]

    # 2. Age Groups
    age_counts = df['age_group'].value_counts()
    data_age = [
        ['AGE GROUP', '', ''],
        ['  18–30 years', age_counts.get(1, 0), round((age_counts.get(1, 0) / total_n) * 100, 2)],
        ['  31–40 years', age_counts.get(2, 0), round((age_counts.get(2, 0) / total_n) * 100, 2)],
        ['  41–50 years', age_counts.get(3, 0), round((age_counts.get(3, 0) / total_n) * 100, 2)],
        ['  51–60 years', age_counts.get(4, 0), round((age_counts.get(4, 0) / total_n) * 100, 2)],
        ['  Over 60 years', age_counts.get(5, 0), round((age_counts.get(5, 0) / total_n) * 100, 2)]
    ]

    # 3. Marital Status (matching manuscript order)
    marital_counts = df['marital_status'].value_counts()
    data_marital = [
        ['MARITAL STATUS', '', ''],
        ['  Married', marital_counts.get(1, 0), round((marital_counts.get(1, 0) / total_n) * 100, 2)],
        ['  Single', marital_counts.get(4, 0), round((marital_counts.get(4, 0) / total_n) * 100, 2)],
        ['  Common-law union', marital_counts.get(5, 0), round((marital_counts.get(5, 0) / total_n) * 100, 2)],
        ['  Divorced', marital_counts.get(2, 0), round((marital_counts.get(2, 0) / total_n) * 100, 2)],
        ['  Widowed', marital_counts.get(3, 0), round((marital_counts.get(3, 0) / total_n) * 100, 2)]
    ]

    all_rows = data_sex + data_age + data_marital
    df_table1 = pd.DataFrame(all_rows, columns=['Category', 'n', '%'])

    with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
        df_table1.to_excel(writer, sheet_name='Table_1_Sociodemographics', index=False)
        ws = writer.sheets['Table_1_Sociodemographics']

        font_header = Font(name='Calibri', size=10, bold=True)
        font_bold = Font(name='Calibri', size=10, bold=True)
        font_body = Font(name='Calibri', size=10)

        border_thick = Side(border_style="medium", color="000000")
        border_thin = Side(border_style="thin", color="D9D9D9")
        border_header = Border(top=border_thick, bottom=border_thick, left=border_thin, right=border_thin)
        border_data = Border(top=border_thin, bottom=border_thin, left=border_thin, right=border_thin)
        border_bottom = Border(top=border_thin, bottom=border_thick, left=border_thin, right=border_thin)

        for col_idx, col_name in enumerate(['Category', 'n', '%'], start=1):
            cell = ws.cell(row=1, column=col_idx, value=col_name)
            cell.font = font_header
            cell.alignment = Alignment(horizontal='center' if col_idx > 1 else 'left', vertical='center')
            cell.border = border_header
        ws.row_dimensions[1].height = 24

        sections = ['SEX', 'AGE GROUP', 'MARITAL STATUS']
        num_rows = len(df_table1)
        for r_idx in range(2, num_rows + 2):
            is_last = (r_idx == num_rows + 1)
            cat_val = str(ws.cell(row=r_idx, column=1).value or '').strip()
            is_sec = cat_val in sections

            for c_idx in range(1, 4):
                cell = ws.cell(row=r_idx, column=c_idx)
                cell.font = font_bold if is_sec else font_body
                cell.border = border_bottom if is_last else border_data
                cell.alignment = Alignment(horizontal='left' if c_idx == 1 else 'center', vertical='center')
            ws.row_dimensions[r_idx].height = 20

        for col in ws.columns:
            max_len = max(len(str(c.value or '')) for c in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    print("=" * 80)
    print(f"Table 1. Sociodemographic profile of patients treated at healthcare facilities in Loja (n = {total_n:,}).")
    print("=" * 80)
    print(df_table1.to_string(index=False))
    print("=" * 80)
    print(f"[OK] Excel table successfully generated at: {output_excel_path}\n")


if __name__ == '__main__':
    main()
