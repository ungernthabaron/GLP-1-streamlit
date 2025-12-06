import pandas as pd

df = pd.read_csv("data/processed_studies.csv")

print("--- PHASES ---")
print(df["Phase"].value_counts())

print("\n--- MECHANISMS ---")
print(df["Mechanism"].value_counts())

print("\n--- TOP 20 SPONSORS ---")
print(df["Sponsor"].value_counts().head(20))
