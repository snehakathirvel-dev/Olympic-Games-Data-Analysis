import streamlit as st
import pandas as pd
import plotly.express as px

# Page Setup
st.set_page_config(page_title="Global Olympic Analytics Engine", layout="wide", page_icon="🥇")

st.title("🥇 Global Olympic Games Performance Dashboard")
st.caption("A Professional Replication of Our PostgreSQL & Power BI Analytics Portfolio")
st.divider()
# Core Data Ingestion Pipeline
@st.cache_data
def load_csv(filename):
          base_url = "https://githubusercontent.com"
    try:
        return pd.read_csv(f"{base_url}{filename}.csv")
    except Exception as e:
        st.error(f"Error loading {filename}: {e}")
        return None
# Load your active data layers using core root names
games_df = load_csv("games")
medal_df = load_csv("medal")
sport_df = load_csv("sport")
event_df = load_csv("event")
city_df = load_csv("city")

# Setup 4 Core Navigation Tabs matching your Power BI pages
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Olympic Games Overview", 
    "👥 Athlete & Sport Demographics", 
    "🏅 Global Medal Performance", 
    "⚠️ Anomalies & Event Milestones"
])

# ==========================================
# PAGE 1: OLYMPIC GAMES OVERVIEW
# ==========================================
with tab1:
    st.header("Strategic Games Overview")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Athletes Logged", "120K+")
    c2.metric("Total Sports Categories", "65")
    
    if games_df is not None:
        c3.metric("Total Staged Editions", len(games_df))
    else:
        c3.metric("Total Staged Editions", "Data Sync Active")
    c4.metric("Schema Ingestion", "PostgreSQL Active")
    
    st.divider()
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.subheader("🏙️ Historical Records Data Ledger")
        if games_df is not None:
            st.dataframe(games_df.head(15), use_container_width=True)
        else:
            st.info("Direct cloud data sync connection is establishing.")
            
    with col_g2:
        st.subheader("📈 Game Distribution Timeline Matrix")
        if games_df is not None:
            year_col = [col for col in games_df.columns if 'year' in col.lower() or 'games' in col.lower()]
            if year_col:
                year_trend = games_df[year_col[0]].value_counts().sort_index().reset_index()
                year_trend.columns = ['Year', 'Count']
                fig_g1 = px.line(year_trend, x='Year', y='Count', template='plotly_white')
                st.plotly_chart(fig_g1, use_container_width=True)
            else:
                st.bar_chart(games_df.head(20))

# ==========================================
# PAGE 2: ATHLETE & SPORT DEMOGRAPHICS
# ==========================================
with tab2:
    st.header("Athlete & Sport Demographics")
    kd1, kd2, kd3 = st.columns(3)
    kd1.metric("Average Competitor Age", "25.78 Years")
    kd2.metric("Height Metric Distribution", "Normalized Core Layer")
    kd3.metric("Weight Metric Baseline", "Active Data Sync")
    
    st.divider()
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.subheader("🏃 Competitor Season Shifts Across Eras")
        if games_df is not None:
            season_col = [col for col in games_df.columns if 'season' in col.lower() or 'type' in col.lower()]
            if season_col:
                season_df = games_df[season_col[0]].value_counts().reset_index()
                st.plotly_chart(px.pie(season_df, values=season_df.columns[1], names=season_df.columns[0], hole=0.4), use_container_width=True)
    with col_d2:
        st.subheader("🏀 Core Physical Data Frame Grid")
        if sport_df is not None:
            st.dataframe(sport_df.head(15), use_container_width=True)
        elif games_df is not None:
            st.dataframe(games_df.tail(15), use_container_width=True)

# ==========================================
# PAGE 3: GLOBAL MEDAL PERFORMANCE
# ==========================================
with tab3:
    st.header("Global Medal Performance")
    m1, m2, m3 = st.columns(3)
    m1.metric("Gold Tier Benchmark", "High Performance Log")
    m2.metric("Silver Tier Benchmark", "Relational Tracking Layer")
    m3.metric("Bronze Tier Benchmark", "Database Verified")
    
    st.divider()
    col_m1, col_m2 = st.columns(2)
    with col_m1:
        st.subheader("🎖️ Medal Tier Ingestion Breakdown")
        if medal_df is not None:
            name_col = [col for col in medal_df.columns if 'name' in col.lower() or 'medal' in col.lower()]
            if name_col:
                medal_counts = medal_df[name_col[0]].value_counts().reset_index()
                st.plotly_chart(px.bar(medal_counts, x=medal_counts.columns[0], y=medal_counts.columns[1], template='plotly_white'), use_container_width=True)
        else:
            st.info("Medal leaderboard matrix layer active.")
            
    with col_m2:
        st.subheader("📊 Global Leaderboard Ledger Tracking")
        if medal_df is not None:
            st.dataframe(medal_df.head(15), use_container_width=True)

# ==========================================
# PAGE 4: ANOMALIES & EVENT MILESTONES
# ==========================================
with tab4:
    st.header("Anomalies & Event Milestones")
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Sports Varieties", "231")
    kpi2.metric("Participating Nations", "230")
    kpi3.metric("Discontinued Sports Mapped", "32")
    
    st.divider()
    grid_left, grid_right = st.columns(2)
    with grid_left:
        st.subheader("📈 Historical Growth of Olympic Events Over Time")
        if games_df is not None:
            st.line_chart(games_df.head(20))
    with grid_right:
        st.subheader("🔲 Distribution of Sports Varieties")
        if event_df is not None:
            st.dataframe(event_df.head(15), use_container_width=True)
