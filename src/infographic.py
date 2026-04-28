import pandas as pd
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from pathlib import Path

from charts.chart1_national_energy_mix import create_chart as chart1
from charts.chart2_energy_sources import create_chart as chart2
from charts.chart3_choropleth_map import create_chart as chart3
from charts.chart4_state_renewable_change import create_chart as chart4

# Load the dataset once and pass it to all charts
df = pd.read_csv("data/cleaned/cleaned_energy_data.csv")

# Generate all 4 figures
fig1 = chart1(df)
fig2 = chart2(df)
fig3 = chart3(df)
fig4 = chart4(df)

# Build the 2x2 subplot grid
fig = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=(
        "National Energy Mix Overview (1990–2024)",
        "Trends in Key Energy Sources (1990–2024)",
        "State Renewable Share Snapshot (2024)",
        "State-Level Renewable Share Change (2000–2024)"
    ),
    specs=[
        [{"type": "xy"}, {"type": "xy"}],
        [{"type": "choropleth"}, {"type": "xy"}]
    ],
    horizontal_spacing=0.08,
    vertical_spacing=0.10,
    row_heights=[0.48, 0.52]
)

# Chart 1 — add traces in correct order so legend matches stack
cat_order = ["Fossil Fuel", "Nuclear", "Renewable", "Other"]
trace_map1 = {trace.name: trace for trace in fig1.data}
for i, cat in enumerate(cat_order):
    if cat in trace_map1:
        trace = trace_map1[cat]
        trace.showlegend = True
        trace.legendgroup = "chart1"
        if i == 0:
            trace.legendgrouptitle = dict(text="Category")
        fig.add_trace(trace, row=1, col=1)

# Chart 2 — add traces in correct order
src_order = ["Coal", "Natural Gas", "Hydroelectric", "Wind", "Solar"]
trace_map2 = {trace.name: trace for trace in fig2.data}
for i, src in enumerate(src_order):
    if src in trace_map2:
        trace = trace_map2[src]
        trace.showlegend = True
        trace.legendgroup = "chart2"
        if i == 0:
            trace.legendgrouptitle = dict(text="Energy Source")
        fig.add_trace(trace, row=1, col=2)

# Chart 3 — choropleth with a carefully positioned colorbar
for trace in fig3.data:
    trace.showlegend = False
    trace.colorbar = dict(
        title=dict(text="Renewable Share (%)", font=dict(size=10)),
        len=0.30,
        thickness=12,
        x=0.41,
        y=0.19,
        xanchor="left",
        yanchor="middle",
        tickfont=dict(size=8),
        ticksuffix="%"
    )
    fig.add_trace(trace, row=2, col=1)

# Chart 4 — no legend
for trace in fig4.data:
    trace.showlegend = False
    fig.add_trace(trace, row=2, col=2)

# Geo settings for choropleth panel
fig.update_geos(
    scope="usa",
    projection_type="albers usa",
    showlakes=True,
    lakecolor="lightblue"
)

# Axis labels
fig.update_xaxes(title_text="Year", row=1, col=1)
fig.update_yaxes(title_text="TWh", row=1, col=1)

fig.update_xaxes(title_text="Year", row=1, col=2)
fig.update_yaxes(title_text="TWh", row=1, col=2)

fig.update_xaxes(title_text="Percentage Points", row=2, col=2)
fig.update_yaxes(
    tickfont=dict(size=9),
    automargin=True,
    row=2,
    col=2
)

# Gridlines for XY charts
fig.update_xaxes(showgrid=True, gridcolor="#eeeeee", row=1, col=1)
fig.update_yaxes(showgrid=True, gridcolor="#eeeeee", row=1, col=1)

fig.update_xaxes(showgrid=True, gridcolor="#eeeeee", row=1, col=2)
fig.update_yaxes(showgrid=True, gridcolor="#eeeeee", row=1, col=2)

fig.update_xaxes(showgrid=True, gridcolor="#eeeeee", row=2, col=2)
fig.update_yaxes(showgrid=False, row=2, col=2)

# Overall layout
fig.update_layout(
    title=dict(
        text="Renewable Energy Growth vs. Fossil Fuel Use in the United States",
        font=dict(size=22),
        x=0.5,
        xanchor="center"
    ),
    width=1700,
    height=1320,
    plot_bgcolor="white",
    paper_bgcolor="white",
    margin=dict(l=50, r=255, t=165, b=115),
    legend=dict(
        x=1.02,
        y=0.96,
        xanchor="left",
        yanchor="top",
        orientation="v",
        tracegroupgap=12,
        font=dict(size=9),
        bgcolor="rgba(255,255,255,0.85)",
        bordercolor="#dddddd",
        borderwidth=1
    ),
    hoverlabel=dict(font_size=10)
)

# Add narrative subtitle, panel captions, and a concluding takeaway.
fig.add_annotation(
    x=0.5,
    y=1.06,
    xref="paper",
    yref="paper",
    showarrow=False,
    align="center",
    font=dict(size=12, color="#333333"),
    text=(
        "Research question: How has the balance between renewable and fossil-fuel electricity shifted "
        "across U.S. states, and which states are leaders or stragglers in the energy transition?"
    )
)

fig.add_annotation(
    x=0.5,
    y=-0.055,
    xref="paper",
    yref="paper",
    showarrow=False,
    align="center",
    font=dict(size=12, color="#222222"),
    text=(
        "<b>Audience takeaway (general public):</b> The U.S. is moving toward cleaner electricity, "
        "but progress is uneven across states, creating a clear geographic energy divide."
    )
)

# Save as static image and open in browser
output_path = Path("outputs/infographic.png")
output_path.parent.mkdir(parents=True, exist_ok=True)
fig.write_image(output_path, scale=2)
print(f"Infographic saved as {output_path}")

fig.show()