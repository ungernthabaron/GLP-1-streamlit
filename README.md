# 🌍 Global Pharma Trends: The "Ozempic Effect" & Beyond

**Project Status:** ✅ Completed (Production Ready)
**Data Source:** ClinicalTrials.gov API v2 (Real-time)
**Dataset:** ~27,500 Clinical Trials (2010-2025)

## 🎯 Project Objective
Originally designed to analyze the **GLP-1 (Ozempic)** market, this project expanded into a **Global Comparative Analysis** of the pharmaceutical industry's hottest trends. We answer the question: *"Is the hype real, and who is winning?"*

## 📊 Key Dashboards

### 1. 🚀 The "Economics of Hype" (App.py)
*   **Financial Gravity:** Visualizes how the 99% profit margin of GLP-1 drugs (COGS <$5 vs Price $1000) is reshaping the industry.
*   **R&D Burn Rate:** Tracks billions of dollars flowing from "Big Pharma" into weight loss trials.
*   **The Rise of Ozempic:** A historical timeline showing the pivot from Diabetes (2017) to Lifestyle/Obesity (2021).

### 2. 📈 Global Trends (pages/1_Global_Trends.py)
A comparative "Battle Royale" between 5 major market segments:
1.  **GLP-1 (Obesity/Diabetes):** The Challenger.
2.  **Oncology (PD-1/CAR-T):** The Incumbent King.
3.  **Gene Therapy (CRISPR):** The High-Risk Future.
4.  **Alzheimer's:** The Graveyard of Drugs.
5.  **mRNA:** The Pandemic Star.

**Key Visualizations:**
*   **Growth Over Time:** Proves the "Hype" by comparing the vertical growth of GLP-1 trials vs. the steady baseline of Oncology.
*   **The "Valley of Death" Proxy:** Compares Phase 1 vs. Phase 3 ratios to estimate attrition risk.
*   **Sankey Diagram:** Maps the strategy of giants (Novo Nordisk, Eli Lilly, Pfizer) — who is diversifying and who is going "All-in".

## 🛠️ Tech Stack
*   **Core:** Python 3.11+
*   **Frontend:** Streamlit (with Custom CSS for "Dark Glassmorphism" UI)
*   **Visualization:** Plotly Express & Graph Objects
*   **Data Engineering:** Custom ETL pipeline (`data_collector.py`, `data_processor.py`) handling pagination, rate limits, and data normalization.

## 🚀 How to Run
1.  **Install Dependencies:**
    ```bash
    pip install streamlit pandas plotly requests
    ```
2.  **Collect Data (Optional - Data already included):**
    ```bash
    python data_collector.py
    ```
    *(Fetches ~27k studies with date sorting to ensure timeline continuity)*
3.  **Process Data:**
    ```bash
    python data_processor.py
    ```
4.  **Launch Dashboard:**
    ```bash
    python -m streamlit run app.py
    ```

## 💡 Key Insights (Analyst Summary)
1.  **The "iPhone Moment":** GLP-1 represents a shift from "treating sick people" (Oncology) to "subscribing healthy people" (Lifestyle).
2.  **Duopoly Power:** The market is dominated by **Novo Nordisk** and **Eli Lilly**. Others are years behind.
3.  **Pan-Organ Potential:** Data shows GLP-1 expanding into Heart Failure, Kidney Disease, and Liver (NASH), tripling the Total Addressable Market (TAM).

---
*Developed by Andrei Volokhovskii*
