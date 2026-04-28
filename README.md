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

## How to Run

Run all commands from the repository root (`us-energy-transition/`).

### 1. Install dependencies
```
pip install pandas plotly dash kaleido xlrd
```

### 2. Clean the data
Run this first to generate the cleaned CSV from the raw EIA file:
```
python src/clean_energy_data.py
```

### 3. View individual charts
Each chart can be run on its own and will open in your browser:
```
python src/charts/chart1_national_energy_mix.py
python src/charts/chart2_energy_sources.py
python src/charts/chart3_choropleth_map.py
python src/charts/chart4_state_renewable_change.py
```

### 4. Generate the infographic
This combines all 4 charts into a single static image (`outputs/infographic.png`):
```
python src/infographic.py
```

### 5. Run the dashboard
```
python src/dashboard.py
```
Then open your browser and go to `http://127.0.0.1:8050`

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
├── src/
│   ├── charts/
│   │   ├── chart1_national_energy_mix.py
│   │   ├── chart2_energy_sources.py
│   │   ├── chart3_choropleth_map.py
│   │   └── chart4_state_renewable_change.py
│   ├── clean_energy_data.py
│   ├── dashboard.py
│   └── infographic.py
├── outputs/
│   └── infographic.png
├── docs/
│   └── Final_Project_Proposal.pdf
└── README.md
```