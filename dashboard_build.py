

from pathlib import Path
import pandas as pd
import plotly.io as pio

from dashboard_static import load_data, PALETTE
from dashboard_interactive import (
    interactive_revenue_trend,
    animated_quarterly_revenue,
    customer_segmentation_bubble,
    product_performance_sunburst,
    channel_performance_toggle,
)

OUTPUT_DIR = Path(__file__).parent / "visualizations"
OUTPUT_DIR.mkdir(exist_ok=True)


def kpi_cards(df):
    total_revenue = df["Revenue"].sum()
    total_orders = len(df)
    avg_order = df["Revenue"].mean()
    avg_rating = df["Rating"].mean()

    cards = [
        ("Total Revenue", f"₹{total_revenue:,.0f}"),
        ("Total Orders", f"{total_orders:,}"),
        ("Avg. Order Value", f"₹{avg_order:,.0f}"),
        ("Avg. Rating", f"{avg_rating:.2f} / 5"),
    ]
    html = '<div class="kpi-row">'
    for label, value in cards:
        html += f'''
        <div class="kpi-card">
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>'''
    html += "</div>"
    return html


def build_dashboard(df):
    figs = {
        "Revenue Trend": interactive_revenue_trend(df, save=False),
        "Quarterly Performance": animated_quarterly_revenue(df, save=False),
        "Customer Segmentation": customer_segmentation_bubble(df, save=False),
        "Product Performance": product_performance_sunburst(df, save=False),
        "Channel Performance": channel_performance_toggle(df, save=False),
    }

    plot_divs = ""
    for title, fig in figs.items():
        div = pio.to_html(fig, include_plotlyjs=False, full_html=False,
                           config={"displaylogo": False, "responsive": True})
        plot_divs += f'<div class="chart-card">{div}</div>\n'

    # Embed plotly.js inline so the dashboard works fully offline
    import plotly
    plotly_js_path = Path(plotly.__file__).parent / "package_data" / "plotly.min.js"
    plotly_js = plotly_js_path.read_text(encoding="utf-8")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SalesScope | Interactive Sales Dashboard</title>
<script>{plotly_js}</script>
<style>
    :root {{
        --primary: {PALETTE['primary']};
        --secondary: {PALETTE['secondary']};
        --accent: {PALETTE['accent']};
        --bg: {PALETTE['background']};
    }}
    * {{ box-sizing: border-box; }}
    body {{
        margin: 0;
        font-family: 'Segoe UI', Arial, sans-serif;
        background: var(--bg);
        color: #2b2b2b;
    }}
    header {{
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        padding: 28px 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
    }}
    header h1 {{
        margin: 0;
        font-size: 1.8rem;
        letter-spacing: 0.5px;
    }}
    header p {{
        margin: 4px 0 0;
        opacity: 0.85;
        font-size: 0.9rem;
    }}
    .badge {{
        background: var(--accent);
        color: #2b2b2b;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }}
    main {{
        padding: 24px 40px 60px;
        max-width: 1400px;
        margin: 0 auto;
    }}
    .kpi-row {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 16px;
        margin: 24px 0 32px;
    }}
    .kpi-card {{
        background: white;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-top: 4px solid var(--accent);
    }}
    .kpi-value {{
        font-size: 1.6rem;
        font-weight: 700;
        color: var(--primary);
    }}
    .kpi-label {{
        margin-top: 6px;
        font-size: 0.85rem;
        color: #6b7b85;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    .grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(560px, 1fr));
        gap: 24px;
    }}
    .chart-card {{
        background: white;
        border-radius: 12px;
        padding: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }}
    footer {{
        text-align: center;
        padding: 20px;
        color: #8a97a0;
        font-size: 0.8rem;
    }}
</style>
</head>
<body>
<header>
    <div>
        <h1>📊 SalesScope Dashboard</h1>
        <p>Sales Trends · Customer Segmentation · Product Performance</p>
    </div>
    <div class="badge">FY 2024–2025</div>
</header>
<main>
    {kpi_cards(df)}
    <div class="grid">
        {plot_divs}
    </div>
</main>
<footer>
    Built with Python, Seaborn, and Plotly &middot; SalesScope Analytics
</footer>
</body>
</html>"""

    out_path = OUTPUT_DIR.parent / "dashboard.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"Dashboard written to {out_path}")
    return out_path


if __name__ == "__main__":
    data = load_data()
    build_dashboard(data)
