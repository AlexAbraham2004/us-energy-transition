import pandas as pd
import plotly.graph_objects as go

# Load the cleaned dataset
df = pd.read_csv("data/cleaned/cleaned_energy_data.csv")

# Filter to the 5 key energy sources from the proposal sketch
sources = ["Coal", "Natural Gas", "Hydroelectric Conventional", "Wind", "Solar Thermal and Photovoltaic"]
filtered = df[df["energy_source"].isin(sources)]

# Aggregate nationally by year and energy source
national = filtered.groupby(["year", "energy_source"])["generation_mwh"].sum().reset_index()

# Convert to TWh
national["generation_twh"] = national["generation_mwh"] / 1e6

# Cleaner display names for the legend
name_map = {
    "Coal": "Coal",
    "Natural Gas": "Natural Gas",
    "Hydroelectric Conventional": "Hydroelectric",
    "Wind": "Wind",
    "Solar Thermal and Photovoltaic": "Solar"
}

# Colors for each source
colors = {
    "Coal": "#4a4a4a",
    "Natural Gas": "#e377c2",
    "Hydroelectric Conventional": "#1f77b4",
    "Wind": "#17becf",
    "Solar Thermal and Photovoltaic": "#f7b731"
}

# Build the line chart
fig = go.Figure()

for source in sources:
    source_data = national[national["energy_source"] == source]
    fig.add_trace(go.Scatter(
        x=source_data["year"],
        y=source_data["generation_twh"],
        name=name_map[source],
        mode="lines",
        line=dict(color=colors[source], width=2.5),
        hovertemplate="%{x}<br>" + name_map[source] + ": %{y:.2f} TWh<extra></extra>"
    ))

fig.update_layout(
    title=dict(
        text="U.S. Electricity Generation by Energy Source (1990–2024)",
        font=dict(size=18),
        x=0.5,
        xanchor="center"
    ),
    xaxis=dict(
        title="Year",
        tickmode="linear",
        dtick=5
    ),
    yaxis=dict(
        title="Net Generation (TWh)"
    ),
    legend=dict(
        title="Energy Source",
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    hovermode="x unified",
    plot_bgcolor="white",
    paper_bgcolor="white",
)

# Add gridlines for readability
fig.update_xaxes(showgrid=True, gridcolor="#eeeeee")
fig.update_yaxes(showgrid=True, gridcolor="#eeeeee")

fig.show()