import requests
import json
import time
import os

# Configuration
BASE_URL = "https://clinicaltrials.gov/api/v2/studies"
OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "raw_studies.json")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Search parameters
# Dictionary of market segments and their key terms
MARKETS = {
    "GLP-1": [
        "GLP-1", "Semaglutide", "Ozempic", "Wegovy", "Tirzepatide", "Mounjaro", "Zepbound", 
        "Retatrutide", "CagriSema", "Orforglipron", "Amylin"
    ],
    "Oncology (PD-1/CAR-T)": [
        "PD-1", "PD-L1", "CAR-T", "Pembrolizumab", "Nivolumab", "Ipilimumab", "Atezolizumab"
    ],
    "Gene Therapy (CRISPR)": [
        "CRISPR", "Cas9", "Gene Editing", "Zinc Finger Nuclease", "TALEN", "Exa-cel"
    ],
    "Alzheimer's": [
        "Alzheimer", "Amyloid", "Tau", "Lecanemab", "Donanemab", "Aducanumab"
    ],
    "mRNA": [
        "mRNA", "Messenger RNA", "Moderna", "BioNTech", "BNT162b2", "mRNA-1273"
    ]
}

PARAMS = {
    "format": "json",
    "pageSize": 100,
    "sort": "StudyFirstPostDate:desc", # Fetch newest first to fill the timeline gap
}

def fetch_studies():
    all_studies = []
    
    for market, terms in MARKETS.items():
        query_term = " OR ".join(terms)
        print(f"\n--- Collecting data for: {market} ---")
        
        current_studies = []
        next_page_token = None
        page_count = 0
        
        # Production Mode: Increased to 10k as requested to fill data gaps
        MAX_STUDIES_PER_CAT = 100000 
        
        while len(current_studies) < MAX_STUDIES_PER_CAT:
            request_params = PARAMS.copy()
            request_params["query.term"] = query_term
            if next_page_token:
                request_params["pageToken"] = next_page_token
                
            try:
                response = requests.get(BASE_URL, params=request_params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                studies = data.get("studies", [])
                if not studies:
                    break
                    
                # Tag each study with its market category
                for s in studies:
                    s["Market"] = market
                    
                current_studies.extend(studies)
                
                page_count += 1
                if page_count % 5 == 0:
                    print(f"  Page {page_count} fetched. Count: {len(current_studies)}")
                
                next_page_token = data.get("nextPageToken")
                if not next_page_token:
                    break
                    
                time.sleep(0.2) # Slightly faster but still polite
                
            except requests.exceptions.RequestException as e:
                print(f"  Error fetching data: {e}")
                # Retry logic could go here, but for now we break to save what we have
                break
        
        print(f"  Finished {market}. Total: {len(current_studies)}")
        all_studies.extend(current_studies)
        
        # Incremental Save
        save_data(all_studies)
            
    print(f"\nTotal studies fetched across all markets: {len(all_studies)}")
    return all_studies

def save_data(studies):
    # Save to a new v2 file to preserve original if needed, or overwrite
    output_file = os.path.join(OUTPUT_DIR, "raw_studies_v2.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(studies, f, indent=2, ensure_ascii=False)
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    studies = fetch_studies()
    if studies:
        save_data(studies)
