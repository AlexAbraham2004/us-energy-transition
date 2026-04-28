import pandas as pd
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html


DATA_PATH = "data/cleaned/cleaned_energy_data.csv"

CATEGORY_ORDER = ["Fossil Fuel", "Nuclear", "Renewable", "Other"]
CATEGORY_COLORS = {
    "Fossil Fuel": "#d62728",
    "Nuclear": "#ff7f0e",
    "Renewable": "#2ca02c",
    "Other": "#aec7e8",
}

SOURCE_ORDER = [
    "Coal",
    "Natural Gas",
    "Hydroelectric Conventional",
    "Wind",
    "Solar Thermal and Photovoltaic",
]
SOURCE_LABELS = {
    "Coal": "Coal",
    "Natural Gas": "Natural Gas",
    "Hydroelectric Conventional": "Hydroelectric",
    "Wind": "Wind",
    "Solar Thermal and Photovoltaic": "Solar",
}
SOURCE_COLORS = {
    "Coal": "#4a4a4a",
    "Natural Gas": "#e377c2",
    "Hydroelectric Conventional": "#1f77b4",
    "Wind": "#17becf",
    "Solar Thermal and Photovoltaic": "#f7b731",
}


def _empty_figure(title: str, message: str) -> go.Figure:
    fig = go.Figure()
    fig.update_layout(
        title=title,
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=45, r=25, t=60, b=45),
    )
    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=15, color="#4a5568"),
        align="center",
    )
    return fig


def _load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    return df


def _filter_states(df: pd.DataFrame, selected_states: list[str]) -> pd.DataFrame:
    if not selected_states:
        return df
    return df[df["state"].isin(selected_states)]


def build_mix_chart(df: pd.DataFrame, start_year: int, end_year: int) -> go.Figure:
    window = df[(df["year"] >= start_year) & (df["year"] <= end_year)]
    if window.empty:
        return _empty_figure(
            "1) National/Selected-State Energy Mix Over Time",
            "No data for selected filters.",
        )
    grouped = window.groupby(["year", "category"])["generation_mwh"].sum().reset_index()
    pivot = grouped.pivot(index="year", columns="category", values="generation_mwh").fillna(0)

    for category in CATEGORY_ORDER:
        if category not in pivot.columns:
            pivot[category] = 0

    pivot = pivot[CATEGORY_ORDER] / 1e6  # TWh

    fig = go.Figure()
    for category in CATEGORY_ORDER:
        fig.add_trace(
            go.Scatter(
                x=pivot.index,
                y=pivot[category],
                name=category,
                mode="lines",
                stackgroup="one",
                fillcolor=CATEGORY_COLORS[category],
                line=dict(color=CATEGORY_COLORS[category], width=0.5),
                hovertemplate=f"%{{x}}<br>{category}: %{{y:.2f}} TWh<extra></extra>",
            )
        )

    fig.update_layout(
        title="1) National/Selected-State Energy Mix Over Time",
        xaxis=dict(title="Year", tickmode="linear", dtick=5),
        yaxis=dict(title="Net Generation (TWh)"),
        legend=dict(title="Category", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=45, r=25, t=60, b=45),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#eeeeee")
    fig.update_yaxes(showgrid=True, gridcolor="#eeeeee")
    return fig


def build_source_chart(
    df: pd.DataFrame, selected_sources: list[str], start_year: int, end_year: int
) -> go.Figure:
    sources = selected_sources or SOURCE_ORDER
    window = df[
        (df["year"] >= start_year)
        & (df["year"] <= end_year)
        & (df["energy_source"].isin(sources))
    ]
    if window.empty:
        return _empty_figure("2) Key Energy Sources Trend", "No data for selected filters.")
    grouped = window.groupby(["year", "energy_source"])["generation_mwh"].sum().reset_index()
    grouped["generation_twh"] = grouped["generation_mwh"] / 1e6

    fig = go.Figure()
    for source in SOURCE_ORDER:
        if source not in sources:
            continue
        source_data = grouped[grouped["energy_source"] == source]
        fig.add_trace(
            go.Scatter(
                x=source_data["year"],
                y=source_data["generation_twh"],
                name=SOURCE_LABELS[source],
                mode="lines",
                line=dict(color=SOURCE_COLORS[source], width=2.5),
                hovertemplate=f"%{{x}}<br>{SOURCE_LABELS[source]}: %{{y:.2f}} TWh<extra></extra>",
            )
        )

    fig.update_layout(
        title="2) Key Energy Sources Trend",
        xaxis=dict(title="Year", tickmode="linear", dtick=5),
        yaxis=dict(title="Net Generation (TWh)"),
        legend=dict(title="Energy Source", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=45, r=25, t=60, b=45),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#eeeeee")
    fig.update_yaxes(showgrid=True, gridcolor="#eeeeee")
    return fig


def build_map_chart(df: pd.DataFrame, map_year: int) -> go.Figure:
    year_df = df[df["year"] == map_year]
    if year_df.empty:
        return _empty_figure(
            f"3) Renewable Share by State ({map_year})",
            "No data for selected filters.",
        )
    totals = year_df.groupby("state")["generation_mwh"].sum().rename("total_mwh")
    renewable = (
        year_df[year_df["category"] == "Renewable"]
        .groupby("state")["generation_mwh"]
        .sum()
        .rename("renewable_mwh")
    )
    merged = pd.concat([totals, renewable], axis=1).fillna(0).reset_index()
    merged = merged[merged["total_mwh"] > 0]
    if merged.empty:
        return _empty_figure(
            f"3) Renewable Share by State ({map_year})",
            "No data for selected filters.",
        )
    merged["renewable_share"] = merged["renewable_mwh"] / merged["total_mwh"] * 100

    fig = go.Figure(
        data=go.Choropleth(
            locations=merged["state"],
            z=merged["renewable_share"],
            locationmode="USA-states",
            colorscale="Greens",
            colorbar=dict(title="Renewable Share (%)", ticksuffix="%"),
            hovertemplate="<b>%{location}</b><br>Renewable Share: %{z:.1f}%<extra></extra>",
        )
    )
    fig.update_layout(
        title=f"3) Renewable Share by State ({map_year})",
        geo=dict(scope="usa", projection=dict(type="albers usa"), showlakes=True, lakecolor="lightblue"),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=25, r=25, t=60, b=25),
    )
    return fig


def _renewable_share(df: pd.DataFrame, year: int) -> pd.Series:
    year_df = df[df["year"] == year]
    totals = year_df.groupby("state")["generation_mwh"].sum()
    renewable = year_df[year_df["category"] == "Renewable"].groupby("state")["generation_mwh"].sum()
    return (renewable / totals * 100).rename(str(year))


def build_change_chart(df: pd.DataFrame, baseline_year: int, comparison_year: int) -> go.Figure:
    baseline = _renewable_share(df, baseline_year)
    comparison = _renewable_share(df, comparison_year)
    change = (comparison - baseline).reset_index()
    change.columns = ["state", "change"]
    change = change.dropna().sort_values("change", ascending=True)
    if change.empty:
        return _empty_figure(
            f"4) Change in Renewable Share by State ({baseline_year} to {comparison_year})",
            "No data for selected filters.",
        )
    colors = ["#2ca02c" if value >= 0 else "#d62728" for value in change["change"]]

    fig = go.Figure(
        go.Bar(
            x=change["change"],
            y=change["state"],
            orientation="h",
            marker_color=colors,
            hovertemplate="<b>%{y}</b><br>Change: %{x:.1f} pp<extra></extra>",
        )
    )
    fig.update_layout(
        title=f"4) Change in Renewable Share by State ({baseline_year} to {comparison_year})",
        xaxis=dict(
            title="Change in Renewable Share (percentage points)",
            zeroline=True,
            zerolinecolor="#333333",
            zerolinewidth=1.5,
        ),
        yaxis=dict(title="State", tickfont=dict(size=10)),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=55, r=25, t=60, b=45),
    )
    fig.update_xaxes(showgrid=True, gridcolor="#eeeeee")
    fig.update_yaxes(showgrid=False)
    return fig


