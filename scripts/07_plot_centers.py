"""
Study: Associated factors of the doctor-patient relationship: An Analysis of Healthcare Users in Loja
Script: 07_plot_centers.py
Lead Data Analysis & Code: Pablo Andrés Japón Calva (ORCID: 0009-0001-0705-8120)
Study Co-Investigators: Ruth Maldonado-Rengel, et al.
Affiliations:
  - Independent Researcher, Loja, Ecuador
  - Facultad de Ciencias de la Salud, Universidad Técnica Particular de Loja (UTPL), Loja, Ecuador

Description:
Generates publication Figure 3: Institutional ranking of perceived physician-patient
relationship (PDRQ-9 Overall Score) across all 30 public healthcare facilities in Loja Canton.
Output: imagenes/figure_3_healthcare_centers.png
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns

# Ensure standard UTF-8 console output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "datos", "pdrq9_patients_data.xlsx")
    img_dir = os.path.join(base_dir, "imagenes")
    os.makedirs(img_dir, exist_ok=True)
    output_image_path = os.path.join(img_dir, "figure_3_healthcare_centers.png")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at: {data_path}")

    df = pd.read_excel(data_path)
    preguntas = [f"pdrq_item{i}" for i in range(1, 10)]
    df['pdrq9_score'] = df[preguntas].mean(axis=1)

    # Official mapping of facility names (with code in parentheses)
    nombres_centros = {
        'CS1': 'Health Center No. 1 (CS1)',
        'CS2': 'Health Center No. 2 (CS2)',
        'CS3': 'Health Center No. 3 (CS3)',
        'CSA': 'Aguangora (CSA)',
        'CSB': 'Belén (CSB)',
        'CSCA': 'Carigán (CSCA)',
        'CSCH': 'Chuquiribamba (CSCH)',
        'CSCHO': 'Chontacruz (CSCHO)',
        'CSCO': 'Comunidades (CSCO)',
        'CSCON': 'Consacola (CSCON)',
        'CSEC': 'El Cisne (CSEC)',
        'CSG': 'Gualel (CSG)',
        'CSHDC': 'Héroes del Cenepa (CSHDC)',
        'CSJ': 'Jimbilla (CSJ)',
        'CSM': 'Malacatos (CSM)',
        'CSMI': 'Miraflores (CSMI)',
        'CSMO': 'Motupe (CSMO)',
        'CSO': 'Obrapía (CSO)',
        'CSP': 'Pichic (CSP)',
        'CSS': 'Santiago (CSS)',
        'CSSC': 'San Cayetano (CSSC)',
        'CSSL': 'San Lucas (CSSL)',
        'CST': 'Taquil (CST)',
        'CSTC': 'Tierras Coloradas (CSTC)',
        'CSUL': 'Unión Lojana (CSUL)',
        'CSY': 'Yangana (CSY)',
        'CSZH': 'Zamora Huaico (CSZH)',
        'HBV': 'Vilcabamba Basic Hospital (HBV)',
        'HGIA': 'Isidro Ayora General Hospital (HGIA)',
        'UAV': 'Vilcabamba Nested Unit (UAV)'
    }

    df['facility_label'] = df['health_center'].map(nombres_centros).fillna(df['health_center'])

    # Aggregate ranking
    df_ranking = df.groupby('facility_label')['pdrq9_score'].agg(
        median='median',
        mean='mean',
        n='count'
    ).reset_index()

    # Sort ascending so highest appears at the top of horizontal barplot
    df_ranking = df_ranking.sort_values(by=['median', 'mean'], ascending=[True, True]).reset_index(drop=True)

    # Editorial style configuration
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        'font.size': 10,
        'font.family': 'sans-serif',
        'axes.labelsize': 11,
        'axes.titlesize': 13
    })

    fig, ax = plt.subplots(figsize=(11, 13))

    norm = mcolors.Normalize(vmin=2.0, vmax=5.0)
    cmap = plt.get_cmap('RdYlGn')
    bar_colors = [cmap(norm(val)) for val in df_ranking['median']]

    bars = ax.barh(
        df_ranking['facility_label'],
        df_ranking['median'],
        color=bar_colors,
        edgecolor='#333333',
        linewidth=0.7,
        height=0.7
    )

    # Add numeric median value at the end of each bar
    for bar in bars:
        width = bar.get_width()
        y_pos = bar.get_y() + bar.get_height() / 2
        ax.text(
            width + 0.06,
            y_pos,
            f'{width:.2f}',
            va='center',
            ha='left',
            fontsize=9.5,
            fontweight='bold',
            color='#2C3E50'
        )

    ax.set_title('Ranking of Perceived Physician-Patient Relationship across Healthcare Facilities', fontweight='bold', pad=18)
    ax.set_xlabel('Median PDRQ-9 Overall Score (Scale 1–5)', fontweight='bold', labelpad=12)
    ax.set_ylabel('Healthcare Facility', fontweight='bold', labelpad=12)

    ax.set_xlim(0, 5.5)
    ax.set_xticks(np.arange(0, 5.5, 0.5))

    # Reference sample median line
    ax.axvline(x=4.56, color='#2980B9', linestyle='--', linewidth=1.2, alpha=0.8, label='Overall Sample Median (4.56)')
    ax.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.9, fontsize=9.5)

    plt.tight_layout()
    plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Figure 3 (Healthcare facilities ranking) successfully generated at: {output_image_path}")


if __name__ == '__main__':
    main()
