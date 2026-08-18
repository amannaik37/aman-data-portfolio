-- =============================================================
-- Website Traffic Analysis — SQL Queries
-- Author: Aman Naik
-- Database: web_analytics
-- Table: sessions
-- =============================================================

-- TABLE STRUCTURE (for reference):
-- sessions (
--   session_id           VARCHAR,
--   session_date         DATE,
--   channel              VARCHAR,
--   device               VARCHAR,
--   country              VARCHAR,
--   city                 VARCHAR,
--   landing_page         VARCHAR,
--   session_duration_sec INT,
--   pages_viewed         INT,
--   bounced              INT,   -- 1 = bounced, 0 = engaged
--   converted            INT,   -- 1 = converted, 0 = not
--   revenue              DECIMAL
-- )


-- =============================================================
-- QUERY 1: Overall KPI Summary
-- =============================================================

SELECT
    COUNT(*)                                                    AS total_sessions,
    SUM(converted)                                              AS total_conversions,
    ROUND(SUM(converted) * 100.0 / COUNT(*), 2)                AS conversion_rate_pct,
    ROUND(SUM(bounced) * 100.0 / COUNT(*), 2)                  AS bounce_rate_pct,
    ROUND(SUM(revenue), 2)                                      AS total_revenue,
    ROUND(AVG(CASE WHEN bounced = 0 THEN session_duration_sec END), 0) AS avg_session_duration_sec,
    ROUND(AVG(CASE WHEN bounced = 0 THEN pages_viewed END), 1) AS avg_pages_per_session
FROM sessions
WHERE session_date BETWEEN '2024-01-01' AND '2024-06-30';


-- =============================================================
-- QUERY 2: Monthly Session Trend
-- =============================================================

SELECT
    DATE_FORMAT(session_date, '%Y-%m')                          AS month,
    COUNT(*)                                                    AS total_sessions,
    SUM(converted)                                              AS conversions,
    ROUND(SUM(converted) * 100.0 / COUNT(*), 2)                AS cvr_pct,
    ROUND(SUM(bounced) * 100.0 / COUNT(*), 2)                  AS bounce_rate_pct,
    ROUND(SUM(revenue), 2)                                      AS revenue
FROM sessions
GROUP BY DATE_FORMAT(session_date, '%Y-%m')
ORDER BY month;


-- =============================================================
-- QUERY 3: Channel Performance (Core KPIs)
-- The most important query for stakeholder reporting
-- =============================================================

SELECT
    channel,
    COUNT(*)                                                    AS total_sessions,
    SUM(converted)                                              AS conversions,
    ROUND(SUM(converted) * 100.0 / COUNT(*), 2)                AS cvr_pct,
    ROUND(SUM(bounced) * 100.0 / COUNT(*), 2)                  AS bounce_rate_pct,
    ROUND(SUM(revenue), 2)                                      AS total_revenue,
    ROUND(SUM(revenue) / NULLIF(SUM(converted), 0), 2)         AS avg_order_value,
    ROUND(SUM(revenue) / COUNT(*), 2)                          AS revenue_per_session,
    ROUND(AVG(CASE WHEN bounced = 0 THEN pages_viewed END), 1) AS avg_pages
FROM sessions
GROUP BY channel
ORDER BY total_sessions DESC;


-- =============================================================
-- QUERY 4: Weekly Sessions Trend by Channel
-- Useful for spotting seasonal spikes per channel
-- =============================================================

SELECT
    YEARWEEK(session_date, 1)                                   AS year_week,
    channel,
    COUNT(*)                                                    AS sessions,
    SUM(converted)                                              AS conversions,
    ROUND(SUM(revenue), 2)                                      AS revenue
FROM sessions
GROUP BY YEARWEEK(session_date, 1), channel
ORDER BY year_week, sessions DESC;


-- =============================================================
-- QUERY 5: Device Performance Analysis
-- =============================================================

