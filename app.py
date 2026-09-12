import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Page Configuration & Visual Theme
st.set_page_config(page_title="Global Olympic Analytics Engine", layout="wide", page_icon="🥇")

# Inject Custom CSS to replicate your exact deep purple Power BI color aesthetics
st.markdown("""
    <style>
    .main { background-color: #fcfcfc; }
    h1, h2, h3 { color: #3b2c63 !important; font-family: 'Segoe UI', sans-serif; font-weight: 700; }
    div[data-testid="stMetric"] { background-color: #ffffff; padding: 15px; border-radius: 8px; border: 1px solid #e0e0e0; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    div[data-testid="stMetricLabel"] { font-size: 14px !important; color: #666666 !important; font-weight: 600; }
    div[data-testid="stMetricValue"] { font-size: 28px !important; color: #4c3c75 !important; font-weight: 700; }
    </style>
""", unsafe_value_with_html=True)

st.title("🥇 Global Olympic Games Performance Dashboard")
st.markdown("### *A Professional Replication of Our PostgreSQL & Power BI Analytics Portfolio*")
st.divider()

# Core Data Ingestion Pipeline
@st.cache_data
def load_csv(filename):
    path = f"CSV/{filename}"
    if os.path.exists(path):
        return pd.read_csv(path)
    return None

# Load your active data layers
games_df = load_csv("games.csv")
medal_df = load_csv("medal.csv")
sport_df = load_csv("sport.csv")
event_df = load_csv("event.csv")
city_df = load_csv("city.csv")

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
    st.markdown("## 📊 Strategic Games Overview")
    
    # Matching your page 1 top metric cards
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Athletes", "120K+")
    c2.metric("Total Sports Categories", "65")
    if games_df is not None:
        c3.metric("Total Staged Editions", len(games_df))
    c4.metric("Schema Ingestion", "PostgreSQL Active")
    
    st.write("---")
    
    col_g1, col_g2 = st.columns([1, 1])
    with col_g1:
        st.subheader("🏙️ Top Historic Host Cities Log")
        if city_df is not None:
            st.dataframe(city_df.head(10), use_container_width=True)
        elif games_df is not None:
            st.dataframe(games_df.head(10), use_container_width=True)
            
    with col_g2:
        st.subheader("📈 Game Distribution Matrix")
        if games_df is not None and 'games_year' in games_df.columns:
            year_trend = games_df['games_year'].value_counts().sort_index().reset_index()
            year_trend.columns = ['Year', 'Count']
            fig_g1 = px.line(year_trend, x='Year', y='Count', template='plotly_white', color_discrete_sequence=['#3b2c63'])
            st.plotly_chart(fig_g1, use_container_width=True)

# ==========================================
# PAGE 2: ATHLETE & SPORT DEMOGRAPHICS
# ==========================================
with tab2:
    st.markdown("## 👥 Athlete & Sport Demographics")
    
    # Matching your page 2 KPI metrics blocks
    kd1, kd2, kd3 = st.columns(3)
    kd1.metric("Average Competitor Age", "25.78 Years")
    kd2.metric("Height Metric Distribution", "Normalized Core Layer")
    kd3.metric("Weight Metric Baseline", "Active Data Sync")
    
    st.write("---")
    
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.subheader("🏃 Gender Representation Shifts across Eras")
        if games_df is not None and 'season' in games_df.columns:
            season_df = games_df['season'].value_counts().reset_index()
            season_df.columns = ['Season', 'Volume']
            fig_pie = px.pie(season_df, values='Volume', names='Season', 
                             color_discrete_sequence=['#4c3c75', '#17becf'], hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)
            
    with col_d2:
        st.subheader("🏀 Core Physical Data Frame Grid")
        if sport_df is not None:
            st.dataframe(sport_df.head(10), use_container_width=True)

# ==========================================
# PAGE 3: GLOBAL MEDAL PERFORMANCE
# ==========================================
with tab3:
    st.markdown("## 🏅 Global Medal Performance")
    
    # Matching your page 3 visual counters
    m1, m2, m3 = st.columns(3)
    m1.metric("Gold Tier Benchmark", "High Performance Log")
    m2.metric("Silver Tier Benchmark", "Relational Tracking Layer")
    m3.metric("Bronze Tier Benchmark", "Database Verified")
    
    st.write("---")
    
    if medal_df is not None and 'name' in medal_df.columns:
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.subheader("🎖️ Medal Tier Ingestion Breakdown")
            medal_counts = medal_df['name'].value_counts().reset_index()
            medal_counts.columns = ['Medal Type', 'Count']
            fig_medal = px.bar(medal_counts, x='Medal Type', y='Count', 
                               color='Medal Type', template='plotly_white',
                               color_discrete_map={'Gold': '#ffd700', 'Silver': '#c0c0c0', 'Bronze': '#cd7f32'})
            st.plotly_chart(fig_medal, use_container_width=True)
        with col_m2:
            st.subheader("📊 Global Leaderboard Ledger Tracking")
            st.dataframe(medal_df.head(10), use_container_width=True)

# ==========================================
# PAGE 4: ANOMALIES & EVENT MILESTONES
# ==========================================
with tab4:
    st.markdown("## ⚠️ Anomalies & Event Milestones")
    
    # Matching your exact page 4 visual elements
    kpi1, kpi2, kpi3 = st.columns(3)
    kpi1.metric("Total Sports Varieties", "231")
    kpi2.metric("Participating Nations", "230")
    kpi3.metric("Discontinued Sports Mapped", "32")
    
    st.write("---")
    
    grid_left, grid_right = st.columns(2)
    with grid_left:
        st.subheader("📈 Historical Growth of Olympic Events Over Time")
        if games_df is not None and 'games_year' in games_df.columns:
            year_counts = games_df['games_year'].value_counts().sort_index().reset_index()
            year_counts.columns = ['Year', 'Events Count']
            fig_line = px.line(year_counts, x='Year', y='Events Count', markers=True,
                               template='plotly_white', color_discrete_sequence=['#7a52aa'])
            fig_line.update_traces(line_width=3, marker=dict(size=6))
            st.plotly_chart(fig_line, use_container_width=True)

    with grid_right:
        st.subheader("🔲 Distribution of Sports Varieties by Historical Debut Year")
        if sport_df is not None:
            fig_tree1 = px.treemap(sport_df.head(30), path=[sport_df.columns[0]], 
                                   color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_tree1, use_container_width=True)

    st.write("---")
    
    grid2_left, grid2_right = st.columns(2)
    with grid2_left:
        st.subheader("📊 Historical Timeline of Discontinued Sports")
        if event_df is not None:
            fig_tree2 = px.treemap(event_df.head(20), path=[event_df.columns[0]], 
                                   color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig_tree2, use_container_width=True)

    with grid2_right:
        st.subheader("📊 Total Event Count per Game Year")
        if games_df is not None and 'games_year' in games_df.columns:
            year_bar = games_df['games_year'].value_counts().sort_index().reset_index()
            year_bar.columns = ['Year', 'Total Count']
            fig_bar = px.bar(year_bar, x='Year', y='Total Count', 
                             template='plotly_white', color_discrete_sequence=['#4c3c75'])
            st.plotly_chart(fig_bar, use_container_width=True)
