import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set up global layout configurations
st.set_page_config(page_title="Global Olympic Games Analytics", layout="wide")

st.title("🥇 Global Olympic Games Performance Dashboard")
st.caption("A Professional Replication of Our PostgreSQL & Power BI Analytics Portfolio")
st.divider()

# Core Data Ingestion Pipeline - Reads directly from the local folder
@st.cache_data
def load_csv(filename):
    # Search for the file in the local CSV directory
    file_path = os.path.join("CSV", f"{filename}.csv")
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        st.error(f"Error loading {filename}.csv: {e}")
        return None

# Load active data layers
city_df = load_csv("city")
competitor_event_df = load_csv("competitor_event")
consolidated_fact_df = load_csv("consolidated_fact")
event_df = load_csv("event")
games_city_df = load_csv("games_city")
games_competitor_df = load_csv("games_competitor")
games_df = load_csv("games")
medal_df = load_csv("medal")
noc_region_df = load_csv("noc_region")
person_region_df = load_csv("person_region")
person_df = load_csv("person")
sport_df = load_csv("sport")

# Build Dashboard Layout Tabs
tab1, tab2, tab3 = st.tabs(["Overview Metrics", "Athlete & Sport Demographics", "Performance Deep Dive"])

with tab1:
    st.subheader("Core System Health & Overview")
    grid_left, grid_right = st.columns(2)
    
    with grid_left:
        if consolidated_fact_df is not None:
            st.metric(label="Total Logged Records", value=f"{len(consolidated_fact_df):,}")
        else:
            st.metric(label="Total Logged Records", value="Unavailable")
            
    with grid_right:
        if games_df is not None:
            st.metric(label="Total Olympic Games Events", value=f"{len(games_df)}")
        else:
            st.metric(label="Total Olympic Games Events", value="Unavailable")

with tab2:
    st.subheader("Athlete Distribution & Characteristics")
    if person_df is not None:
        st.markdown("**Overview of Registered Competitors Summary Data**")
        st.dataframe(person_df.head(100), use_container_width=True)
    else:
        st.warning("Demographic records are currently loading or unavailable.")

with tab3:
    st.subheader("Historical Medal Performance Analytics")
    if medal_df is not None:
        st.markdown("**Historical Medal Inventory Overview**")
        st.dataframe(medal_df.head(100), use_container_width=True)
    else:
        st.warning("Performance records are currently loading or unavailable.")
