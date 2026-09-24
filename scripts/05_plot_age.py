"""
Study: Associated factors of the doctor-patient relationship: An Analysis of Healthcare Users in Loja
Script: 05_plot_age.py
Lead Data Analysis & Code: Pablo Andrés Japón Calva (ORCID: 0009-0001-0705-8120)
Study Co-Investigators: Ruth Maldonado-Rengel, et al.
Affiliations:
  - Independent Researcher, Loja, Ecuador
  - Facultad de Ciencias de la Salud, Universidad Técnica Particular de Loja (UTPL), Loja, Ecuador

Description:
Generates publication Figure 1: Boxplot visualizing the distribution of the perceived
physician-patient relationship (PDRQ-9 Overall Score) across patient age cohorts.
Output: imagenes/figure_1_age.png
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
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
    output_image_path = os.path.join(img_dir, "figure_1_age.png")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at: {data_path}")

    df = pd.read_excel(data_path)
    preguntas = [f"pdrq_item{i}" for i in range(1, 10)]
    df['pdrq9_score'] = df[preguntas].mean(axis=1)

    mapa_edad = {
        1: '18–30 years',
        2: '31–40 years',
        3: '41–50 years',
        4: '51–60 years',
        5: 'Over 60 years'
    }
    df['age_group_label'] = df['age_group'].map(mapa_edad)

    # Editorial style configuration
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        'font.size': 11,
        'font.family': 'sans-serif',
        'axes.labelsize': 12,
        'axes.titlesize': 13
    })

    fig, ax = plt.subplots(figsize=(9, 6))

    orden_edad = ['18–30 years', '31–40 years', '41–50 years', '51–60 years', 'Over 60 years']

    colores_distintivos = {
        '18–30 years': '#3498DB',   # Blue
        '31–40 years': '#F39C12',   # Amber
        '41–50 years': '#2ECC71',   # Emerald green
        '51–60 years': '#9B59B6',   # Purple
        'Over 60 years': '#E74C3C'  # Coral red
    }

    sns.boxplot(
        x='age_group_label',
        y='pdrq9_score',
        data=df,
        order=orden_edad,
        palette=colores_distintivos,
        hue='age_group_label',
        legend=False,
        width=0.52,
        fliersize=3,
        linewidth=1.3,
        ax=ax
    )

    ax.set_title('Perceived Physician-Patient Relationship Across Age Groups', fontweight='bold', pad=15)
    ax.set_xlabel('Age Group', fontweight='bold', labelpad=10)
    ax.set_ylabel('PDRQ-9 Overall Score (Scale 1–5)', fontweight='bold', labelpad=10)
    ax.set_ylim(1.0, 5.3)

    plt.tight_layout()
    plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Figure 1 (Age comparison) successfully generated at: {output_image_path}")


if __name__ == '__main__':
    main()
