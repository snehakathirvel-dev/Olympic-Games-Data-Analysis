--1. Frequency and Trends of Hosting the Olympic Games
SELECT 
    (games_year / 10) * 10 AS decade_block,
    season,
    COUNT(DISTINCT id) AS unique_games_hosted
FROM games
GROUP BY (games_year / 10) * 10, season
ORDER BY decade_block ASC, season;


--2. Changes in the Duration of Olympic Games Over Time
SELECT 
    g.games_year,
    g.games_name,
    g.season,
    COUNT(DISTINCT ce.event_id) AS total_scheduled_events
FROM games g
JOIN games_competitor gc ON g.id = gc.games_id
JOIN competitor_event ce ON gc.id = ce.competitor_id
GROUP BY g.id, g.games_year, g.games_name, g.season
ORDER BY g.games_year ASC, g.season;

--3. Notable Event Densities or Anomalies Associated with Specific Games
SELECT 
    g.games_year, 
    g.games_name,
    COUNT(DISTINCT gc.person_id) AS total_participating_athletes,
    COUNT(DISTINCT e.sport_id) AS total_distinct_sports,
    COUNT(ce.medal_id) FILTER (WHERE ce.medal_id IN (1, 2, 3)) AS total_medals_awarded
FROM games g
JOIN games_competitor gc ON g.id = gc.games_id
JOIN competitor_event ce ON gc.id = ce.competitor_id
JOIN event e ON ce.event_id = e.id
GROUP BY g.id, g.games_year, g.games_name
ORDER BY total_participating_athletes DESC;

--4. Emerging Sports Recently Added to the Olympics
SELECT 
    s.sport_name,
    MIN(g.games_year) AS debut_year
FROM sport s
JOIN event e ON s.id = e.sport_id
JOIN competitor_event ce ON e.id = ce.event_id
JOIN games_competitor gc ON ce.competitor_id = gc.id
JOIN games g ON gc.games_id = g.id
GROUP BY s.id, s.sport_name
ORDER BY debut_year DESC, s.sport_name ASC;

--5. Shifting Popularity Metrics of Sports Over Time
SELECT 
    g.games_year,
    s.sport_name,
    COUNT(DISTINCT gc.person_id) AS total_active_athletes
FROM games_competitor gc
JOIN games g ON gc.games_id = g.id
JOIN competitor_event ce ON gc.id = ce.competitor_id
JOIN event e ON ce.event_id = e.id
JOIN sport s ON e.sport_id = s.id
GROUP BY g.games_year, s.sport_name
ORDER BY s.sport_name, g.games_year ASC;

--6. Sports Uniquely Tied to Particular Regions or Cultures
SELECT 
    s.sport_name,
    nr.region_name,
    COUNT(ce.medal_id) AS total_medals_won
FROM competitor_event ce
JOIN medal m ON ce.medal_id = m.id
JOIN event e ON ce.event_id = e.id
JOIN sport s ON e.sport_id = s.id
JOIN games_competitor gc ON ce.competitor_id = gc.id
JOIN person_region pr ON gc.person_id = pr.person_id
JOIN noc_region nr ON pr.region_id = nr.id
WHERE m.medal_name IN ('Gold', 'Silver', 'Bronze')
GROUP BY s.sport_name, nr.region_name
ORDER BY s.sport_name ASC, total_medals_won DESC;

--7. Gender-Based Balance Tracking and Imbalances Across Sports
SELECT 
    s.sport_name,
    p.gender,
    COUNT(DISTINCT ce.event_id) AS total_distinct_events
FROM competitor_event ce
JOIN event e ON ce.event_id = e.id
JOIN sport s ON e.sport_id = s.id
JOIN games_competitor gc ON ce.competitor_id = gc.id
JOIN person p ON gc.person_id = p.id
GROUP BY s.sport_name, p.gender
ORDER BY s.sport_name ASC, total_distinct_events DESC;

--8. Chronological Introductions of Brand New Events
SELECT 
    e.event_name,
    s.sport_name,
    MIN(g.games_year) AS event_introduction_year
