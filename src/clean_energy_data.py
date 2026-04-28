import pandas as pd

# Load the raw Excel file (header is on row 2, so we skip the first row)
df = pd.read_excel("data/raw/annual_generation_state.xls", engine="xlrd", header=1)

# We only want the total industry figures to avoid double counting across producer types
df = df[df["TYPE OF PRODUCER"] == "Total Electric Power Industry"]

# Remove the US total rows and any blank state entries
df = df[~df["STATE"].isin(["US-TOTAL", "US-Total", "  "])]
df["STATE"] = df["STATE"].str.strip()
df = df[df["STATE"] != ""]

# Drop the "Total" rows since they are just aggregates, also drop Pumped Storage
# because it records negative generation and isn't a real energy source
df = df[~df["ENERGY SOURCE"].isin(["Total", "Pumped Storage"])]

# Rename columns to be cleaner and easier to work with
df = df.rename(columns={
    "YEAR": "year",
    "STATE": "state",
    "TYPE OF PRODUCER": "producer_type",
    "ENERGY SOURCE": "energy_source",
    "GENERATION (Megawatthours)": "generation_mwh"
})

# Drop producer_type since every row is the same value now
df = df.drop(columns=["producer_type"])

# Group each energy source into a broader category
renewables = ["Hydroelectric Conventional", "Wind",
              "Solar Thermal and Photovoltaic", "Geothermal",
              "Wood and Wood Derived Fuels", "Other Biomass"]
fossil_fuels = ["Coal", "Natural Gas", "Petroleum", "Other Gases"]
nuclear = ["Nuclear"]

def categorize(source):
    if source in renewables:
        return "Renewable"
    elif source in fossil_fuels:
        return "Fossil Fuel"
    elif source in nuclear:
        return "Nuclear"
    else:
        return "Other"

df["category"] = df["energy_source"].apply(categorize)

# A small number of rows have slightly negative values due to rounding, set them to 0
df["generation_mwh"] = df["generation_mwh"].clip(lower=0)

# Reset the index after all the filtering
df = df.reset_index(drop=True)

# Save the cleaned data to a CSV
df.to_csv("data/cleaned/cleaned_energy_data.csv", index=False)

print(f"Shape: {df.shape}")
print(f"Years: {df['year'].min()} to {df['year'].max()}")
print(f"States: {df['state'].nunique()}")
print(f"Energy sources: {df['energy_source'].nunique()}")
print(f"Null values: {df.isnull().sum().sum()}")
print(f"Negative values: {(df['generation_mwh'] < 0).sum()}")
print()
print("Categories:")
print(df["category"].value_counts())
print()
print("Preview:")
print(df.head(10))