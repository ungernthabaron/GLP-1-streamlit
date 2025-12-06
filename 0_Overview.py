import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="GLP-1 Phenomenon Analysis", 
    page_icon="🧬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PREMIUM CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Inter:wght@300;400;500;600;700&display=swap');
    
    :root {
        --primary: #FF3B3B;
        --secondary: #FF8E53;
        --bg: #050505;
        --card-bg: rgba(255, 255, 255, 0.03);
        --text: #E0E0E0;
    }

    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        max-width: 100% !important;
    }
    
    .stApp {
        background: linear-gradient(180deg, #0a0a0a 0%, #1a1a1a 100%);
    }
    
    /* Sticky Header */
    [data-testid="stHeader"] {
        background: rgba(10, 10, 10, 0.95);
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f0f 0%, #1a1a1a 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Card Component */
    .chart-card {
        background: var(--card-bg);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .chart-card:hover {
        border-color: rgba(255, 59, 59, 0.3);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    .card-title {
        font-family: 'Playfair Display', serif;
        font-size: 1.5rem;
        color: #FFF;
        margin-bottom: 0.5rem;
    }
    
    .card-subtitle {
        color: #888;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    /* Metrics */
    .metric-card {
        background: linear-gradient(135deg, rgba(255,59,59,0.1), rgba(255,255,255,0.03));
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.2rem;
        border-radius: 12px;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: var(--primary);
        font-family: 'Playfair Display', serif;
    }
    
    .metric-label {
        color: #AAA;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.5rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255,255,255,0.02);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 24px;
        background-color: transparent;
        border-radius: 8px;
        color: #888;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        color: #FFF;
    }
    
    /* Highlight */
    .highlight {
        color: var(--primary);
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# --- DATA LOADING ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/processed_studies.csv")
        df["StartDate"] = pd.to_datetime(df["StartDate"], errors="coerce")
        df["StartYear"] = df["StartDate"].dt.year
        return df
    except FileNotFoundError:
        return None

df = load_data()
if df is None:
    st.error("⚠️ Data not found")
    st.stop()

# Segmentation
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

min_year = int(df["StartYear"].min()) if not df["StartYear"].isnull().all() else 2010
real_max_year = int(df["StartYear"].max()) if not df["StartYear"].isnull().all() else 2025
max_year = min(real_max_year, 2025)

# --- SIDEBAR FILTERS ---
with st.sidebar:
    st.markdown("### 🔬 GLP-1 Analysis")
    st.markdown("---")
    
    st.markdown("#### Filters")
    
    # Year Range
    year_filter = st.slider(
        "Year Range",
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )
    
    # Segment Filter
    all_segments = df["Segment"].unique().tolist()
    segment_filter = st.multiselect(
        "Segments",
        options=all_segments,
        default=all_segments
    )
    
    # Phase Filter
    all_phases = ["Phase 1", "Phase 2", "Phase 3", "Phase 4"]
    phase_filter = st.multiselect(
        "Clinical Phases",
        options=all_phases,
        default=all_phases
    )
    
    st.markdown("---")
    st.markdown("#### Quick Stats")
    
    filtered_df = df[
        (df["StartYear"] >= year_filter[0]) &
        (df["StartYear"] <= year_filter[1]) &
        (df["Segment"].isin(segment_filter))
    ]
    
    st.metric("Total Studies", f"{len(filtered_df):,}")
    st.metric("GLP-1 Studies", f"{len(filtered_df[filtered_df['Segment']=='GLP-1 & Incretins']):,}")
    
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; font-size: 0.8rem; color: #666;">
            <b>Andrei Volokhovskii</b><br>
            <a href="https://www.linkedin.com/in/andrei-volokhovskii-a094b9260/" 
               target="_blank" style="color: #FF3B3B; text-decoration: none;">
                LinkedIn →
            </a>
        </div>
    """, unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def create_chart_card(title, subtitle=""):
    return f"""
    <div class="card-title">{title}</div>
    <div class="card-subtitle">{subtitle}</div>
    """

def clean_chart(fig):
    fig.update_layout(
        font=dict(family="Inter", color="#E0E0E0"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=40, b=20),
    )
    return st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# --- MAIN CONTENT ---
st.markdown(f"""
<div style="text-align: left; margin-bottom: 2rem;">
    <h1 style="font-size: 3.5rem; font-family: 'Playfair Display', serif; 
                background: linear-gradient(90deg, #FF3B3B, #FF8E53); 
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        The GLP-1 Revolution
    </h1>
    <p style="font-size: 1.2rem; color: #888;">
        A forensic analysis of pharmaceutical disruption ({min_year}–{max_year})
    </p>
</div>
""", unsafe_allow_html=True)

# Key Metrics Bar
glp1_df = filtered_df[filtered_df["Segment"] == "GLP-1 & Incretins"]
peak_yr = glp1_df["StartYear"].value_counts().idxmax() if len(glp1_df) > 0 else max_year
trials_peak = len(glp1_df[glp1_df["StartYear"] == peak_yr])

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(glp1_df):,}</div>
            <div class="metric-label">Total GLP-1 Trials</div>
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{int(peak_yr)}</div>
            <div class="metric-label">Peak Year</div>
        </div>
    """, unsafe_allow_html=True)
with col3:
    share = len(glp1_df) / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{share:.1f}%</div>
            <div class="metric-label">Market Share</div>
        </div>
    """, unsafe_allow_html=True)
with col4:
    p3_count = len(glp1_df[glp1_df["Phase"] == "Phase 3"])
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{p3_count}</div>
            <div class="metric-label">Phase 3 Trials</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- TAB NAVIGATION ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Overview", 
    "🌱 Act I: The Context", 
    "🚀 Act II: The Disruption", 
    "👑 Act III: Dominance",
    "🔍 Deep Insights"
])

with tab1:
    st.markdown("""
    <div class="chart-card">
        <h3>Executive Summary</h3>
        <p style="font-size: 1.1rem; line-height: 1.8; color: #CCC;">
            GLP-1 receptor agonists have undergone a transformation from a niche diabetes 
            treatment to a <span class="highlight">lifestyle drug class</span>, driving unprecedented 
            growth in clinical trials that defies historical pharmaceutical trends.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Timeline Trend
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown(create_chart_card(
        "Clinical Trial Volume Over Time",
        "Year-over-year trend by segment"
    ), unsafe_allow_html=True)
    
    yearly_trend = filtered_df.groupby(["StartYear", "Segment"]).size().reset_index(name="Count")
    fig = px.line(
        yearly_trend,
        x="StartYear",
        y="Count",
        color="Segment",
        color_discrete_map={
            "GLP-1 & Incretins": "#FF3B3B",
            "Legacy Metabolic": "#2E86C1",
            "Oncology (The Giant)": "#555",
            "All Other Therapy Areas": "#333"
        }
    )
    fig.update_layout(template="plotly_dark", xaxis_title="Year", yaxis_title="Number of Trials", height=400)
    clean_chart(fig)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # NEW: YoY Growth Rate Comparison
    col_comp1, col_comp2 = st.columns(2)
    
    with col_comp1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown(create_chart_card(
            "Year-over-Year Growth Rate",
            "Percentage change vs previous year"
        ), unsafe_allow_html=True)
        
        # Calculate YoY for each segment
        yoy_data = []
        for segment in ["GLP-1 & Incretins", "Legacy Metabolic", "Oncology (The Giant)"]:
            seg_df = filtered_df[filtered_df["Segment"] == segment]
            yearly = seg_df.groupby("StartYear").size().reset_index(name="Count")
            yearly = yearly.sort_values("StartYear")
            yearly["YoY_Change"] = yearly["Count"].pct_change() * 100
            yearly["Segment"] = segment
            yoy_data.append(yearly)
        
        yoy_combined = pd.concat(yoy_data)
        yoy_combined = yoy_combined[yoy_combined["StartYear"] >= 2015]  # Focus on recent years
        
        fig = px.bar(
            yoy_combined,
            x="StartYear",
            y="YoY_Change",
            color="Segment",
            barmode="group",
            color_discrete_map={
                "GLP-1 & Incretins": "#FF3B3B",
                "Legacy Metabolic": "#7C8B9E",
                "Oncology (The Giant)": "#555"
            }
        )
        fig.add_hline(y=0, line_dash="dash", line_color="#666", line_width=1)
        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Year",
            yaxis_title="Growth Rate (%)",
            height=350
        )
        clean_chart(fig)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_comp2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown(create_chart_card(
            "Market Share Evolution",
            "Percentage of total trials by segment"
        ), unsafe_allow_html=True)
        
        # Calculate market share over time
        yearly_total = filtered_df.groupby("StartYear").size().reset_index(name="Total")
        yearly_segment = filtered_df.groupby(["StartYear", "Segment"]).size().reset_index(name="Count")
        share_df = yearly_segment.merge(yearly_total, on="StartYear")
        share_df["Share"] = (share_df["Count"] / share_df["Total"]) * 100
        
        # Focus on key segments
        share_df = share_df[share_df["Segment"].isin(["GLP-1 & Incretins", "Legacy Metabolic", "Oncology (The Giant)"])]
        
        fig = px.area(
            share_df,
            x="StartYear",
            y="Share",
            color="Segment",
            color_discrete_map={
                "GLP-1 & Incretins": "#FF3B3B",
                "Legacy Metabolic": "#7C8B9E",
                "Oncology (The Giant)": "#555"
            }
        )
        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Year",
            yaxis_title="Market Share (%)",
            height=350,
            hovermode="x unified"
        )
        clean_chart(fig)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # NEW: Heatmap
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown(create_chart_card(
        "Activity Heatmap: Segment × Year",
        "Color intensity shows trial volume"
    ), unsafe_allow_html=True)
    
    heatmap_data = filtered_df.groupby(["StartYear", "Segment"]).size().reset_index(name="Count")
    heatmap_pivot = heatmap_data.pivot(index="Segment", columns="StartYear", values="Count").fillna(0)
    
    fig = px.imshow(
        heatmap_pivot,
        labels=dict(x="Year", y="Segment", color="Trials"),
        aspect="auto",
        color_continuous_scale="Reds"
    )
    fig.update_layout(
        template="plotly_dark",
        height=350
    )
    clean_chart(fig)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # NEW: Indexed Growth Comparison
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown(create_chart_card(
        "Indexed Growth Comparison (2015 = 100)",
        "Compare relative growth trajectories"
    ), unsafe_allow_html=True)
    
    indexed_data = []
    base_year = 2015
    for segment in ["GLP-1 & Incretins", "Legacy Metabolic", "Oncology (The Giant)"]:
        seg_df = filtered_df[filtered_df["Segment"] == segment]
        yearly = seg_df.groupby("StartYear").size().reset_index(name="Count")
        yearly = yearly[yearly["StartYear"] >= base_year].sort_values("StartYear")
        
        if len(yearly) > 0 and yearly.iloc[0]["Count"] > 0:
            base_count = yearly.iloc[0]["Count"]
            yearly["Indexed"] = (yearly["Count"] / base_count) * 100
            yearly["Segment"] = segment
            indexed_data.append(yearly)
    
    if indexed_data:
        indexed_combined = pd.concat(indexed_data)
        
        fig = px.line(
            indexed_combined,
            x="StartYear",
            y="Indexed",
            color="Segment",
            markers=True,
            color_discrete_map={
                "GLP-1 & Incretins": "#FF3B3B",
                "Legacy Metabolic": "#7C8B9E",
                "Oncology (The Giant)": "#555"
            }
        )
        fig.add_hline(y=100, line_dash="dash", line_color="#FFD700", line_width=2, annotation_text="Baseline (2015)")
        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Year",
            yaxis_title="Indexed Value (2015 = 100)",
            height=400,
            hovermode="x unified"
        )
        clean_chart(fig)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""
    ### The Sleeping Giant (2010–2018)
    
    Prior to 2018, the pharmaceutical landscape was dominated by **oncology**. 
    GLP-1s existed (Liraglutide) but were buried under the massive volume of cancer research.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown(create_chart_card("Research Volume by Category (2010-2018)"), unsafe_allow_html=True)
    
    df_act1 = filtered_df[(filtered_df["StartYear"] >= 2010) & (filtered_df["StartYear"] <= 2018)]
    act1_counts = df_act1["Segment"].value_counts().reset_index()
    act1_counts.columns = ["Segment", "Count"]
    
    fig = px.treemap(
        act1_counts,
        path=['Segment'],
        values='Count',
        color='Segment',
        color_discrete_map={
            "Oncology (The Giant)": "#2A2A2A",
            "Legacy Metabolic": "#404040",
            "All Other Therapy Areas": "#1A1A1A",
            "GLP-1 & Incretins": "#FF3B3B"
        }
    )
    fig.update_layout(template="plotly_dark", height=500)
    clean_chart(fig)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # NEW: Act I - Pie Chart Comparison
    col_act1_a, col_act1_b = st.columns(2)
    
    with col_act1_a:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown(create_chart_card("Segment Distribution", "Pie chart view of 2010-2018"), unsafe_allow_html=True)
        
        fig = px.pie(
            act1_counts,
            values='Count',
            names='Segment',
            color='Segment',
            color_discrete_map={
                "Oncology (The Giant)": "#555",
                "Legacy Metabolic": "#7C8B9E",
                "All Other Therapy Areas": "#333",
                "GLP-1 & Incretins": "#FF3B3B"
            },
            hole=0.4
        )
        fig.update_layout(template="plotly_dark", height=350)
        clean_chart(fig)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_act1_b:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown(create_chart_card("Yearly Breakdown", "Trial count by year (2010-2018)"), unsafe_allow_html=True)
        
        yearly_act1 = df_act1.groupby(["StartYear", "Segment"]).size().reset_index(name="Count")
        
        fig = px.bar(
            yearly_act1,
            x="StartYear",
            y="Count",
            color="Segment",
            color_discrete_map={
                "Oncology (The Giant)": "#555",
                "Legacy Metabolic": "#7C8B9E",
                "All Other Therapy Areas": "#333",
                "GLP-1 & Incretins": "#FF3B3B"
            }
        )
        fig.update_layout(template="plotly_dark", height=350, barmode="stack")
        clean_chart(fig)
        st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""
    ### The Vertical Takeoff (2018–2024)
    
    **December 2017**: FDA approves semaglutide (Ozempic) for Type 2 Diabetes.  
    **June 2021**: FDA approves Wegovy for obesity. The floodgates open.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown(create_chart_card("GLP-1 Growth Trajectory", "Notice the exponential curve post-2021"), unsafe_allow_html=True)
    
    glp1_yearly = glp1_df.groupby("StartYear").size().reset_index(name="Count")
    glp1_yearly = glp1_yearly[(glp1_yearly["StartYear"] >= 2015) & (glp1_yearly["StartYear"] <= max_year)]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=glp1_yearly["StartYear"],
        y=glp1_yearly["Count"],
        mode='lines+markers',
        line=dict(width=4, color='#FF3B3B'),
        fill='tozeroy',
        fillcolor='rgba(255, 59, 59, 0.2)',
        marker=dict(size=10)
    ))
    
    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Year",
        yaxis_title="New Trials Started",
        height=450
    )
    clean_chart(fig)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # NEW: Act II - Comparison with Other Segments
    col_act2_a, col_act2_b = st.columns(2)
    
    with col_act2_a:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown(create_chart_card("GLP-1 vs Competition", "Side-by-side comparison 2018-2024"), unsafe_allow_html=True)
        
        df_act2 = filtered_df[(filtered_df["StartYear"] >= 2018) & (filtered_df["StartYear"] <= 2024)]
        act2_comparison = df_act2.groupby(["StartYear", "Segment"]).size().reset_index(name="Count")
        
        fig = px.line(
            act2_comparison,
            x="StartYear",
            y="Count",
            color="Segment",
            markers=True,
            color_discrete_map={
                "GLP-1 & Incretins": "#FF3B3B",
                "Legacy Metabolic": "#7C8B9E",
                "Oncology (The Giant)": "#555",
                "All Other Therapy Areas": "#333"
            }
        )
        fig.update_layout(template="plotly_dark", height=350)
        clean_chart(fig)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_act2_b:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown(create_chart_card("Cumulative Growth", "Total trials accumulated over time"), unsafe_allow_html=True)
        
        glp1_cumulative = glp1_yearly.copy()
        glp1_cumulative["Cumulative"] = glp1_cumulative["Count"].cumsum()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=glp1_cumulative["StartYear"],
            y=glp1_cumulative["Cumulative"],
            fill='tozeroy',
            fillcolor='rgba(255, 59, 59, 0.3)',
            line=dict(color='#FF3B3B', width=3)
        ))
        fig.update_layout(
            template="plotly_dark",
            xaxis_title="Year",
            yaxis_title="Cumulative Trials",
            height=350
        )
        clean_chart(fig)
        st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown("""
    ### Total Category Dominance
    
    When you isolate **Metabolic diseases** (Diabetes, Obesity), GLP-1 isn't just competing—it's replacing.
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown(create_chart_card("Phase Distribution", "GLP-1 vs Legacy Metabolic (2020+)"), unsafe_allow_html=True)
        
        metabolic_df = filtered_df[(filtered_df["Segment"].isin(["GLP-1 & Incretins", "Legacy Metabolic"])) & (filtered_df["StartYear"] >= 2020)]
        phase_counts = metabolic_df.groupby(["Phase", "Segment"]).size().reset_index(name="Count")
        phase_counts = phase_counts[phase_counts["Phase"].isin(phase_filter)]
        
        fig = px.bar(
            phase_counts,
            x="Phase",
            y="Count",
            color="Segment",
            barmode="group",
            color_discrete_map={
                "Legacy Metabolic": "#7C8B9E",
                "GLP-1 & Incretins": "#FF3B3B"
            },
            text_auto=True
        )
        fig.update_traces(textfont_size=12, textposition="outside")
        fig.update_layout(
            template="plotly_dark", 
            height=400,
            yaxis_title="Number of Trials",
            xaxis_title="Clinical Phase"
        )
        clean_chart(fig)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_b:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown(create_chart_card("Phase 3 Success Rate", "Percentage of trials reaching late-stage"), unsafe_allow_html=True)
        
        success_rate = (len(metabolic_df[metabolic_df["Phase"]=="Phase 3"]) / len(metabolic_df)) * 100 if len(metabolic_df) > 0 else 0
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=success_rate,
            number={'suffix': "%", 'font': {'size': 48, 'color': '#FFF'}},
            gauge={
                'axis': {'range': [0, 30], 'tickwidth': 1, 'tickcolor': "#666"},
                'bar': {'color': "#FF3B3B", 'thickness': 0.8},
                'bgcolor': "rgba(0,0,0,0.3)",
                'borderwidth': 2,
                'bordercolor': "#333",
                'steps': [
                    {'range': [0, 10], 'color': '#1a1a1a'},
                    {'range': [10, 20], 'color': '#2a2a2a'},
                    {'range': [20, 30], 'color': '#3a3a3a'}
                ],
                'threshold': {
                    'line': {'color': "#FFD700", 'width': 4},
                    'thickness': 0.75,
                    'value': 20
                }
            }
        ))
        fig.update_layout(
            height=400,
            font={'color': "#E0E0E0", 'family': "Inter"}
        )
        clean_chart(fig)
        st.markdown('</div>', unsafe_allow_html=True)

with tab5:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.markdown(create_chart_card("Expansion Map", "Mechanism × Condition Matrix"), unsafe_allow_html=True)
    
    bubble_df = glp1_df.groupby(["Mechanism", "Conditions"]).size().reset_index(name="Count")
    bubble_df = bubble_df.sort_values("Count", ascending=False).head(30)
    
    fig = px.scatter(
        bubble_df,
        x="Mechanism",
        y="Conditions",
        size="Count",
        color="Count",
        color_continuous_scale="Reds",
        hover_data=["Count"]
    )
    fig.update_layout(template="plotly_dark", height=600)
    clean_chart(fig)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # NEW: Deep Insights - Additional Analysis
    col_ins_a, col_ins_b = st.columns(2)
    
    with col_ins_a:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown(create_chart_card("Top Conditions", "Most studied conditions for GLP-1"), unsafe_allow_html=True)
        
        top_conditions = glp1_df["Conditions"].value_counts().head(10).reset_index()
        top_conditions.columns = ["Condition", "Count"]
        
        fig = px.bar(
            top_conditions,
            y="Condition",
            x="Count",
            orientation='h',
            color="Count",
            color_continuous_scale="Reds"
        )
        fig.update_layout(
            template="plotly_dark",
            height=400,
            yaxis={'categoryorder':'total ascending'}
        )
        clean_chart(fig)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_ins_b:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown(create_chart_card("Mechanism Breakdown", "Distribution of drug mechanisms"), unsafe_allow_html=True)
        
        mechanisms = glp1_df["Mechanism"].value_counts().head(8).reset_index()
        mechanisms.columns = ["Mechanism", "Count"]
        
        fig = px.pie(
            mechanisms,
            values="Count",
            names="Mechanism",
            color_discrete_sequence=px.colors.sequential.Reds_r
        )
        fig.update_layout(template="plotly_dark", height=400)
        clean_chart(fig)
        st.markdown('</div>', unsafe_allow_html=True)
