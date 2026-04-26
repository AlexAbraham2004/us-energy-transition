import pandas as pd
import plotly.graph_objects as go

# Load the cleaned dataset
df = pd.read_csv("data/cleaned/cleaned_energy_data.csv")

# Function to calculate renewable share for a given year
def renewable_share(year):
    d = df[df["year"] == year]
    total = d.groupby("state")["generation_mwh"].sum()
    renewable = d[d["category"] == "Renewable"].groupby("state")["generation_mwh"].sum()
    return (renewable / total * 100).rename(year)

# Calculate share for 2000 and 2024
share_2000 = renewable_share(2000)
share_2024 = renewable_share(2024)

# Calculate the change and sort
change = (share_2024 - share_2000).reset_index()
change.columns = ["state", "change"]
change = change.dropna()  # Drop DC which has no data
change = change.sort_values("change", ascending=True)  # ascending for horizontal bar

# Color bars by positive (green) or negative (red) change
colors = ["#2ca02c" if v >= 0 else "#d62728" for v in change["change"]]

# Build the bar chart
fig = go.Figure(go.Bar(
    x=change["change"],
    y=change["state"],
    orientation="h",
    marker_color=colors,
    hovertemplate="<b>%{y}</b><br>Change: %{x:.1f}%<extra></extra>"
))

fig.update_layout(
    title=dict(
        text="Change in Renewable Energy Share by State (2000–2024)",
        font=dict(size=18),
        x=0.5,
        xanchor="center"
    ),
    xaxis=dict(
        title="Change in Renewable Share (percentage points)",
        zeroline=True,
        zerolinecolor="#333333",
        zerolinewidth=1.5
    ),
    yaxis=dict(
        title="State",
        tickfont=dict(size=11)
    ),
    plot_bgcolor="white",
    paper_bgcolor="white",
    height=700,
    margin=dict(l=60, r=40, t=60, b=60)
)

fig.update_xaxes(showgrid=True, gridcolor="#eeeeee")

fig.show()