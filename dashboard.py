"""
Interactive Sales Dashboard - Main Entry Point
================================================
Run this script to:
1. Generate/load the sales dataset
2. Produce all Seaborn statistical visualizations (Days 1-4)
3. Produce all Plotly interactive visualizations (Day 5)
4. Build the combined branded HTML dashboard (Days 6-7)

Usage:
    python dashboard.py
"""

import os
from pathlib import Path

from dashboard_static import load_data, generate_all_static_plots
from dashboard_interactive import generate_all_interactive_plots
from dashboard_build import build_dashboard


def main():
    data_path = Path(__file__).parent / "sales_data.csv"
    if not data_path.exists():
        print("sales_data.csv not found. Run generate_data.py first.")
        return

    print("Loading data...")
    df = load_data(data_path)
    print(f"Loaded {len(df):,} records spanning "
          f"{df['OrderDate'].min().date()} to {df['OrderDate'].max().date()}")

    print("\n[Days 1-4] Generating Seaborn statistical visualizations...")
    generate_all_static_plots(df)

    print("\n[Day 5] Generating Plotly interactive visualizations...")
    generate_all_interactive_plots(df)

    print("\n[Days 6-7] Building combined branded dashboard...")
    out_path = build_dashboard(df)

    print(f"\nDone! Open '{out_path}' in a browser to view the dashboard.")


if __name__ == "__main__":
    main()
