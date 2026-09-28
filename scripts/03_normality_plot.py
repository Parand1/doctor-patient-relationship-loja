"""
Study: Associated factors of the doctor-patient relationship: An Analysis of Healthcare Users in Loja
Script: 03_normality_plot.py
Lead Data Analysis & Code: Pablo Andrés Japón Calva (ORCID: 0009-0001-0705-8120)
Study Co-Investigators: Ruth Maldonado-Rengel, et al.
Affiliations:
  - Independent Researcher, Loja, Ecuador
  - Facultad de Ciencias de la Salud, Universidad Técnica Particular de Loja (UTPL), Loja, Ecuador

Description:
Generates diagnostic figure (Figure 0) with 2 panels
documenting the non-normal distribution and clinical ceiling effect of the PDRQ-9 Overall Mean Score:
  - Panel A: Density histogram with empirical KDE curve vs. theoretical normal curve,
    displaying sample mean and median.
  - Panel B: Quantile-Quantile (Q-Q) plot against theoretical Gaussian quantiles.
Output: imagenes/figure_0_normality.png
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

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
    output_image_path = os.path.join(img_dir, "figure_0_normality.png")

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at: {data_path}")

    df = pd.read_excel(data_path)
    pdrq_items = [f"pdrq_item{i}" for i in range(1, 10)]
    df['gsi'] = df[pdrq_items].mean(axis=1)
    data = df['gsi']

    mean_val = data.mean()
    median_val = data.median()
    sd_val = data.std()
    skew_val = data.skew()

    # Editorial style configuration
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        'font.size': 11,
        'font.family': 'sans-serif',
        'axes.labelsize': 12,
        'axes.titlesize': 13,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10
    })

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # -------------------------------------------------------------
    # PANEL A: Empirical Density and Theoretical Normal Curve
    # -------------------------------------------------------------
    ax1 = axes[0]
    sns.histplot(data, stat='density', bins=25, color='#4A90E2', alpha=0.55, edgecolor='black', ax=ax1, label='Empirical Histogram')
    sns.kdeplot(data, color='#1A365D', linewidth=2.2, ax=ax1, label='Empirical Density (KDE)')

    # Theoretical normal curve
    x_range = np.linspace(data.min() - 0.2, 5.2, 300)
    normal_pdf = stats.norm.pdf(x_range, mean_val, sd_val)
    ax1.plot(x_range, normal_pdf, color='#E53E3E', linestyle='--', linewidth=2.0, label='Theoretical Normal Curve')

    # Central tendency markers
    ax1.axvline(mean_val, color='#E53E3E', linestyle='-', linewidth=1.8, label=f'Mean ({mean_val:.2f})')
    ax1.axvline(median_val, color='#2B6CB0', linestyle='-', linewidth=1.8, label=f'Median ({median_val:.2f})')

    ax1.set_title('A. Empirical Density vs. Theoretical Gaussian Curve', fontweight='bold', pad=12)
    ax1.set_xlabel('PDRQ-9 Overall Score')
    ax1.set_ylabel('Probability Density')
    ax1.set_xlim(1.0, 5.3)
    ax1.legend(loc='upper left', frameon=True)

    # Skewness annotation box
    ax1.text(0.05, 0.55, f"n = {len(data)}\nSkewness = {skew_val:.2f}\n(Negative Skew)", 
             transform=ax1.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#EDF2F7', edgecolor='#CBD5E0'))

    # -------------------------------------------------------------
    # PANEL B: Normal Q-Q Plot
    # -------------------------------------------------------------
    ax2 = axes[1]
    (osm, osr), (slope, intercept, r) = stats.probplot(data, dist="norm", plot=None)
    ax2.scatter(osm, osr, color='#2B6CB0', alpha=0.45, s=20, edgecolors='none', label='Observed Quantiles')
    ax2.plot(osm, slope * osm + intercept, color='#E53E3E', linestyle='-', linewidth=2.0, label='Theoretical Reference Line')

    ax2.set_title('B. Normal Q-Q Plot (Quantile-Quantile)', fontweight='bold', pad=12)
    ax2.set_xlabel('Theoretical Quantiles (Standard Normal)')
    ax2.set_ylabel('Sample Quantiles (Observed Score)')
    ax2.legend(loc='upper left', frameon=True)

    # Lower tail deviation note
    ax2.text(0.05, 0.65, f"Pronounced deviation in lower tail\nreflecting negative skewness\nand ceiling effect", 
             transform=ax2.transAxes, fontsize=10, verticalalignment='top',
             bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF5F5', edgecolor='#FEB2B2'))

    plt.tight_layout()
    plt.savefig(output_image_path, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Normality diagnostic plot successfully generated at: {output_image_path}")


if __name__ == '__main__':
    main()
