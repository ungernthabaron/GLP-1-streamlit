import pandas as pd

df = pd.read_csv("data/processed_studies.csv")

print(f"Total studies: {len(df)}")

# Check Phase quality
valid_phases = ["Early Phase 1", "Phase 1", "Phase 1/Phase 2", "Phase 2", "Phase 2/Phase 3", "Phase 3", "Phase 4"]
df_valid_phase = df[df["Phase"].isin(valid_phases)]
print(f"Studies with valid phase: {len(df_valid_phase)} ({len(df_valid_phase)/len(df):.1%})")

# Check Date quality for Phase 3
df_phase3 = df[df["Phase"].str.contains("Phase 3", na=False)]
print(f"Total Phase 3 studies: {len(df_phase3)}")
df_phase3_dates = df_phase3.dropna(subset=["StartDate", "CompletionDate"])
print(f"Phase 3 studies with dates: {len(df_phase3_dates)}")

# Top sponsors with VALID phases
print("\nTop Sponsors by VALID Phase count:")
print(df_valid_phase["Sponsor"].value_counts().head(10))

# Check what the "Top 10" in the app are currently
top_sponsors_all = df["Sponsor"].value_counts().head(10).index.tolist()
print(f"\nTop 10 Sponsors (by total volume) used in App default: {top_sponsors_all}")

# Check overlap
print("\nOverlap check:")
for s in top_sponsors_all:
    count = len(df_valid_phase[df_valid_phase["Sponsor"] == s])
    print(f"{s}: {count} valid phase studies")
