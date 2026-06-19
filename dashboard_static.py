"""
Interactive Sales Dashboard - Core Module
==========================================
Contains data loading, color theme, and Seaborn/Matplotlib static
visualization functions (Days 1-4 of the build plan).
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# ----------------------------------------------------------------------
# Cohesive Color Theme
# ----------------------------------------------------------------------
PALETTE = {
    "primary": "#2E5266",     # deep slate blue
    "secondary": "#6E8898",   # muted blue-grey
    "accent": "#F4A259",      # warm orange accent
    "accent2": "#5B8C5A",     # muted green
    "highlight": "#D1495B",   # coral red
    "background": "#F7F9FB",
}

CATEGORY_PALETTE = ["#2E5266", "#6E8898", "#F4A259", "#5B8C5A", "#D1495B"]
SEGMENT_PALETTE = {"New": "#6E8898", "Returning": "#2E5266", "VIP": "#F4A259"}

PLOTLY_TEMPLATE_COLORS = dict(
    colorway=CATEGORY_PALETTE,
    paper_bgcolor=PALETTE["background"],
    plot_bgcolor="white",
)

OUTPUT_DIR = Path(__file__).parent / "visualizations"
OUTPUT_DIR.mkdir(exist_ok=True)


def set_style():
    """Apply a cohesive Seaborn/Matplotlib style across all plots (Day 1)."""
    sns.set_theme(style="whitegrid", palette=CATEGORY_PALETTE)
    plt.rcParams.update({
        "figure.facecolor": PALETTE["background"],
        "axes.facecolor": "white",
        "axes.edgecolor": "#CBD5DC",
        "axes.titleweight": "bold",
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "font.family": "DejaVu Sans",
        "figure.dpi": 110,
    })


def load_data(path="sales_data.csv"):
    df = pd.read_csv(path, parse_dates=["OrderDate"])
    return df


# ----------------------------------------------------------------------
# Day 1: Basic Seaborn plot - Sales Trend (line)
# ----------------------------------------------------------------------
def plot_monthly_revenue_trend(df, save=True):
    monthly = df.groupby("Month", as_index=False)["Revenue"].sum()
    fig, ax = plt.subplots(figsize=(9, 4.5))
    sns.lineplot(data=monthly, x="Month", y="Revenue", marker="o",
                  color=PALETTE["primary"], linewidth=2.5, ax=ax)
    ax.set_title("Monthly Revenue Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue (₹)")
    ax.tick_params(axis="x", rotation=60)
    fig.tight_layout()
    if save:
        fig.savefig(OUTPUT_DIR / "01_monthly_revenue_trend.png", bbox_inches="tight")
    return fig


# ----------------------------------------------------------------------
# Day 2: Statistical Visualizations - Box & Violin plots with annotations
# ----------------------------------------------------------------------
def plot_price_distribution_box(df, save=True):
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.boxplot(x="Category", y="Price", data=df, hue="Category", palette=CATEGORY_PALETTE, legend=False, ax=ax)
    ax.set_title("Price Distribution by Category")
    ax.set_xlabel("Category")
    ax.set_ylabel("Price (₹)")

    # Statistical annotation: median labels
    medians = df.groupby("Category")["Price"].median()
    for i, cat in enumerate(ax.get_xticklabels()):
        cat_name = cat.get_text()
        median_val = medians[cat_name]
        ax.text(i, median_val, f"{median_val:.0f}", ha="center", va="bottom",
                fontsize=9, fontweight="bold", color=PALETTE["highlight"])

    fig.tight_layout()
    if save:
        fig.savefig(OUTPUT_DIR / "02_price_distribution_box.png", bbox_inches="tight")
    return fig


def plot_revenue_violin_by_segment(df, save=True):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.violinplot(x="CustomerSegment", y="Revenue", data=df, hue="CustomerSegment",
                    palette=SEGMENT_PALETTE, legend=False, ax=ax, cut=0)
    ax.set_title("Revenue Distribution by Customer Segment")
    ax.set_xlabel("Customer Segment")
    ax.set_ylabel("Revenue (₹)")

    means = df.groupby("CustomerSegment")["Revenue"].mean()
    for i, seg in enumerate(ax.get_xticklabels()):
        seg_name = seg.get_text()
        mean_val = means[seg_name]
        ax.scatter(i, mean_val, color="black", marker="D", s=30, zorder=5)
        ax.text(i + 0.12, mean_val, f"mean={mean_val:.0f}", fontsize=9, va="center")

    fig.tight_layout()
    if save:
        fig.savefig(OUTPUT_DIR / "03_revenue_violin_segment.png", bbox_inches="tight")
    return fig


# ----------------------------------------------------------------------
# Day 3: Heatmaps & Correlation Matrix
# ----------------------------------------------------------------------
def plot_correlation_heatmap(df, save=True):
    numeric_cols = ["Price", "Quantity", "Discount", "Revenue", "Rating", "Age"]
    corr = df[numeric_cols].corr()

    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0,
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8}, ax=ax)
    ax.set_title("Correlation Matrix - Numeric Features")
    fig.tight_layout()
    if save:
        fig.savefig(OUTPUT_DIR / "04_correlation_heatmap.png", bbox_inches="tight")
    return fig


def plot_region_category_heatmap(df, save=True):
    pivot = df.pivot_table(values="Revenue", index="Region", columns="Category",
                            aggfunc="sum", fill_value=0)
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu", linewidths=0.5, ax=ax)
    ax.set_title("Total Revenue by Region and Category")
    fig.tight_layout()
    if save:
        fig.savefig(OUTPUT_DIR / "05_region_category_heatmap.png", bbox_inches="tight")
    return fig


# ----------------------------------------------------------------------
# Day 4: Multi-plot Dashboard - 2x2 Subplot Grid
# ----------------------------------------------------------------------
def plot_2x2_dashboard(df, save=True):
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    fig.suptitle("Sales Performance Overview", fontsize=16, fontweight="bold",
                  color=PALETTE["primary"])

    # Top-left: Revenue by category (bar)
    cat_rev = df.groupby("Category", as_index=False)["Revenue"].sum().sort_values("Revenue", ascending=False)
    sns.barplot(data=cat_rev, x="Category", y="Revenue", hue="Category", palette=CATEGORY_PALETTE, legend=False, ax=axes[0, 0])
    axes[0, 0].set_title("Revenue by Category")
    axes[0, 0].tick_params(axis="x", rotation=30)

    # Top-right: Channel share (count)
    sns.countplot(data=df, x="Channel", hue="CustomerSegment",
                   palette=SEGMENT_PALETTE, ax=axes[0, 1])
    axes[0, 1].set_title("Orders by Channel & Segment")
    axes[0, 1].legend(title="Segment", fontsize=8)

    # Bottom-left: Quantity vs Price scatter
    sns.scatterplot(data=df.sample(400, random_state=1), x="Price", y="Quantity",
                     hue="Category", palette=CATEGORY_PALETTE, alpha=0.6, ax=axes[1, 0])
    axes[1, 0].set_title("Quantity vs Price")
    axes[1, 0].legend(fontsize=7, title="Category")

    # Bottom-right: Rating distribution
    sns.histplot(data=df, x="Rating", hue="CustomerSegment", multiple="stack",
                  palette=SEGMENT_PALETTE, bins=9, ax=axes[1, 1])
    axes[1, 1].set_title("Customer Rating Distribution")

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    if save:
        fig.savefig(OUTPUT_DIR / "06_2x2_dashboard.png", bbox_inches="tight")
    return fig


def generate_all_static_plots(df):
    set_style()
    plot_monthly_revenue_trend(df)
    plot_price_distribution_box(df)
    plot_revenue_violin_by_segment(df)
    plot_correlation_heatmap(df)
    plot_region_category_heatmap(df)
    plot_2x2_dashboard(df)
    print(f"Saved static plots to {OUTPUT_DIR}")


if __name__ == "__main__":
    data = load_data()
    generate_all_static_plots(data)
