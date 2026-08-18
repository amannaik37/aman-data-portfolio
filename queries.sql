-- =============================================================
-- Telecom Customer Churn Analysis — SQL Queries
-- Author: Aman Naik
-- Database: telecom_churn
-- Table: customers
-- =============================================================

-- TABLE STRUCTURE (for reference):
-- customers (
--   customer_id       VARCHAR,
--   gender            VARCHAR,
--   senior_citizen    INT,
--   partner           VARCHAR,
--   dependents        VARCHAR,
--   tenure            INT,
--   phone_service     VARCHAR,
--   multiple_lines    VARCHAR,
--   internet_service  VARCHAR,
--   online_security   VARCHAR,
--   contract          VARCHAR,
--   paperless_billing VARCHAR,
--   payment_method    VARCHAR,
--   monthly_charges   DECIMAL,
--   total_charges     DECIMAL,
--   churn             VARCHAR
-- )


-- =============================================================
-- QUERY 1: Overall Churn Rate
-- =============================================================

SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    SUM(CASE WHEN churn = 'No' THEN 1 ELSE 0 END) AS retained_customers,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    ) AS churn_rate_pct
FROM customers;


-- =============================================================
-- QUERY 2: Churn Rate by Contract Type
-- Key insight: Month-to-month contracts churn the most
-- =============================================================

SELECT
    contract,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    ) AS churn_rate_pct
FROM customers
GROUP BY contract
ORDER BY churn_rate_pct DESC;


-- =============================================================
-- QUERY 3: Churn Rate by Tenure Bucket
-- New customers churn at much higher rates
-- =============================================================

SELECT
    CASE
        WHEN tenure BETWEEN 0 AND 12 THEN '0-12 months (New)'
        WHEN tenure BETWEEN 13 AND 24 THEN '13-24 months'
        WHEN tenure BETWEEN 25 AND 48 THEN '25-48 months'
        ELSE '49+ months (Loyal)'
    END AS tenure_bucket,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    ) AS churn_rate_pct
FROM customers
GROUP BY
    CASE
        WHEN tenure BETWEEN 0 AND 12 THEN '0-12 months (New)'
        WHEN tenure BETWEEN 13 AND 24 THEN '13-24 months'
        WHEN tenure BETWEEN 25 AND 48 THEN '25-48 months'
        ELSE '49+ months (Loyal)'
    END
ORDER BY churn_rate_pct DESC;


-- =============================================================
-- QUERY 4: Average Monthly Charges — Churned vs Retained
-- Churned customers typically pay more per month
-- =============================================================

SELECT
    churn,
    COUNT(*) AS customer_count,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges,
    ROUND(MIN(monthly_charges), 2) AS min_monthly_charges,
    ROUND(MAX(monthly_charges), 2) AS max_monthly_charges,
    ROUND(AVG(total_charges), 2) AS avg_total_charges
FROM customers
GROUP BY churn;


-- =============================================================
-- QUERY 5: Churn Rate by Internet Service Type
-- Fiber optic customers churn at higher rates
-- =============================================================

SELECT
    internet_service,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    ) AS churn_rate_pct,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges
FROM customers
GROUP BY internet_service
ORDER BY churn_rate_pct DESC;


-- =============================================================
-- QUERY 6: Churn Rate by Payment Method
-- =============================================================

SELECT
    payment_method,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    ) AS churn_rate_pct
FROM customers
GROUP BY payment_method
ORDER BY churn_rate_pct DESC;


-- =============================================================
-- QUERY 7: High-Risk Customer Segments
-- Month-to-month + Fiber optic + No online security = highest churn
-- =============================================================

SELECT
    contract,
    internet_service,
    online_security,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    ) AS churn_rate_pct,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges
FROM customers
GROUP BY contract, internet_service, online_security
HAVING COUNT(*) > 50
ORDER BY churn_rate_pct DESC
LIMIT 10;


-- =============================================================
-- QUERY 8: Senior Citizen Churn Analysis
-- =============================================================

SELECT
    CASE WHEN senior_citizen = 1 THEN 'Senior Citizen' ELSE 'Non-Senior' END AS customer_type,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned,
    ROUND(
        SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    ) AS churn_rate_pct,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges
FROM customers
GROUP BY senior_citizen;


-- =============================================================
-- QUERY 9: Monthly Revenue at Risk (from likely churners)
-- Identifies revenue impact of high-churn segments
-- =============================================================

SELECT
    contract,
    COUNT(*) AS at_risk_customers,
    ROUND(SUM(monthly_charges), 2) AS monthly_revenue_at_risk,
    ROUND(AVG(monthly_charges), 2) AS avg_monthly_charges
FROM customers
WHERE churn = 'Yes'
GROUP BY contract
ORDER BY monthly_revenue_at_risk DESC;


-- =============================================================
-- QUERY 10: Customer Lifetime Value Comparison
-- How much did churned vs retained customers spend overall?
-- =============================================================

SELECT
    churn AS churn_status,
    COUNT(*) AS customer_count,
    ROUND(AVG(tenure), 1) AS avg_tenure_months,
    ROUND(AVG(total_charges), 2) AS avg_lifetime_value,
    ROUND(SUM(total_charges), 2) AS total_revenue_contributed
FROM customers
GROUP BY churn;
