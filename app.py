import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set up clean, widescreen analytical dashboard configurations
st.set_page_config(page_title="Olympic Analytics Portfolio", layout="wide", initial_sidebar_state="expanded")

st.title("🥇 Global Olympic Games Performance Dashboard")
st.caption("A Professional Enterprise Replication of Our PostgreSQL & Power BI Analytics Architecture")
st.divider()

# 1. Central Data Ingestion Engine (Loads ALL 12 Active CSV Layers Local Files)
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

# Initialize entire database dictionary
db = load_olympic_system()

# 2. Sidebar Navigation and Multi-File Status Tracker
st.sidebar.title("🗄️ Database Management")
st.sidebar.markdown("### System File Connection Monitor")

# Track file availability explicitly in the sidebar UI
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
    st.markdown("### Quick Data Verification View")
    if db["consolidated_fact"] is not None:
        st.dataframe(db["consolidated_fact"].head(100), use_container_width=True)
    else:
        st.info("Upload your consolidated data to view transaction details.")

# --- TAB 2: ATHLETE & SPORT DEMOGRAPHICS ---
with tab2:
    st.subheader("Athlete & Sport Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Sample Profile: Competitor Records**")
        if db["person"] is not None:
            st.dataframe(db["person"].head(50), use_container_width=True)
        else:
            st.warning("Person layer unavailable.")
            
    with col2:
        st.markdown("**Sample Profile: Sports & Disciplines**")
        if db["sport"] is not None:
            st.dataframe(db["sport"].head(50), use_container_width=True)
        else:
            st.warning("Sport layer unavailable.")

# --- TAB 3: HISTORICAL MEDAL ANALYTICS ---
with tab3:
    st.subheader("Performance & Medal Distributions")
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("**Sample Profile: Awarded Medals Inventory**")
        if db["medal"] is not None:
            st.dataframe(db["medal"].head(50), use_container_width=True)
        else:
            st.warning("Medal layer unavailable.")
            
    with col4:
        st.markdown("**Sample Profile: Regional Mappings (NOC)**")
        if db["noc_region"] is not None:
            st.dataframe(db["noc_region"].head(50), use_container_width=True)
        else:
            st.warning("NOC Region layer unavailable.")

# --- TAB 4: RAW RELATIONAL SCHEMA EXPLORER ---
with tab4:
    st.subheader("Relational Database Schema Table Inspections")
    st.markdown("Select any active relational table below to inspect its data shape directly:")
    
    selected_layer = st.selectbox("Choose Table Layer:", list(db.keys()))
    
    if db[selected_layer] is not None:
        st.write(f"Showing sample records for **{selected_layer}.csv**:")
        st.write(f"**Shape:** {db[selected_layer].shape[0]} rows, {db[selected_layer].shape[1]} columns")
        st.dataframe(db[selected_layer], use_container_width=True)
    else:
        st.error(f"The selected table layer '{selected_layer}' is empty or failed to load.")
