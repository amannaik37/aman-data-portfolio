# Website Traffic Analysis & Performance Dashboard

**Tools:** SQL · Python · Tableau · Excel  
**Domain:** Digital Analytics · Web Performance · Marketing  
**Year:** 2024

---

## Project Overview

Understanding where your website traffic comes from — and what happens after visitors land — is critical for any digital business. This project analyses **50,000+ website sessions** across 6 months to uncover performance trends across acquisition channels, devices, and geographies.

The goal was to replace manual Excel-based reporting with a centralised, automated analytics pipeline and a Tableau dashboard that stakeholders could use for real-time performance monitoring.

---

## Business Problem

> "Which channels are driving quality traffic? Where are users dropping off? Which regions and devices convert best?"

Answering this helps the marketing and product teams:
- Allocate budget to the highest-performing acquisition channels
- Identify underperforming regions or devices that need attention
- Track conversion funnels and spot where users are dropping off
- Replace weekly manual reporting with a live dashboard

---

## Dataset

- **Source:** Google Analytics export / simulated web session data
- **Records:** 50,000+ sessions over 6 months (Jan–Jun 2024)
- **Key Fields:** session_id, date, channel, device_type, country, city, landing_page, pages_viewed, session_duration, bounced, converted, revenue

---

## Project Structure

```
website-traffic/
├── README.md               ← You are here
├── traffic_analysis.py     ← Full Python analysis pipeline
└── queries.sql             ← SQL queries for session analysis
```

---

## Python Pipeline — What the Code Does

### Step 1 — Data Loading & Overview
- Load session-level data
- Check date range, unique channels, devices, countries
- Identify missing values and data quality issues

### Step 2 — Data Cleaning
- Parse and standardise date columns
- Handle missing session durations (fill with median per channel)
- Standardise channel names (remove inconsistent casing/formatting)
- Flag and remove duplicate session IDs

### Step 3 — Traffic Analysis
- Monthly session trend (overall + by channel)
- Channel performance: sessions, bounce rate, conversion rate, revenue
- Device breakdown: mobile vs desktop vs tablet
- Geographic analysis: top countries and cities by sessions and conversions

### Step 4 — Funnel & Engagement Analysis
- Average pages per session by channel
- Average session duration by device
- Bounce rate trends over time
- Conversion rate by channel and device

### Step 5 — Visualisations
- Line chart: monthly session trends by channel
- Bar chart: conversion rate by acquisition channel
- Heatmap: sessions by day of week and hour
- Funnel chart: sessions → engaged → converted

---

## SQL Analysis

SQL queries cover:
- Monthly and weekly session trends
- Channel-level performance (sessions, bounce rate, CVR, revenue)
- Device and geography breakdowns
- Top landing pages by sessions and conversions
- User engagement scoring

---

## Key Results

| Metric | Value |
|---|---|
| Total Sessions Analyzed | 50,000+ |
| Time Period | Jan – Jun 2024 |
| Acquisition Channels | 8+ |
| Top Converting Channel | Organic Search |
| Highest Bounce Rate | Direct Traffic |
| Best Converting Device | Desktop |
| KPIs Tracked in Dashboard | 10+ |

---

## Tableau Dashboard

The Tableau dashboard includes:
- Session trend line chart (monthly, filterable by channel)
- Channel performance comparison table (sessions, CVR, revenue)
- Geographic map — sessions and conversions by country
- Device split donut chart
- Bounce rate trend over time
- KPI summary cards (total sessions, total revenue, avg session duration, overall CVR)
- Filter slicers: date range, channel, device, country

---

## How to Run

```bash
# Install dependencies
pip install pandas numpy matplotlib seaborn

# Run the analysis
python traffic_analysis.py
```

---

## Author

**Aman Naik**  
Data Analyst | Mumbai  
[LinkedIn](https://www.linkedin.com/in/aman-naik37/) · [GitHub](https://github.com/amannaik37)