SELECT
    device,
    COUNT(*)                                                    AS total_sessions,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2)          AS session_share_pct,
    SUM(converted)                                              AS conversions,
    ROUND(SUM(converted) * 100.0 / COUNT(*), 2)                AS cvr_pct,
    ROUND(SUM(bounced) * 100.0 / COUNT(*), 2)                  AS bounce_rate_pct,
    ROUND(SUM(revenue), 2)                                      AS total_revenue,
    ROUND(AVG(CASE WHEN bounced = 0 THEN session_duration_sec END) / 60.0, 1) AS avg_duration_mins
FROM sessions
GROUP BY device
ORDER BY total_sessions DESC;


-- =============================================================
-- QUERY 6: Geographic Analysis — Top Countries
-- =============================================================

SELECT
    country,
    COUNT(*)                                                    AS total_sessions,
    SUM(converted)                                              AS conversions,
    ROUND(SUM(converted) * 100.0 / COUNT(*), 2)                AS cvr_pct,
    ROUND(SUM(revenue), 2)                                      AS total_revenue,
    ROUND(SUM(bounced) * 100.0 / COUNT(*), 2)                  AS bounce_rate_pct
FROM sessions
GROUP BY country
ORDER BY total_sessions DESC
LIMIT 20;


-- =============================================================
-- QUERY 7: Top Landing Pages by Sessions and CVR
-- =============================================================

SELECT
    landing_page,
    COUNT(*)                                                    AS sessions,
    SUM(converted)                                              AS conversions,
    ROUND(SUM(converted) * 100.0 / COUNT(*), 2)                AS cvr_pct,
    ROUND(SUM(bounced) * 100.0 / COUNT(*), 2)                  AS bounce_rate_pct,
    ROUND(SUM(revenue), 2)                                      AS revenue
FROM sessions
GROUP BY landing_page
HAVING COUNT(*) > 100
ORDER BY sessions DESC
LIMIT 15;


-- =============================================================
-- QUERY 8: Channel + Device Cross Analysis
-- Which channel/device combo converts best?
-- =============================================================

SELECT
    channel,
    device,
    COUNT(*)                                                    AS sessions,
    ROUND(SUM(converted) * 100.0 / COUNT(*), 2)                AS cvr_pct,
    ROUND(SUM(bounced) * 100.0 / COUNT(*), 2)                  AS bounce_rate_pct,
    ROUND(SUM(revenue), 2)                                      AS revenue
FROM sessions
GROUP BY channel, device
HAVING COUNT(*) > 200
ORDER BY cvr_pct DESC;


-- =============================================================
-- QUERY 9: Day of Week Performance
-- Which days get the most quality traffic?
-- =============================================================

SELECT
    DAYNAME(session_date)                                       AS day_of_week,
    DAYOFWEEK(session_date)                                     AS day_num,
    COUNT(*)                                                    AS total_sessions,
    ROUND(SUM(converted) * 100.0 / COUNT(*), 2)                AS cvr_pct,
    ROUND(SUM(bounced) * 100.0 / COUNT(*), 2)                  AS bounce_rate_pct,
    ROUND(SUM(revenue), 2)                                      AS revenue
FROM sessions
GROUP BY DAYNAME(session_date), DAYOFWEEK(session_date)
ORDER BY day_num;


-- =============================================================
-- QUERY 10: Month-over-Month Growth Rate
-- Tracks whether traffic and revenue are growing
-- =============================================================

WITH monthly_metrics AS (
    SELECT
        DATE_FORMAT(session_date, '%Y-%m')  AS month,
        COUNT(*)                            AS sessions,
        SUM(revenue)                        AS revenue
    FROM sessions
    GROUP BY DATE_FORMAT(session_date, '%Y-%m')
)
SELECT
    month,
    sessions,
    ROUND(revenue, 2)                       AS revenue,
    LAG(sessions) OVER (ORDER BY month)     AS prev_month_sessions,
    ROUND(
        (sessions - LAG(sessions) OVER (ORDER BY month)) * 100.0
        / NULLIF(LAG(sessions) OVER (ORDER BY month), 0), 2
    )                                       AS session_growth_pct,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY month)) * 100.0
        / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 2
    )                                       AS revenue_growth_pct
FROM monthly_metrics
ORDER BY month;
