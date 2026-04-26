# U.S. Energy Transition (1990–2024)

Final project for CSc 47400 — Data Visualization. This project analyzes how electricity generation has shifted between renewable energy and fossil fuels across all 50 U.S. states from 1990 to 2024, using data from the U.S. Energy Information Administration (EIA).

## Research Question
How has the balance between renewable and fossil fuel electricity generation shifted across U.S. states from 1990 to 2024, and which states have emerged as leaders or laggards in the energy transition?

## Deliverables
- **Interactive Dashboard** — Built with Dash, allows users to filter by state and energy source
- **Infographic** — Four static visualizations built with Plotly telling a connected story about the U.S. energy transition

## Visualizations
1. U.S. Electricity Generation by Energy Category (1990–2024) — Stacked area chart showing the national energy mix over time
2. U.S. Electricity Generation by Energy Source (1990–2024) — Line chart tracking Coal, Natural Gas, Hydroelectric, Wind, and Solar individually
3. Renewable Share by State in 2024 — Choropleth map showing the geographic energy divide
4. Change in Renewable Share by State (2000–2024) — Bar chart ranking states by how much they have shifted toward renewables

## Data Source
[EIA — Net Generation by State by Type of Producer by Energy Source](https://www.eia.gov/electricity/data/state/)
Date range: 1990–2024

## Tools
- Python
- Pandas
- Plotly
- Dash

## Project Structure
```
us-energy-transition/
│
├── data/
│   ├── raw/
│   │   └── annual_generation_state.xls
│   └── cleaned/
│       └── cleaned_energy_data.csv
│
├── clean_energy_data.py
├── chart1_national_energy_mix.py
├── chart2_energy_sources.py
├── chart3_choropleth_map.py
├── chart4_state_renewable_change.py
└── README.md
```