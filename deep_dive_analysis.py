import pandas as pd
from collections import Counter
import re

df = pd.read_csv("data/processed_studies.csv")

print(f"Total studies: {len(df)}")

# 1. Analyze Conditions (Indications)
# The 'Conditions' column is a list-like string. We need to parse it.
all_conditions = []
for cond_str in df["Conditions"].dropna():
    # Simple cleanup
    conds = eval(cond_str) if cond_str.startswith("[") else [cond_str]
    all_conditions.extend(conds)

# Filter out generic terms
ignore_terms = ["Diabetes", "Type 2", "Obesity", "Overweight", "Healthy", "Pharmacokinetics", "Safety"]
filtered_conditions = [c for c in all_conditions if not any(term.lower() in c.lower() for term in ignore_terms)]

print("\n--- Top 20 'Surprising' Indications (excluding Diabetes/Obesity) ---")
print(Counter(filtered_conditions).most_common(20))

# 2. Analyze "Oral" trend
# Check if "Oral" appears in Title or Interventions
df["Is_Oral"] = df["Title"].str.contains("Oral", case=False) | df["Interventions"].str.contains("Oral", case=False) | df["Mechanism"].str.contains("Oral", case=False)
oral_studies = df[df["Is_Oral"]]
print(f"\nTotal Oral GLP-1 Studies: {len(oral_studies)}")
print("Top Sponsors for Oral Drugs:")
print(oral_studies["Sponsor"].value_counts().head(10))

# 3. Competitor Watch (Who is not Novo or Lilly?)
others = df[~df["Sponsor"].isin(["Novo Nordisk", "Eli Lilly", "Eli Lilly and Company"])]
print("\n--- Top Challengers (Non-Duopoly) ---")
print(others["Sponsor"].value_counts().head(10))
