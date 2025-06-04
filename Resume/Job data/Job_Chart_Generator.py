
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def load_and_clean_data(filepath):
    df = pd.read_csv(filepath)
    df.columns = df.columns.str.strip()
    df['date of sale'] = pd.to_datetime(df['date of sale'], errors='coerce')
    cols = ['total sale amount', 'Kitchen', 'Bathroom', 'Flooring', 'Remodel', 'Cabinet']
    df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')
    return df

def plot_category_totals(df, year, output_dir):
    df_year = df[df['date of sale'].dt.year == year]
    totals = df_year[['Kitchen', 'Bathroom', 'Flooring', 'Remodel', 'Cabinet']].sum()
    plt.figure(figsize=(10, 6))
    bars = plt.bar(totals.index, totals.values, color='skyblue')
    plt.title(f'{year} - Total Dollar Amount by Category')
    plt.xlabel('Categories')
    plt.ylabel('Total Dollar Amount')
    plt.ylim(0, 1500000)
    plt.grid(True, axis='y')
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f'${height:,.0f}',
                 ha='center', va='bottom', fontsize=10)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"{year}_bar_chart.pdf"))
    plt.close()

def plot_grouped_bar(df, output_dir):
    df_2024 = df[df['date of sale'].dt.year == 2024]
    df_2025 = df[df['date of sale'].dt.year == 2025]
    categories = ['Kitchen', 'Bathroom', 'Flooring', 'Remodel', 'Cabinet']
    totals_2024 = df_2024[categories].sum()
    totals_2025 = df_2025[categories].sum()
    x = np.arange(len(categories))
    width = 0.35
    fig, ax = plt.subplots(figsize=(10, 6))
    bars_2024 = ax.bar(x - width/2, totals_2024, width, label='2024', color='skyblue')
    bars_2025 = ax.bar(x + width/2, totals_2025, width, label='2025', color='lightgreen')
    ax.set_title('2024 vs 2025 - Total Dollar Amount by Category')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.set_ylabel('Total Dollar Amount')
    ax.set_ylim(0, 1500000)
    ax.legend()
    ax.grid(True, axis='y')
    for bar in bars_2024:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'${bar.get_height():,.0f}',
                ha='center', va='bottom', fontsize=9)
    for bar in bars_2025:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height(), f'${bar.get_height():,.0f}',
                ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "Grouped_Bar_Chart.pdf"))
    plt.close()

def generate_all_charts(file_path, output_dir="charts"):
    os.makedirs(output_dir, exist_ok=True)
    df = load_and_clean_data(file_path)
    plot_category_totals(df, 2024, output_dir)
    plot_category_totals(df, 2025, output_dir)
    plot_grouped_bar(df, output_dir)
    print(f"Charts saved to: {output_dir}")
