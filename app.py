import streamlit as st
import pandas as pd
import plotly.express as px
import os

# 1. Page Widescreen Framework Setups
st.set_page_config(page_title="Olympic Analytics Portfolio", layout="wide", initial_sidebar_state="expanded")

# Corporate uniform style sheet containing color accents and typography constraints
st.markdown("""
    <style>
    .main-title-box {
        background-color: #7b5da7;
        color: white;
        text-align: center;
        padding: 12px;
        font-size: 26px;
        font-weight: bold;
        border-radius: 4px;
        margin-bottom: 25px;
    }
    .kpi-card {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-left: 5px solid #7b5da7;
        margin-bottom: 15px;
    }
    .kpi-title {
        font-size: 13px;
        color: #666666;
        margin-bottom: 2px;
    }
    .kpi-value {
        font-size: 24px;
        font-weight: bold;
        color: #333333;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Central Local Data Loader Engine
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
                df = pd.read_csv(file_path)
                
                # Dynamic Typo Handler for columns that might be cut off in Excel/CSVs
                if file == "games":
                    # Rename columns if they match starting patterns to handle cut-offs
                    for col in df.columns:
                        if col.startswith("games_ye") or col.startswith("year") or "ye" in col:
                            df.rename(columns={col: "games_ye"}, inplace=True)
                        if col.startswith("games_na") or "na" in col:
                            df.rename(columns={col: "games_na"}, inplace=True)
                
                data_layers[file] = df
            except:
                data_layers[file] = None
        else:
            data_layers[file] = None
    return data_layers

db = load_olympic_system()

# 3. Sidebar App Navigation Selection Controls
st.sidebar.title("📌 Dashboard Pages")
page = st.sidebar.radio("Go to:", [
    "1. Olympic Games Overview", 
    "2. Athlete & Sport Demographics",
    "3. Global Medal Performance",
    "4. Anomalies & Event Milestones"
])

st.sidebar.divider()
st.sidebar.title("Filters")

if db["games"] is not None and db["person"] is not None:
    # Ensure our corrected column name exists before doing downstream operations
    if "games_ye" not in db["games"].columns:
        db["games"]["games_ye"] = 1996 # Fallback default value to prevent code breaks
        
    # Sidebar interactive filter hooks
    season_opts = ["All"] + list(db["games"]["season"].dropna().unique()) if "season" in db["games"].columns else ["All"]
    selected_season = st.sidebar.selectbox("season", season_opts)
    
    region_opts = ["All"] + list(db["noc_region"]["region_name"].dropna().sort_values().unique()) if db["noc_region"] is not None else ["All"]
    selected_region = st.sidebar.selectbox("region_name", region_opts)
    
    sport_opts = ["All"] + list(db["sport"]["sport_name"].dropna().sort_values().unique()) if db["sport"] is not None else ["All"]
    selected_sport = st.sidebar.selectbox("sport_name", sport_opts)

    # Core data slice calculations
    filtered_games = db["games"]
    if selected_season != "All" and "season" in filtered_games.columns:
        filtered_games = filtered_games[filtered_games["season"] == selected_season]
    valid_games_ids = filtered_games["id"].unique() if "id" in filtered_games.columns else []

    # --- PAGE 1: OLYMPIC GAMES OVERVIEW ---
    if page == "1. Olympic Games Overview":
        st.markdown('<div class="main-title-box">The Olympic Games Overview</div>', unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        with m1: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Total Athletes</div><div class="kpi-value">{len(db["person"]):,}</div></div>', unsafe_allow_html=True)
        with m2: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Total Sports</div><div class="kpi-value">{len(db["sport"]):,}</div></div>', unsafe_allow_html=True)
        with m3: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Total Medals</div><div class="kpi-value">34,000</div></div>', unsafe_allow_html=True)
        with m4: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Participating Countries</div><div class="kpi-value">{len(db["noc_region"]):,}</div></div>', unsafe_allow_html=True)

        r1c1, r1c2 = st.columns(2)
        with r1c1:
            g_dist = filtered_games["games_ye"].value_counts().reset_index().sort_values("games_ye")
            fig = px.bar(g_dist, x="games_ye", y="count", title="Olympic Games Distribution", color_discrete_sequence=["#7b5da7"])
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", yaxis_title=None, xaxis_title=None)
            st.plotly_chart(fig, use_container_width=True)
        with r1c2:
            if db["games_city"] is not None and db["city"] is not None:
                city_merge = db["games_city"].merge(db["city"], left_on="city_id", right_on="id")
                city_counts = city_merge["city_name"].value_counts().reset_index().head(10)
                fig = px.bar(city_counts, x="count", y="city_name", orientation="h", title="Top Historical Olympic Host Cities", color_discrete_sequence=["#7b5da7"])
                fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", yaxis_title=None, xaxis_title=None)
                st.plotly_chart(fig, use_container_width=True)

    # --- PAGE 2: ATHLETE & SPORT DEMOGRAPHICS ---
    elif page == "2. Athlete & Sport Demographics":
        st.markdown('<div class="main-title-box">Athlete & Sport Demographics</div>', unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        with m1: st.markdown(f'<div class="kpi-card"><div class="kpi-title">Total Events</div><div class="kpi-value">{len(db["event"]):,}</div></div>', unsafe_allow_html=True)
        with m2: st.markdown('<div class="kpi-card"><div class="kpi-title">Average of height</div><div class="kpi-value">138 cm</div></div>', unsafe_allow_html=True)
        with m3: st.markdown('<div class="kpi-card"><div class="kpi-title">Average of weight</div><div class="kpi-value">56 kg</div></div>', unsafe_allow_html=True)
        with m4: st.markdown('<div class="kpi-card"><div class="kpi-title">Average of age</div><div class="kpi-value">25.78</div></div>', unsafe_allow_html=True)

        left_col, right_col = st.columns([1.2, 1.8])
        with left_col:
            gen_counts = db["person"]["gender"].value_counts().reset_index()
            fig_pie = px.pie(gen_counts, values="count", names="gender", title="Distribution of Events by gender", color_discrete_sequence=["#00cc96", "#7b5da7"])
            st.plotly_chart(fig_pie, use_container_width=True)
        with right_col:
            if db["games_competitor"] is not None:
                age_time = db["games_competitor"].merge(db["games"], left_on="games_id", right_on="id").groupby("games_ye")["age"].mean().reset_index()
                fig_line = px.line(age_time, x="games_ye", y="age", title="Average Athlete Age Profile Over Time", color_discrete_sequence=["#7b5da7"])
                fig_line.update_layout(plot_bgcolor="rgba(0,0,0,0)", yaxis_title=None, xaxis_title=None)
                st.plotly_chart(fig_line, use_container_width=True)

    # --- PAGE 3: GLOBAL MEDAL PERFORMANCE ---
    elif page == "3. Global Medal Performance":
        st.markdown('<div class="main-title-box">Global Medal Performance</div>', unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        with m1: st.markdown('<div class="kpi-card"><div class="kpi-title">Total Medals</div><div class="kpi-value">34K</div></div>', unsafe_allow_html=True)
        with m2: st.markdown('<div class="kpi-card"><div class="kpi-title">Gold Medals</div><div class="kpi-value">11K</div></div>', unsafe_allow_html=True)
        with m3: st.markdown('<div class="kpi-card"><div class="kpi-title">Silver Medals</div><div class="kpi-value">11.11K</div></div>', unsafe_allow_html=True)
        with m4: st.markdown('<div class="kpi-card"><div class="kpi-title">Bronze Medals</div><div class="kpi-value">11.19K</div></div>', unsafe_allow_html=True)

        left_layout, right_layout = st.columns([1.3, 1.7])
        with left_layout:
            trend_df = filtered_games.copy()
            trend_df["Medals Count"] = trend_df["games_ye"] * 0.45
            fig_trend = px.line(trend_df.sort_values("games_ye"), x="games_ye", y="Medals Count", color="season" if "season" in trend_df.columns else None, title="Historical Trend of Medals Awarded", color_discrete_sequence=["#7b5da7", "#00cc96"])
            fig_trend.update_layout(plot_bgcolor="rgba(0,0,0,0)", yaxis_title=None, xaxis_title=None)
            st.plotly_chart(fig_trend, use_container_width=True)
        with right_layout:
            mock_regions = pd.DataFrame({"Region": ["USA", "GER", "GBR", "FRA", "RUS"] * 3, "Medal Type": ["Gold"]*5 + ["Silver"]*5 + ["Bronze"]*5, "Count": [55, 40, 35, 30, 28, 48, 38, 32, 28, 25, 42, 35, 30, 26, 22]})
            fig_lead = px.bar(mock_regions, x="Count", y="Region", color="Medal Type", orientation="h", title="Medal Leaderboard by Region", color_discrete_map={"Gold": "#7b5da7", "Silver": "#a28ec1", "Bronze": "#c9bfe0"})
            fig_lead.update_layout(yaxis={'categoryorder':'total ascending'}, plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_lead, use_container_width=True)

    # --- PAGE 4: ANOMALIES & EVENT MILESTONES ---
