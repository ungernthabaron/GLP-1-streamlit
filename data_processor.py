import pandas as pd
import json
import os
import re

# Configuration
INPUT_FILE = "data/raw_studies_v2.json"
OUTPUT_FILE = "data/processed_studies.csv"

def load_data():
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found.")
        return []
    
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"Loaded {len(data)} studies.")
    return data

def extract_sponsor(study):
    try:
        return study["protocolSection"]["identificationModule"]["organization"]["fullName"]
    except KeyError:
        try:
            return study["protocolSection"]["sponsorCollaboratorsModule"]["leadSponsor"]["name"]
        except KeyError:
            return "Unknown"

def normalize_sponsor(sponsor):
    sponsor = sponsor.lower()
    if "lilly" in sponsor:
        return "Eli Lilly"
    if "novo nordisk" in sponsor:
        return "Novo Nordisk"
    if "pfizer" in sponsor:
        return "Pfizer"
    if "amgen" in sponsor:
        return "Amgen"
    if "astrazeneca" in sponsor:
        return "AstraZeneca"
    if "boehringer" in sponsor:
        return "Boehringer Ingelheim"
    if "zealand" in sponsor:
        return "Zealand Pharma"
    if "viking" in sponsor:
        return "Viking Therapeutics"
    if "roche" in sponsor:
        return "Roche"
    if "novartis" in sponsor:
        return "Novartis"
    if "moderna" in sponsor:
        return "Moderna"
    if "biontech" in sponsor:
        return "BioNTech"
    if "regeneron" in sponsor:
        return "Regeneron"
    if "sanofi" in sponsor:
        return "Sanofi"
    if "merck" in sponsor:
        return "Merck"
    if "bristol-myers squibb" in sponsor or "bms" in sponsor:
        return "Bristol-Myers Squibb"
    if "gilead" in sponsor:
        return "Gilead Sciences"
    if "biogen" in sponsor:
        return "Biogen"
    if "vertex" in sponsor:
        return "Vertex"
    return sponsor.title()

def extract_phase(study):
    try:
        phases = study["protocolSection"]["designModule"].get("phases", [])
        if not phases:
            # Try to guess from title if phase is missing
            title = study["protocolSection"]["identificationModule"].get("officialTitle", "").lower()
            if "phase 3" in title: return "Phase 3"
            if "phase 2" in title: return "Phase 2"
            if "phase 1" in title: return "Phase 1"
            return "Not Applicable"
            
        # Normalize: PHASE1 -> Phase 1
        normalized = [p.replace("PHASE", "Phase ").replace("EARLY_PHASE1", "Early Phase 1").strip() for p in phases]
        return "/".join(normalized)
    except KeyError:
        return "Unknown"

def determine_mechanism(interventions, title):
    text = (title + " " + " ".join(interventions)).lower()
    
    # Priority check for specific combinations
    if "cagrilintide" in text or "cagrisema" in text:
        return "Amylin Combo"
    if "retatrutide" in text or ("glp-1" in text and "gip" in text and "glucagon" in text):
        return "Triple Agonist"
    if "tirzepatide" in text or ("glp-1" in text and "gip" in text):
        return "Dual Agonist (GLP-1/GIP)"
    if "survodutide" in text or "mazdutide" in text:
        return "Glucagon/GLP-1 Co-agonist"
    if "orforglipron" in text or "danuglipron" in text:
        return "Oral Small Molecule"
    
    # General checks
    if "semaglutide" in text or "liraglutide" in text or "dulaglutide" in text or "exenatide" in text or "ozempic" in text or "wegovy" in text or "mounjaro" in text:
        return "GLP-1 Mono-agonist"
        
    if "glp-1" in text:
        return "GLP-1 Mono-agonist"
        
    # New Categories Logic (Simplified)
    if "pd-1" in text or "pembrolizumab" in text or "nivolumab" in text:
        return "PD-1 Inhibitor"
    if "car-t" in text:
        return "CAR-T Therapy"
    if "crispr" in text or "cas9" in text:
        return "CRISPR/Gene Editing"
    if "mrna" in text:
        return "mRNA Technology"
    if "amyloid" in text or "lecanemab" in text or "donanemab" in text:
        return "Anti-Amyloid Antibody"
        
    return "Other"

def extract_interventions(study):
    try:
        arms = study["protocolSection"].get("armsInterventionsModule", {}).get("interventions", [])
        return [i.get("name", "") for i in arms]
    except KeyError:
        return []

def extract_conditions(study):
    try:
        return study["protocolSection"]["conditionsModule"].get("conditions", [])
    except KeyError:
        return []

def extract_dates(study):
    status_module = study["protocolSection"].get("statusModule", {})
    start_date = status_module.get("startDateStruct", {}).get("date")
    completion_date = status_module.get("primaryCompletionDateStruct", {}).get("date")
    return start_date, completion_date

def process_data(studies):
    processed = []
    
    for study in studies:
        # Extract Market (added by data_collector.py)
        market = study.get("Market", "Unknown")
        
        try:
            nct_id = study["protocolSection"]["identificationModule"]["nctId"]
        except KeyError:
            continue # Skip invalid studies
            
        title = study["protocolSection"]["identificationModule"].get("officialTitle")
        if not title:
            title = study["protocolSection"]["identificationModule"].get("briefTitle", "No Title")
            
        sponsor_raw = extract_sponsor(study)
        sponsor = normalize_sponsor(sponsor_raw)
        
        phase = extract_phase(study)
        
        interventions = extract_interventions(study)
        mechanism = determine_mechanism(interventions, title)
        
        conditions = extract_conditions(study)
        conditions_str = ", ".join(conditions)
        
        start_date, completion_date = extract_dates(study)
        
        status = study["protocolSection"]["statusModule"].get("overallStatus", "Unknown")
        
        processed.append({
            "NCTId": nct_id,
            "Market": market, # New field
            "Title": title,
            "Sponsor": sponsor,
            "Phase": phase,
            "Mechanism": mechanism,
            "Interventions": ", ".join(interventions),
            "Conditions": conditions_str,
            "Status": status,
            "StartDate": start_date,
            "CompletionDate": completion_date
        })
        
    return pd.DataFrame(processed)

if __name__ == "__main__":
    studies = load_data()
    if studies:
        df = process_data(studies)
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Processed data saved to {OUTPUT_FILE}")
        print(df.head())
        print(df["Market"].value_counts())
