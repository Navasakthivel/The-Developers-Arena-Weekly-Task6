

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

from dashboard_static import PALETTE, CATEGORY_PALETTE, SEGMENT_PALETTE, load_data

OUTPUT_DIR = Path(__file__).parent / "visualizations"
OUTPUT_DIR.mkdir(exist_ok=True)


def fig_layout(fig, title):
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color=PALETTE["primary"]), x=0.02),
        paper_bgcolor=PALETTE["background"],
        plot_bgcolor="white",
        font=dict(family="Arial", size=12, color="#333"),
        margin=dict(l=40, r=20, t=60, b=40),
        legend=dict(bgcolor="rgba(255,255,255,0.6)"),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#E5E9EC")
    fig.update_yaxes(showgrid=True, gridcolor="#E5E9EC")
    return fig


# ----------------------------------------------------------------------
# 1. Revenue trend with category dropdown
# ----------------------------------------------------------------------
def interactive_revenue_trend(df, save=True):
    monthly_cat = df.groupby(["Month", "Category"], as_index=False)["Revenue"].sum()
    monthly_all = df.groupby("Month", as_index=False)["Revenue"].sum()
    monthly_all["Category"] = "All Categories"
    combined = pd.concat([monthly_all, monthly_cat], ignore_index=True)

    fig = px.line(
        combined, x="Month", y="Revenue", color="Category",
        color_discrete_sequence=["#333333"] + CATEGORY_PALETTE,
        markers=True,
        title="Monthly Revenue Trend by Category"
    )

    # Build dropdown to isolate each category
    categories = ["All Categories"] + sorted(df["Category"].unique())
    buttons = []
    for cat in categories:
        visible = [trace.name == cat for trace in fig.data]
        buttons.append(dict(
            label=cat,
            method="update",
            args=[{"visible": visible}, {"title": f"Monthly Revenue Trend — {cat}"}]
        ))
    # "Show all" option
    buttons.insert(0, dict(
        label="Show All",
        method="update",
        args=[{"visible": [True] * len(fig.data)}, {"title": "Monthly Revenue Trend by Category"}]
    ))

    fig.update_layout(
        updatemenus=[dict(
            buttons=buttons, direction="down", x=1.0, y=1.18,
            xanchor="right", showactive=True
        )]
    )
    fig.update_traces(hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra>%{fullData.name}</extra>")
    fig_layout(fig, "Monthly Revenue Trend by Category")

    if save:
        fig.write_html(OUTPUT_DIR / "07_interactive_revenue_trend.html")
    return fig


# ----------------------------------------------------------------------
# 2. Animated bar chart - Quarterly revenue by category
# ----------------------------------------------------------------------
def animated_quarterly_revenue(df, save=True):
    q_rev = df.groupby(["Quarter", "Category"], as_index=False)["Revenue"].sum()
    q_rev = q_rev.sort_values("Quarter")
    max_rev = q_rev["Revenue"].max() * 1.1

    fig = px.bar(
        q_rev, x="Category", y="Revenue", color="Category",
        color_discrete_sequence=CATEGORY_PALETTE,
        animation_frame="Quarter",
        range_y=[0, max_rev],
        title="Quarterly Revenue by Category (Animated)"
    )
    fig.update_traces(hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>")
    fig_layout(fig, "Quarterly Revenue by Category (Animated)")
    fig.update_layout(showlegend=False)

    if save:
        fig.write_html(OUTPUT_DIR / "08_animated_quarterly_revenue.html")
    return fig


# ----------------------------------------------------------------------
# 3. Customer segmentation - bubble scatter (Age vs Revenue vs Rating)
# ----------------------------------------------------------------------
def customer_segmentation_bubble(df, save=True):
    sample = df.sample(min(600, len(df)), random_state=7)
    fig = px.scatter(
        sample, x="Age", y="Revenue", size="Quantity", color="CustomerSegment",
        color_discrete_map=SEGMENT_PALETTE,
        hover_data={"Category": True, "Region": True, "Rating": True, "Channel": True},
        title="Customer Segmentation: Age vs Revenue"
    )
    fig.update_traces(marker=dict(opacity=0.65, line=dict(width=0.5, color="white")))
    fig_layout(fig, "Customer Segmentation: Age vs Revenue (bubble size = Quantity)")

    if save:
        fig.write_html(OUTPUT_DIR / "09_customer_segmentation_bubble.html")
    return fig


# ----------------------------------------------------------------------
# 4. Product performance - sunburst (Category > Region)
# ----------------------------------------------------------------------
def product_performance_sunburst(df, save=True):
    sun = df.groupby(["Category", "Region"], as_index=False)["Revenue"].sum()
    fig = px.sunburst(
        sun, path=["Category", "Region"], values="Revenue",
        color="Category", color_discrete_sequence=CATEGORY_PALETTE,
        title="Product Performance: Revenue by Category & Region"
    )
    fig.update_traces(hovertemplate="<b>%{label}</b><br>Revenue: ₹%{value:,.0f}<extra></extra>")
    fig_layout(fig, "Product Performance: Revenue by Category & Region")

    if save:
        fig.write_html(OUTPUT_DIR / "10_product_performance_sunburst.html")
    return fig


# ----------------------------------------------------------------------
# 5. Channel performance with toggle buttons (Revenue vs Order Count)
# ----------------------------------------------------------------------
def channel_performance_toggle(df, save=True):
    rev = df.groupby("Channel", as_index=False)["Revenue"].sum()
    cnt = df.groupby("Channel", as_index=False).size().rename(columns={"size": "Orders"})

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=rev["Channel"], y=rev["Revenue"], name="Revenue",
        marker_color=CATEGORY_PALETTE[0],
        hovertemplate="<b>%{x}</b><br>Revenue: ₹%{y:,.0f}<extra></extra>",
        visible=True
    ))
    fig.add_trace(go.Bar(
        x=cnt["Channel"], y=cnt["Orders"], name="Order Count",
        marker_color=CATEGORY_PALETTE[2],
        hovertemplate="<b>%{x}</b><br>Orders: %{y}<extra></extra>",
        visible=False
    ))

    fig.update_layout(
        updatemenus=[dict(
            type="buttons", direction="right", x=1.0, y=1.18, xanchor="right",
            buttons=[
                dict(label="Revenue", method="update",
                     args=[{"visible": [True, False]}, {"yaxis": {"title": "Revenue (₹)"}}]),
                dict(label="Order Count", method="update",
                     args=[{"visible": [False, True]}, {"yaxis": {"title": "Orders"}}]),
            ]
        )]
    )
    fig_layout(fig, "Channel Performance")
    fig.update_yaxes(title="Revenue (₹)")

    if save:
        fig.write_html(OUTPUT_DIR / "11_channel_performance_toggle.html")
    return fig


def generate_all_interactive_plots(df):
    interactive_revenue_trend(df)
    animated_quarterly_revenue(df)
    customer_segmentation_bubble(df)
    product_performance_sunburst(df)
    channel_performance_toggle(df)
    print(f"Saved interactive plots to {OUTPUT_DIR}")


if __name__ == "__main__":
    data = load_data()
    generate_all_interactive_plots(data)
