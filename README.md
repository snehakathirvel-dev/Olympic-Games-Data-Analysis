# End-to-End Olympic Games Data Analytics Portfolio Project

A comprehensive data analytics and data engineering project that builds a structured relational database backend using **PostgreSQL** to clean and model historical records, combined with a production-ready interactive visual reporting layer in **Power BI**. 

---

## 🛠️ Technology Stack & Tools
* **Database Backend:** PostgreSQL (Advanced relational design, indexing, and multi-table analysis)
* **Data Visualization:** Power BI Desktop (Interactive multi-tab dashboard layout)
* **Scripting & Automation:** Python 3 (`python-pptx` custom automation engine)
* **IDE Development:** Visual Studio Code & Git Version Control

---

## 📂 Project Repository Structure
```text
Olympic_Games_Project/
├── CSV/                      # Data Ingestion: 25 structured relational flat files
├── sports_psql_project.sql   # Data Engineering: Core script covering 18 analytical milestones
├── project_1.pbix            # Reporting Layer: Multi-tab interactive dashboard file
└── Olympic_Games_Analysis_Project.pdf  # Executive Presentation Deck
```

---

## 💻 SQL Data Engineering & Analytics Focus
The database backend consists of **18 comprehensive structural data queries** designed to parse global event timelines, participation streaks, and historical anomalies over more than a century of games. 

### Key Technical Implementations:
* **Advanced Multi-Table Joins:** Linking historical `games`, `competitor_event`, and geographic region datasets across changing eras.
* **Time Intelligence Blocks:** Designing complex groupings to track host frequency distributions and year-over-year competition velocity.
* **Anomaly Identification Modules:** Constructing isolated filters to isolate short-lived competitive events, sport classification lifecycles, and exceptional performance metrics.

---

## 📊 Production Power BI Dashboard Architecture
The data modeling layer maps data inputs smoothly onto a polished, **4-perspective reporting layout** configured for fluid cross-filtering and metric tracking:

1. **Olympic Games Overview:** Features high-level strategic KPI cards mapping active eras, historical edition totals, and macro participant growth timelines.
2. **Athlete & Sport Demographics:** Drives analytical views into shifting physical distributions (age metrics, height/weight matrices) along with granular tracking of changing gender distribution representation across decades.
3. **Global Medal Performance:** Built around dynamic stacked horizontal nation leaderboards broken down by Gold, Silver, and Bronze splits, anchored alongside interactive geographic bubble distribution maps.
4. **Anomalies & Event Milestones:** Tracks specific category debuts, lifecycle phases of historical competition changes, and structured treemaps visualizing the timelines of discontinued sports categories like Tug-of-War.
