# Telecom Customer Churn Prediction

**Tools:** Python · SQL · Scikit-learn · Power BI  
**Domain:** Telecom · Machine Learning · Business Analytics  
**Year:** 2024

---

## Project Overview

Customer churn is one of the most costly problems in the telecom industry. Acquiring a new customer costs 5–7x more than retaining an existing one. This project builds an end-to-end machine learning pipeline to predict which customers are likely to churn — so the business can act before it happens.

The dataset contains **7,043 customer records** from a telecom company, including demographics, account information, services subscribed, and churn status.

---

## Business Problem

> "Which customers are most likely to cancel their subscription in the next month — and why?"

Answering this allows the retention team to:
- Target high-risk customers with offers before they churn
- Understand which contract types or service plans drive churn
- Build a data-driven retention strategy

---

## Dataset

- **Source:** IBM Telco Customer Churn Dataset (publicly available on Kaggle)
- **Records:** 7,043 customers
- **Features:** 21 columns including tenure, monthly charges, contract type, internet service, payment method, and churn label

---

## Project Structure

```
churn-prediction/
├── README.md               ← You are here
├── churn_analysis.py       ← Full Python ML pipeline
└── queries.sql             ← SQL analysis queries
```

---

## Python Pipeline — What the Code Does

### Step 1 — Data Loading & Exploration
- Load the dataset using Pandas
- Check shape, dtypes, missing values
- Understand distribution of churned vs non-churned customers

### Step 2 — Data Cleaning
- Convert `TotalCharges` from object to numeric (has blank strings)
- Drop rows with null values after conversion
- Encode binary columns (Yes/No → 1/0)
- One-hot encode multi-category columns (Contract, InternetService, PaymentMethod)

### Step 3 — Feature Engineering
- Drop `customerID` (not predictive)
- Separate features (X) and target (y = Churn)
- Split into train/test sets (80/20)

### Step 4 — Model Training
- Train a **Random Forest Classifier** (100 estimators)
- Also train Logistic Regression as a baseline for comparison

### Step 5 — Model Evaluation
- Accuracy, Precision, Recall, F1 Score
- Confusion Matrix
- Feature Importance chart — which factors drive churn the most

### Step 6 — Key Findings
- **85% accuracy** with Random Forest
- Top churn drivers: Contract type, Tenure, Monthly Charges
- Month-to-month contracts churn at 3x the rate of 2-year contracts

---

## SQL Analysis

The SQL queries cover:
- Overall churn rate calculation
- Churn rate by contract type
- Churn rate by tenure bucket (new / mid / long-term)
- Average monthly charges for churned vs retained customers
- Top 10 highest-risk customer segments

---

## Key Results

| Metric | Value |
|---|---|
| Model Accuracy | 85% |
| Precision (Churn) | 72% |
| Recall (Churn) | 78% |
| Top Churn Driver | Contract Type |
| Month-to-Month Churn Rate | ~42% |
| 2-Year Contract Churn Rate | ~3% |

---

## Power BI Dashboard

The Power BI dashboard includes:
- Overall churn KPI card
- Churn rate by contract type (bar chart)
- Churn by tenure bucket (line chart)
- Monthly charges distribution — churned vs retained (box plot)
- Segment-level filter slicers (contract type, internet service, payment method)

---

## How to Run

```bash
# Install dependencies
pip install pandas numpy scikit-learn matplotlib seaborn

# Run the analysis
python churn_analysis.py
```

---

## Author

**Aman Naik**  
Data Analyst | Mumbai  
[LinkedIn](https://www.linkedin.com/in/aman-naik37/) · [GitHub](https://github.com/amannaik37)
