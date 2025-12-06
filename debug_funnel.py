import pandas as pd

# Load data
df = pd.read_csv("data/processed_studies.csv")

# Reproduce App Logic
top_sponsors = df["Sponsor"].value_counts().head(10).index.tolist()
all_mechanisms = sorted(df["Mechanism"].unique().tolist())

print(f"Top 10 Sponsors: {top_sponsors}")

# Filter
filtered_df = df[
    (df["Sponsor"].isin(top_sponsors)) & 
    (df["Mechanism"].isin(all_mechanisms))
]

print(f"Filtered Data Size: {len(filtered_df)}")
print("\n--- Phase Distribution in Filtered Data ---")
print(filtered_df["Phase"].value_counts())

print("\n--- Sample of 'Not Applicable' studies ---")
print(filtered_df[filtered_df["Phase"] == "Not Applicable"][["Title", "Sponsor", "Mechanism"]].head())
