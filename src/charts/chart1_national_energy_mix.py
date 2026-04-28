import pandas as pd
import plotly.graph_objects as go

def create_chart(df):
    # Aggregate generation nationally by year and category
    national = df.groupby(["year", "category"])["generation_mwh"].sum().reset_index()

    # Pivot so each category becomes its own column
    national_pivot = national.pivot(index="year", columns="category", values="generation_mwh").fillna(0)

    # Order the categories for stacking (bottom to top)
    category_order = ["Fossil Fuel", "Nuclear", "Renewable", "Other"]
    national_pivot = national_pivot[category_order]

    # Convert MWh to TWh for readability on the y-axis
    national_pivot = national_pivot / 1e6

    # Colors for each category
    colors = {
        "Fossil Fuel": "#d62728",
        "Nuclear":     "#ff7f0e",
        "Renewable":   "#2ca02c",
        "Other":       "#aec7e8"
    }

    # Build the stacked area chart
    fig = go.Figure()

    for category in category_order:
        fig.add_trace(go.Scatter(
            x=national_pivot.index,
            y=national_pivot[category],
            name=category,
            mode="lines",
            stackgroup="one",
            fillcolor=colors[category],
            line=dict(color=colors[category], width=0.5),
            hovertemplate="%{x}<br>" + category + ": %{y:.2f} TWh<extra></extra>"
        ))

    # Annotations pointing to the actual dips in total generation
    annotations = [
        dict(
            x=2009, y=3955,
            text="2008 Financial Crisis",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#333333",
            ax=60, ay=-50,
            font=dict(size=12, color="#333333"),
            bgcolor="white",
            bordercolor="#333333",
            borderwidth=1,
            borderpad=4
        ),
        dict(
            x=2020, y=4015,
            text="2020 COVID-19",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#333333",
            ax=-80, ay=-50,
            font=dict(size=12, color="#333333"),
            bgcolor="white",
            bordercolor="#333333",
            borderwidth=1,
            borderpad=4
        )
    ]

    fig.update_layout(
        title=dict(
            text="U.S. Electricity Generation by Energy Category (1990–2024)",
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
            title="Net Generation (TWh)",
        ),
        legend=dict(
            title="Category",
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            traceorder="normal"
        ),
        annotations=annotations,
        hovermode="x unified",
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    return fig

if __name__ == "__main__":
    df = pd.read_csv("data/cleaned/cleaned_energy_data.csv")
    create_chart(df).show()