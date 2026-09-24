"""
Study: Associated factors of the doctor-patient relationship: An Analysis of Healthcare Users in Loja
Script: 04_plot_sex.py
Lead Data Analysis & Code: Pablo Andrés Japón Calva (ORCID: 0009-0001-0705-8120)
Study Co-Investigators: Ruth Maldonado-Rengel, et al.
Affiliations:
  - Independent Researcher, Loja, Ecuador
  - Facultad de Ciencias de la Salud, Universidad Técnica Particular de Loja (UTPL), Loja, Ecuador

Description:
Generates publication Figure 4: Boxplot comparing perceived physician-patient relationship
scores (PDRQ-9 Overall Score) by patient biological sex.
Output: imagenes/figure_4_sex.png
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
    output_image_path = os.path.join(img_dir, "figure_4_sex.png")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at: {data_path}")

    df = pd.read_excel(data_path)
    preguntas = [f"pdrq_item{i}" for i in range(1, 10)]
    df['pdrq9_score'] = df[preguntas].mean(axis=1)

    mapa_sexo = {1: 'Male (n = 995)', 2: 'Female (n = 2,262)'}
    df['sex_label'] = df['sex'].map(mapa_sexo)

    # Editorial style configuration
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        'font.size': 11,
        'font.family': 'sans-serif',
        'axes.labelsize': 12,
        'axes.titlesize': 13
    })

    fig, ax = plt.subplots(figsize=(8, 6))

    # Sober institutional palette
    paleta = {'Male (n = 995)': '#4A90E2', 'Female (n = 2,262)': '#E57373'}

    sns.boxplot(
        x='sex_label',
        y='pdrq9_score',
        data=df,
        palette=paleta,
        hue='sex_label',
        legend=False,
        width=0.45,
        fliersize=3,
        linewidth=1.4,
        ax=ax
    )

    ax.set_title('Perceived Physician-Patient Relationship by Patient Sex', fontweight='bold', pad=15)
    ax.set_xlabel('Sex', fontweight='bold', labelpad=10)
    ax.set_ylabel('PDRQ-9 Overall Score (Scale 1–5)', fontweight='bold', labelpad=10)
    ax.set_ylim(1.0, 5.3)

    plt.tight_layout()
    plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Figure 4 (Sex comparison) successfully generated at: {output_image_path}")


if __name__ == '__main__':
    main()