df = _load_data()
year_min = int(df["year"].min())
year_max = int(df["year"].max())
all_states = sorted(df["state"].dropna().unique().tolist())

app = Dash(__name__)
app.title = "U.S. Energy Transition Dashboard"

app.layout = html.Div(
    style={
        "maxWidth": "1500px",
        "margin": "0 auto",
        "padding": "20px 24px 30px 24px",
        "fontFamily": "Arial, sans-serif",
        "backgroundColor": "#f7f9fc",
    },
    children=[
        html.H2(
            "Renewable Energy Growth vs. Fossil Fuel Use in the United States",
            style={"textAlign": "center", "marginBottom": "6px"},
        ),
        html.P(
            "Interactive dashboard: explore national trends, key sources, geographic differences, "
            "and state-by-state transition momentum.",
            style={"textAlign": "center", "color": "#4a5568", "marginTop": "0", "marginBottom": "18px"},
        ),
        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "repeat(5, minmax(180px, 1fr))",
                "gap": "12px",
                "marginBottom": "14px",
                "backgroundColor": "white",
                "border": "1px solid #e2e8f0",
                "borderRadius": "10px",
                "padding": "14px",
            },
            children=[
                html.Div(
                    [
                        html.Label("States (optional filter)", style={"fontWeight": "bold"}),
                        dcc.Dropdown(
                            id="state-filter",
                            options=[{"label": st, "value": st} for st in all_states],
                            value=[],
                            multi=True,
                            placeholder="All states",
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.Label("Energy sources (line chart)", style={"fontWeight": "bold"}),
                        dcc.Dropdown(
                            id="source-filter",
                            options=[{"label": SOURCE_LABELS[src], "value": src} for src in SOURCE_ORDER],
                            value=SOURCE_ORDER,
                            multi=True,
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.Label("Trend window", style={"fontWeight": "bold"}),
                        dcc.RangeSlider(
                            id="year-range",
                            min=year_min,
                            max=year_max,
                            value=[max(year_min, 1990), year_max],
                            marks={
                                y: str(y)
                                for y in range(
                                    (year_min // 5) * 5,
                                    year_max + 1,
                                    5,
                                )
                                if year_min <= y <= year_max
                            },
                            tooltip={"always_visible": False, "placement": "bottom"},
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.Label("Map year", style={"fontWeight": "bold"}),
                        dcc.Slider(
                            id="map-year",
                            min=year_min,
                            max=year_max,
                            value=year_max,
                            marks={
                                year_min: str(year_min),
                                year_max: str(year_max),
                            },
                            tooltip={"always_visible": False, "placement": "bottom"},
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.Label("Change chart years", style={"fontWeight": "bold"}),
                        html.Div(
                            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "8px"},
                            children=[
                                dcc.Dropdown(
                                    id="baseline-year",
                                    options=[{"label": str(y), "value": y} for y in range(year_min, year_max)],
                                    value=max(year_min, 2000),
                                    clearable=False,
                                ),
                                dcc.Dropdown(
                                    id="comparison-year",
                                    options=[{"label": str(y), "value": y} for y in range(year_min + 1, year_max + 1)],
                                    value=year_max,
                                    clearable=False,
                                ),
                            ],
                        ),
                    ]
                ),
            ],
        ),
        html.Div(
            style={"display": "flex", "justifyContent": "flex-end", "marginBottom": "12px"},
            children=[
                html.Button(
                    "Reset filters",
                    id="reset-filters",
                    n_clicks=0,
                    style={
                        "backgroundColor": "#2b6cb0",
                        "color": "white",
                        "border": "none",
                        "padding": "8px 12px",
                        "borderRadius": "6px",
                        "cursor": "pointer",
                    },
                )
            ],
        ),
        html.Div(
            id="validation-note",
            style={
                "minHeight": "22px",
                "marginBottom": "6px",
                "color": "#9b2c2c",
                "fontSize": "0.92rem",
                "fontWeight": "bold",
            },
        ),
        html.Div(
            style={"display": "grid", "gridTemplateColumns": "1fr 1fr", "gap": "14px"},
            children=[
                dcc.Graph(id="mix-chart", config={"displaylogo": False}),
                dcc.Graph(id="source-chart", config={"displaylogo": False}),
                dcc.Graph(id="map-chart", config={"displaylogo": False}),
                dcc.Graph(id="change-chart", config={"displaylogo": False}),
            ],
        ),
        html.P(
            "Story flow: mix shift -> source-level trends -> geography snapshot -> long-run state momentum.",
            style={"textAlign": "center", "color": "#2d3748", "marginTop": "8px", "marginBottom": "0"},
        ),
    ],
)


@app.callback(
    Output("mix-chart", "figure"),
    Output("source-chart", "figure"),
    Output("map-chart", "figure"),
    Output("change-chart", "figure"),
    Output("validation-note", "children"),
    Input("state-filter", "value"),
    Input("source-filter", "value"),
    Input("year-range", "value"),
    Input("map-year", "value"),
    Input("baseline-year", "value"),
    Input("comparison-year", "value"),
)
def update_dashboard(
    selected_states: list[str],
    selected_sources: list[str],
    year_range: list[int],
    map_year: int,
    baseline_year: int,
    comparison_year: int,
):
    selected_states = selected_states or []
    selected_sources = selected_sources or SOURCE_ORDER
    start_year, end_year = year_range
    year_filtered = df[(df["year"] >= start_year) & (df["year"] <= end_year)]
    scope_df = _filter_states(year_filtered, selected_states)

    note = ""
    if baseline_year >= comparison_year:
        note = "Baseline year must be earlier than comparison year."

    mix_fig = build_mix_chart(scope_df, start_year, end_year)
    source_fig = build_source_chart(scope_df, selected_sources, start_year, end_year)
    map_fig = build_map_chart(scope_df, map_year)
    if baseline_year >= comparison_year:
        change_fig = go.Figure()
        change_fig.update_layout(
            title=f"4) Change in Renewable Share by State ({baseline_year} to {comparison_year})",
            plot_bgcolor="white",
            paper_bgcolor="white",
            margin=dict(l=55, r=25, t=60, b=45),
        )
        change_fig.add_annotation(
            text="Choose a baseline year earlier than comparison year.",
            x=0.5,
            y=0.5,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=14, color="#4a5568"),
            align="center",
        )
    else:
        change_fig = build_change_chart(scope_df, baseline_year, comparison_year)
    return mix_fig, source_fig, map_fig, change_fig, note


@app.callback(
    Output("state-filter", "value"),
    Output("source-filter", "value"),
    Output("year-range", "value"),
    Output("map-year", "value"),
    Output("baseline-year", "value"),
    Output("comparison-year", "value"),
    Input("reset-filters", "n_clicks"),
    prevent_initial_call=True,
)
def reset_filters(_: int):
    return [], SOURCE_ORDER, [max(year_min, 1990), year_max], year_max, max(year_min, 2000), year_max


if __name__ == "__main__":
    app.run(debug=False)
