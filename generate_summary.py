import pandas as pd

# Load processed data
df = pd.read_csv("data/processed_studies.csv")

# 1. Aggregation by Market, Phase, and Sponsor
summary = df.groupby(["Market", "Phase", "Sponsor"]).size().reset_index(name="Study_Count")

# Sort by count descending
summary = summary.sort_values("Study_Count", ascending=False)

# Save to CSV
output_file = "data/market_summary.csv"
summary.to_csv(output_file, index=False)

print(f"Summary saved to {output_file}")
print(summary.head())

# Also generate a high-level market overview
market_overview = df.groupby("Market").agg({
    "NCTId": "count",
    "Sponsor": lambda x: x.mode()[0] if not x.mode().empty else "Unknown",
    "Phase": lambda x: x.mode()[0] if not x.mode().empty else "Unknown"
}).reset_index()
market_overview.columns = ["Market", "Total_Studies", "Top_Sponsor", "Most_Common_Phase"]
market_overview.to_csv("data/market_overview.csv", index=False)
print(f"Market overview saved to data/market_overview.csv")