FROM event e
JOIN sport s ON e.sport_id = s.id
JOIN competitor_event ce ON e.id = ce.event_id
JOIN games_competitor gc ON ce.competitor_id = gc.id
JOIN games g ON gc.games_id = g.id
GROUP BY e.event_name, s.sport_name
ORDER BY event_introduction_year DESC, e.event_name ASC;

--9. Are there any events that have been discontinued or removed from the Olympics?
SELECT 
    e.event_name,
    MIN(g.games_year) AS first_appearance,
    MAX(g.games_year) AS last_appearance
FROM event e
JOIN competitor_event ce ON e.id = ce.event_id
JOIN games_competitor gc ON ce.competitor_id = gc.id
JOIN games g ON gc.games_id = g.id
GROUP BY e.event_name
HAVING MAX(g.games_year) < (SELECT MAX(games_year) FROM games)
ORDER BY last_appearance DESC, event_name ASC;

--10. Are there any notable trends in the height and weight of participants over time?
SELECT 
    g.games_year,
    ROUND(AVG(p.height) FILTER (WHERE p.height > 0), 2) AS avg_height_cm,
    ROUND(AVG(p.weight) FILTER (WHERE p.weight > 0), 2) AS avg_weight_kg,
    COUNT(DISTINCT p.id) AS total_athletes_measured
FROM games g
JOIN games_competitor gc ON g.id = gc.games_id
JOIN person p ON gc.person_id = p.id
GROUP BY g.games_year
ORDER BY g.games_year ASC;

--11. Are there any dominant countries or regions in specific sports or events?
SELECT 
    s.sport_name,
    nr.region_name,
    COUNT(ce.medal_id) AS total_medals_won
FROM competitor_event ce
JOIN medal m ON ce.medal_id = m.id
JOIN event e ON ce.event_id = e.id
JOIN sport s ON e.sport_id = s.id
JOIN games_competitor gc ON ce.competitor_id = gc.id
JOIN person_region pr ON gc.person_id = pr.person_id
JOIN noc_region nr ON pr.region_id = nr.id
WHERE m.medal_name IN ('Gold', 'Silver', 'Bronze')
GROUP BY s.sport_name, nr.region_name
ORDER BY s.sport_name ASC, total_medals_won DESC;

--12. Physical and Biometric Factors Contributing to Success
SELECT 
    nr.region_name,
    COUNT(ce.medal_id) AS total_medals_won,
    ROUND(AVG(gc.age), 1) AS avg_medalist_age,
    ROUND(AVG(p.height) FILTER (WHERE p.height > 0), 1) AS avg_medalist_height_cm,
    ROUND(AVG(p.weight) FILTER (WHERE p.weight > 0), 1) AS avg_medalist_weight_kg
FROM competitor_event ce
JOIN medal m ON ce.medal_id = m.id
JOIN games_competitor gc ON ce.competitor_id = gc.id
JOIN person p ON gc.person_id = p.id
JOIN person_region pr ON p.id = pr.person_id
JOIN noc_region nr ON pr.region_id = nr.id
WHERE m.medal_name IN ('Gold', 'Silver', 'Bronze')
GROUP BY nr.region_name
ORDER BY total_medals_won DESC;

--13. All-Time Country Consistency (Multi-Edition Performance)
SELECT 
    nr.region_name,
    COUNT(DISTINCT gc.games_id) AS consecutive_editions_medaled,
    COUNT(ce.medal_id) AS total_medals_all_time
FROM competitor_event ce
JOIN medal m ON ce.medal_id = m.id
JOIN games_competitor gc ON ce.competitor_id = gc.id
JOIN person_region pr ON gc.person_id = pr.person_id
JOIN noc_region nr ON pr.region_id = nr.id
WHERE m.medal_name IN ('Gold', 'Silver', 'Bronze')
GROUP BY nr.region_name
HAVING COUNT(DISTINCT gc.games_id) > 1
ORDER BY consecutive_editions_medaled DESC, total_medals_all_time DESC;

