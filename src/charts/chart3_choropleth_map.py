import pandas as pd
import plotly.graph_objects as go

def create_chart(df):
    # Filter to 2024 only
    df_2024 = df[df["year"] == 2024]

    # Calculate total generation per state
    total = df_2024.groupby("state")["generation_mwh"].sum().reset_index()
    total.columns = ["state", "total_mwh"]

    # Calculate renewable generation per state
    renewable = df_2024[df_2024["category"] == "Renewable"].groupby("state")["generation_mwh"].sum().reset_index()
    renewable.columns = ["state", "renewable_mwh"]

    # Merge and calculate renewable share
    merged = total.merge(renewable, on="state")
    merged["renewable_share"] = (merged["renewable_mwh"] / merged["total_mwh"]) * 100

    # Build the choropleth map
    fig = go.Figure(data=go.Choropleth(
        locations=merged["state"],
        z=merged["renewable_share"],
        locationmode="USA-states",
        colorscale="Greens",
        colorbar=dict(
            title=dict(text="Renewable Share (%)", font=dict(size=13)),
            ticksuffix="%"
        ),
        hovertemplate="<b>%{location}</b><br>Renewable Share: %{z:.1f}%<extra></extra>"
    ))

    fig.update_layout(
        title=dict(
            text="Renewable Energy Share of Electricity Generation by State (2024)",
            font=dict(size=18),
            x=0.5,
            xanchor="center"
        ),
        geo=dict(
            scope="usa",
            projection=dict(type="albers usa"),
            showlakes=True,
            lakecolor="lightblue"
        ),
        paper_bgcolor="white"
    )

    return fig


if __name__ == "__main__":
    df = pd.read_csv("data/cleaned/cleaned_energy_data.csv")
    create_chart(df).show()