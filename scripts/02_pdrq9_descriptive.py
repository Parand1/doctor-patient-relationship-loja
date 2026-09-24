"""
Study: Associated factors of the doctor-patient relationship: An Analysis of Healthcare Users in Loja
Script: 02_pdrq9_descriptive.py
Lead Data Analysis & Code: Pablo Andrés Japón Calva (ORCID: 0009-0001-0705-8120)
Study Co-Investigators: Ruth Maldonado-Rengel, et al.
Affiliations:
  - Independent Researcher, Loja, Ecuador
  - Facultad de Ciencias de la Salud, Universidad Técnica Particular de Loja (UTPL), Loja, Ecuador

Description:
Computes comprehensive parametric (Mean, SD) and non-parametric (Median, IQR, [Q1–Q3])
descriptive statistics for all 9 PDRQ-9 items and the composite PDRQ-9 Overall Mean Score,
corresponding to Table 2 of the manuscript.
Outputs:
  - Console: Formatted Table 2 summary.
  - Excel: tablas/table_2_pdrq9_descriptive.xlsx with publication styling.
"""

import os
import sys
import numpy as np
import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
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
    output_excel_path = os.path.join(tables_dir, "table_2_pdrq9_descriptive.xlsx")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at: {data_path}")

    df = pd.read_excel(data_path)
    total_n = len(df)

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

    # Compute PDRQ-9 Overall Mean Score
    df['pdrq_overall_score'] = df[pdrq_items].mean(axis=1)

    rows = []
    for idx, col in enumerate(pdrq_items):
        series = df[col]
        q1 = np.percentile(series, 25)
        q3 = np.percentile(series, 75)
        iqr = q3 - q1
        rows.append({
            'Item': item_labels[idx],
            'Mean': round(series.mean(), 2),
            'SD': round(series.std(), 2),
            'Median': round(series.median(), 2),
            'IQR': round(iqr, 2),
            '[Q1–Q3]': f"[{q1:.2f}–{q3:.2f}]"
        })

    # Overall Mean Score row
    overall = df['pdrq_overall_score']
    ov_q1 = np.percentile(overall, 25)
    ov_q3 = np.percentile(overall, 75)
    ov_iqr = ov_q3 - ov_q1

    rows.append({
        'Item': 'PDRQ-9 Overall Mean Score',
        'Mean': round(overall.mean(), 2),
        'SD': round(overall.std(), 2),
        'Median': round(overall.median(), 2),
        'IQR': round(ov_iqr, 2),
        '[Q1–Q3]': f"[{ov_q1:.2f}–{ov_q3:.2f}]"
    })

    df_table2 = pd.DataFrame(rows)

    # Export to Excel with styling
    with pd.ExcelWriter(output_excel_path, engine='openpyxl') as writer:
        df_table2.to_excel(writer, sheet_name='Table_2_PDRQ9', index=False)
        ws = writer.sheets['Table_2_PDRQ9']

        font_header = Font(name='Calibri', size=10, bold=True)
        font_bold = Font(name='Calibri', size=10, bold=True)
        font_body = Font(name='Calibri', size=10)
        border_thick = Side(border_style="medium", color="000000")
        border_thin = Side(border_style="thin", color="D9D9D9")
        border_header = Border(top=border_thick, bottom=border_thick, left=border_thin, right=border_thin)
        border_data = Border(top=border_thin, bottom=border_thin, left=border_thin, right=border_thin)
        border_bottom = Border(top=border_thin, bottom=border_thick, left=border_thin, right=border_thin)

        for col_idx, col_name in enumerate(df_table2.columns, start=1):
            cell = ws.cell(row=1, column=col_idx, value=col_name)
            cell.font = font_header
            cell.alignment = Alignment(horizontal='center' if col_idx > 1 else 'left', vertical='center')
            cell.border = border_header
        ws.row_dimensions[1].height = 24

        num_rows = len(df_table2)
        for r_idx in range(2, num_rows + 2):
            is_last = (r_idx == num_rows + 1)
            for c_idx in range(1, len(df_table2.columns) + 1):
                cell = ws.cell(row=r_idx, column=c_idx)
                cell.font = font_bold if is_last else font_body
                cell.border = border_bottom if is_last else border_data
                cell.alignment = Alignment(horizontal='left' if c_idx == 1 else 'center', vertical='center')
            ws.row_dimensions[r_idx].height = 20

        for col in ws.columns:
            max_len = max(len(str(c.value or '')) for c in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    # Console output
    print("=" * 85)
    print(f"Table 2. Item-level and overall scores on the patient-physician relationship (n = {total_n:,}).")
    print("=" * 85)
    print(df_table2.to_string(index=False))
    print("=" * 85)
    print("Note: Both parametric (Mean, SD) and non-parametric statistics (Median, IQR)")
    print("are reported due to pronounced negative skewness (skewness = −1.76).")
    print(f"[OK] Excel table successfully generated at: {output_excel_path}\n")


if __name__ == "__main__":
    main()
