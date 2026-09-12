import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set up global widescreen configurations
st.set_page_config(page_title="Global Olympic Analytics Portfolio", layout="wide", initial_sidebar_state="expanded")

st.title("🥇 Global Olympic Games Performance Dashboard")
st.caption("A Professional Enterprise Replication of Our PostgreSQL & Power BI Analytics Architecture")
st.divider()

# 1. Central Data Ingestion Engine (Loads ALL 12 Active CSV Layers)
@st.cache_data
def load_olympic_system():
    files = [
        "city", "competitor_event", "consolidated_fact", "event", 
        "games_city", "games_competitor", "games", "medal", 
        "noc_region", "person_region", "person", "sport"
    ]
    data_layers = {}
    
    for file in files:
        file_path = os.path.join("CSV", f"{file}.csv")
        if os.path.exists(file_path):
            try:
                data_layers[file] = pd.read_csv(file_path)
            except Exception as e:
                data_layers[file] = None
        else:
            data_layers[file] = None
    return data_layers

db = load_olympic_system()

# 2. Sidebar Navigation and Multi-File Status Tracker
st.sidebar.title("🗄️ Database Management")
st.sidebar.markdown("### System File Connection Monitor")

for name, df in db.items():
    if df is not None:
        st.sidebar.success(f"Connected: `{name}.csv` ({len(df):,} rows)")
    else:
        st.sidebar.error(f"Missing: `{name}.csv` layer")

# 3. Main Dashboard Layout - Replicating Your 4 Key Power BI Focus Areas
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Executive KPI Overview", 
    "🏃 Athlete & Sport Demographics", 
    "🏅 Historical Medal Analytics", 
    "📂 Raw Relational Schema Explorer"
])

# --- TAB 1: EXECUTIVE KPI OVERVIEW ---
with tab1:
    st.subheader("High-Level Executive Metrics")
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        total_records = len(db["consolidated_fact"]) if db["consolidated_fact"] is not None else 0
        st.metric("Total Consolidated Records", f"{total_records:,}")
    with m2:
        total_athletes = len(db["person"]) if db["person"] is not None else 0
        st.metric("Registered Competitors", f"{total_athletes:,}")
    with m3:
        total_games = len(db["games"]) if db["games"] is not None else 0
        st.metric("Historical Olympic Games", f"{total_games:,}")
    with m4:
        total_sports = len(db["sport"]) if db["sport"] is not None else 0
        st.metric("Tracked Sporting Categories", f"{total_sports:,}")

    st.divider()
    
    st.markdown("### 📊 Database Storage Profile")
    row_counts = []
    for name, df in db.items():
        if df is not None:
            row_counts.append({"Table Name": f"{name}.csv", "Total Rows": len(df)})
    
    if row_counts:
        counts_df = pd.DataFrame(row_counts)
        fig_base = px.bar(
            counts_df, 
            x="Table Name", 
            y="Total Rows", 
            title="Data Volume Distribution across Your 12 Relational Tables",
            text_auto='.2s',
            color="Table Name"
        )
        st.plotly_chart(fig_base, use_container_width=True)

# --- TAB 2: ATHLETE & SPORT DEMOGRAPHICS ---
with tab2:
    st.subheader("Athlete & Sport Analysis Visualizations")
    col1, col2 = st.columns(2)
    
    with col1:
        if db["person"] is not None and 'gender' in db["person"].columns:
            st.markdown("### Gender Distribution")
            gender_counts = db["person"]['gender'].value_counts().reset_index()
            gender_counts.columns = ['Gender', 'Count']
            fig_gen = px.pie(gender_counts, values='Count', names='Gender', title="Athlete Breakdown by Gender", color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_gen, use_container_width=True)
        else:
            st.info("Athlete data layers or gender configurations are loading.")
            
    with col2:
        if db["games_competitor"] is not None and 'age' in db["games_competitor"].columns:
            st.markdown("### Athlete Age Distribution Profile")
            # Clear null values to ensure proper graph plotting bounds
            age_data = db["games_competitor"]['age'].dropna()
            fig_age = px.histogram(age_data, x='age', title="Distribution Count of Athlete Ages", nbins=30, color_discrete_sequence=['#636EFA'])
            st.plotly_chart(fig_age, use_container_width=True)
        else:
            st.info("Competitor performance history layers are loading.")

# --- TAB 3: HISTORICAL MEDAL ANALYTICS ---
with tab3:
    st.subheader("Performance & Medal Distributions Visualizations")
    col3, col4 = st.columns(2)
    
    with col3:
        if db["games"] is not None and 'season' in db["games"].columns:
            st.markdown("### Olympic Games Season Classifications")
            season_counts = db["games"]['season'].value_counts().reset_index()
            season_counts.columns = ['Season', 'Count']
            fig_sea = px.pie(season_counts, values='Count', names='Season', title="Ratio of Summer vs. Winter Games hosted")
            st.plotly_chart(fig_sea, use_container_width=True)
        else:
            st.info("Historical games records are loading.")
            
    with col4:
        if db["medal"] is not None and 'medal_name' in db["medal"].columns:
            st.markdown("### Master Medal Classifications")
            medal_counts = db["medal"]['medal_name'].value_counts().reset_index()
            medal_counts.columns = ['Medal Type', 'Count']
            fig_med = px.bar(medal_counts, x='Medal Type', y='Count', title="Available Unique Medal Rankings Categories", color='Medal Type')
            st.plotly_chart(fig_med, use_container_width=True)
        else:
            st.info("Medal lookup system layers are loading.")

# --- TAB 4: RAW RELATIONAL SCHEMA EXPLORER ---
with tab4:
    st.subheader("Relational Database Schema Table Inspections")
    selected_layer = st.selectbox("Choose Table Layer to View:", list(db.keys()), key="final_explorer")
    
    if db[selected_layer] is not None:
        st.write(f"Showing sample records for **{selected_layer}.csv**:")
        st.write(f"**Shape:** {db[selected_layer].shape:,} rows, {db[selected_layer].shape} columns")
        st.dataframe(db[selected_layer].head(100), use_container_width=True)
    else:
        st.error(f"The selected table layer '{selected_layer}' is empty or failed to load.")