--14. Regional Domination Over Specific Sports or Events
SELECT 
    s.sport_name,
    nr.region_name,
    COUNT(ce.medal_id) AS total_medals_won,
    DENSE_RANK() OVER (PARTITION BY s.sport_name ORDER BY COUNT(ce.medal_id) DESC) AS regional_rank_in_sport
FROM competitor_event ce
JOIN medal m ON ce.medal_id = m.id
JOIN event e ON ce.event_id = e.id
JOIN sport s ON e.sport_id = s.id
JOIN games_competitor gc ON ce.competitor_id = gc.id
JOIN person_region pr ON gc.person_id = pr.person_id
JOIN noc_region nr ON pr.region_id = nr.id
WHERE m.medal_name IN ('Gold', 'Silver', 'Bronze')
GROUP BY s.sport_name, nr.region_name
ORDER BY s.sport_name ASC, total_medals_won DESC;

--15. Unexpected or Surprising Historical Wins
WITH regional_historical_tallies AS (
    SELECT 
        pr.region_id,
        COUNT(ce.medal_id) AS lifetime_medals
    FROM competitor_event ce
    JOIN medal m ON ce.medal_id = m.id
    JOIN games_competitor gc ON ce.competitor_id = gc.id
    JOIN person_region pr ON gc.person_id = pr.person_id
    WHERE m.medal_name IN ('Gold', 'Silver', 'Bronze')
    GROUP BY pr.region_id
)
SELECT 
    g.games_year,
    g.games_name,
    nr.region_name AS underdog_country,
    p.full_name AS athlete_name,
    e.event_name,
    m.medal_name
FROM competitor_event ce
JOIN medal m ON ce.medal_id = m.id
JOIN event e ON ce.event_id = e.id
JOIN games_competitor gc ON ce.competitor_id = gc.id
JOIN games g ON gc.games_id = g.id
JOIN person p ON gc.person_id = p.id
JOIN person_region pr ON p.id = pr.person_id
JOIN noc_region nr ON pr.region_id = nr.id
JOIN regional_historical_tallies rht ON pr.region_id = rht.region_id
WHERE m.medal_name IN ('Gold', 'Silver', 'Bronze')
  AND rht.lifetime_medals < 5
ORDER BY g.games_year DESC, underdog_country ASC;

--16. Delegation Expansion and Decline Trajectories
SELECT 
    g.games_year,
    g.games_name,
    nr.region_name,
    COUNT(DISTINCT gc.person_id) AS delegation_athlete_volume
FROM games_competitor gc
JOIN games g ON gc.games_id = g.id
JOIN person_region pr ON gc.person_id = pr.person_id
JOIN noc_region nr ON pr.region_id = nr.id
GROUP BY g.games_year, g.games_name, nr.region_name
ORDER BY nr.region_name ASC, g.games_year ASC;

--17 & 18. Influence of Geography & All-Time Global Leaderboard Share
SELECT 
    nr.region_name,
    COUNT(CASE WHEN m.medal_name = 'Gold' THEN 1 END) AS gold_count,
    COUNT(CASE WHEN m.medal_name = 'Silver' THEN 1 END) AS silver_count,
    COUNT(CASE WHEN m.medal_name = 'Bronze' THEN 1 END) AS bronze_count,
    COUNT(ce.medal_id) AS total_medals_won,
    ROUND(
        (COUNT(ce.medal_id)::NUMERIC / (SELECT COUNT(*) FROM competitor_event WHERE medal_id IN (1, 2, 3))) * 100, 
        2
    ) AS global_podium_percentage_share
FROM competitor_event ce
JOIN medal m ON ce.medal_id = m.id
JOIN games_competitor gc ON ce.competitor_id = gc.id
JOIN person_region pr ON gc.person_id = pr.person_id
JOIN noc_region nr ON pr.region_id = nr.id
WHERE m.medal_name IN ('Gold', 'Silver', 'Bronze')
GROUP BY nr.region_name
ORDER BY total_medals_won DESC;






















