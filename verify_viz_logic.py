import pandas as pd
import os

# Mock the logic from 0_Overview.py
def verify_logic():
    print("--- Verifying Logic for 0_Overview.py ---")
    
    # 1. Load Data
    if not os.path.exists("data/processed_studies.csv"):
        print("❌ Data file not found!")
        return

    df = pd.read_csv("data/processed_studies.csv")
    df["StartDate"] = pd.to_datetime(df["StartDate"], errors="coerce")
    df["StartYear"] = df["StartDate"].dt.year
    
    print(f"✅ Data Loaded: {len(df)} rows")
    
    # 2. Segmentation
    metabolic_keywords = ["Diabetes", "Obesity", "Weight", "Metabolic", "NASH", "Liver", "Cardiovascular", "Kidney"]
    def get_segment(condition_str, mech_str):
        c = str(condition_str).lower()
        m = str(mech_str).lower()
        
        if "glp-1" in m or "semaglutide" in m or "tirzepatide" in m:
            return "GLP-1 & Incretins"
        
        if any(k.lower() in c for k in metabolic_keywords):
            return "Legacy Metabolic"
        
        if "cancer" in c or "tumor" in c or "oncology" in c or "lymphoma" in c:
            return "Oncology (The Giant)"
        
        return "All Other Therapy Areas"

    df["Segment"] = df.apply(lambda x: get_segment(x["Conditions"], x["Mechanism"]), axis=1)
    
    # 3. Verify Dynamic Years
    min_year = int(df["StartYear"].min())
    max_year = int(df["StartYear"].max())
    print(f"📅 Year Range: {min_year} - {max_year}")
    
    # 4. Verify GLP-1 Metrics
    glp1_df = df[df["Segment"] == "GLP-1 & Incretins"]
    print(f"🧬 GLP-1 Trials Found: {len(glp1_df)}")
    
    if len(glp1_df) > 0:
        peak_yr = glp1_df["StartYear"].value_counts().idxmax()
        peak_count = glp1_df["StartYear"].value_counts().max()
        print(f"📈 Peak Year: {int(peak_yr)} (Count: {peak_count})")
        
        trials_latest = len(glp1_df[glp1_df["StartYear"] == max_year])
        print(f"📊 Activity in Max Year ({max_year}): {trials_latest}")
    else:
        print("❌ No GLP-1 trials found with current segmentation logic!")

    # 5. Act 1 Check
    act1_df = df[(df["StartYear"] >= 2010) & (df["StartYear"] <= 2018)]
    glp1_act1 = len(act1_df[act1_df["Segment"] == "GLP-1 & Incretins"])
    print(f"🍰 Act 1 (2010-2018) GLP-1 Count: {glp1_act1}")

if __name__ == "__main__":
    verify_logic()
