# =============================================================
# Telecom Customer Churn Prediction
# Author: Aman Naik
# Tools: Python, Pandas, Scikit-learn, Matplotlib, Seaborn
# Dataset: IBM Telco Customer Churn (Kaggle)
# =============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix, classification_report
)
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

# =============================================================
# STEP 1 — LOAD DATA
# =============================================================

print("=" * 60)
print("TELECOM CUSTOMER CHURN PREDICTION")
print("=" * 60)

# Load dataset
# Download from: https://www.kaggle.com/datasets/blastchar/telco-customer-churn
df = pd.read_csv('WA_Fn-UseC_-Telco-Customer-Churn.csv')

print(f"\nDataset Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print(f"\nFirst 5 rows:")
print(df.head())

# =============================================================
# STEP 2 — EXPLORATORY DATA ANALYSIS
# =============================================================

print("\n" + "=" * 60)
print("STEP 2: EXPLORATORY DATA ANALYSIS")
print("=" * 60)

print(f"\nData Types:\n{df.dtypes}")
print(f"\nMissing Values:\n{df.isnull().sum()}")
print(f"\nChurn Distribution:\n{df['Churn'].value_counts()}")
print(f"\nChurn Rate: {round(df['Churn'].value_counts(normalize=True)['Yes'] * 100, 2)}%")

# Plot churn distribution
plt.figure(figsize=(14, 10))

plt.subplot(2, 3, 1)
churn_counts = df['Churn'].value_counts()
plt.bar(['Retained', 'Churned'], churn_counts.values, color=['#3ecfb2', '#7c6ff7'])
plt.title('Overall Churn Distribution')
plt.ylabel('Number of Customers')
for i, v in enumerate(churn_counts.values):
    plt.text(i, v + 50, str(v), ha='center', fontweight='bold')

plt.subplot(2, 3, 2)
churn_by_contract = df.groupby('Contract')['Churn'].apply(
    lambda x: (x == 'Yes').mean() * 100
).reset_index()
churn_by_contract.columns = ['Contract', 'ChurnRate']
plt.bar(churn_by_contract['Contract'], churn_by_contract['ChurnRate'], color=['#f76f6f', '#f7c46f', '#3ecfb2'])
plt.title('Churn Rate by Contract Type')
plt.ylabel('Churn Rate (%)')
plt.xticks(rotation=15)

plt.subplot(2, 3, 3)
df['TenureBucket'] = pd.cut(df['tenure'], bins=[0, 12, 24, 48, 72],
                             labels=['0-12 months', '13-24 months', '25-48 months', '49-72 months'])
churn_by_tenure = df.groupby('TenureBucket')['Churn'].apply(
    lambda x: (x == 'Yes').mean() * 100
).reset_index()
plt.bar(churn_by_tenure['TenureBucket'].astype(str),
        churn_by_tenure['Churn'], color='#7c6ff7')
plt.title('Churn Rate by Tenure')
plt.ylabel('Churn Rate (%)')
plt.xticks(rotation=20)

plt.subplot(2, 3, 4)
churned = df[df['Churn'] == 'Yes']['MonthlyCharges']
retained = df[df['Churn'] == 'No']['MonthlyCharges']
plt.hist(churned, bins=30, alpha=0.7, label='Churned', color='#f76f6f')
plt.hist(retained, bins=30, alpha=0.7, label='Retained', color='#3ecfb2')
plt.title('Monthly Charges Distribution')
plt.xlabel('Monthly Charges ($)')
plt.ylabel('Count')
plt.legend()

plt.subplot(2, 3, 5)
churn_by_internet = df.groupby('InternetService')['Churn'].apply(
    lambda x: (x == 'Yes').mean() * 100
).reset_index()
churn_by_internet.columns = ['InternetService', 'ChurnRate']
plt.bar(churn_by_internet['InternetService'], churn_by_internet['ChurnRate'],
        color=['#f7c46f', '#7c6ff7', '#3ecfb2'])
plt.title('Churn Rate by Internet Service')
plt.ylabel('Churn Rate (%)')

plt.subplot(2, 3, 6)
churn_by_payment = df.groupby('PaymentMethod')['Churn'].apply(
    lambda x: (x == 'Yes').mean() * 100
).reset_index()
churn_by_payment.columns = ['PaymentMethod', 'ChurnRate']
plt.barh(churn_by_payment['PaymentMethod'], churn_by_payment['ChurnRate'], color='#7c6ff7')
plt.title('Churn Rate by Payment Method')
plt.xlabel('Churn Rate (%)')

plt.tight_layout()
plt.savefig('eda_charts.png', dpi=150, bbox_inches='tight')
plt.show()
print("\nEDA charts saved as 'eda_charts.png'")

# =============================================================
# STEP 3 — DATA CLEANING & PREPROCESSING
# =============================================================

print("\n" + "=" * 60)
print("STEP 3: DATA CLEANING & PREPROCESSING")
print("=" * 60)

# Fix TotalCharges — has blank strings, should be numeric
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
nulls_before = df.isnull().sum().sum()
df.dropna(inplace=True)
print(f"Rows removed due to null TotalCharges: {nulls_before - df.isnull().sum().sum()}")
print(f"Dataset shape after cleaning: {df.shape}")

# Drop customerID — not predictive
df.drop('customerID', axis=1, inplace=True)

# Drop TenureBucket (created for EDA only)
if 'TenureBucket' in df.columns:
    df.drop('TenureBucket', axis=1, inplace=True)

# Encode binary Yes/No columns
binary_cols = ['Partner', 'Dependents', 'PhoneService', 'PaperlessBilling',
               'MultipleLines', 'OnlineSecurity', 'OnlineBackup',
               'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']

for col in binary_cols:
    df[col] = df[col].map({'Yes': 1, 'No': 1, 'No phone service': 0, 'No internet service': 0})

# Encode target variable
df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})

# Encode gender
df['gender'] = df['gender'].map({'Male': 1, 'Female': 0})

# One-hot encode remaining categorical columns
cat_cols = ['InternetService', 'Contract', 'PaymentMethod']
df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

print(f"\nFinal feature columns: {list(df.columns)}")
print(f"Final dataset shape: {df.shape}")

# =============================================================
# STEP 4 — FEATURE ENGINEERING & TRAIN/TEST SPLIT
# =============================================================

print("\n" + "=" * 60)
print("STEP 4: FEATURE ENGINEERING & TRAIN/TEST SPLIT")
print("=" * 60)

X = df.drop('Churn', axis=1)
y = df['Churn']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set: {X_train.shape[0]} rows")
print(f"Test set: {X_test.shape[0]} rows")
print(f"Churn rate in training set: {round(y_train.mean() * 100, 2)}%")
print(f"Churn rate in test set: {round(y_test.mean() * 100, 2)}%")

# =============================================================
# STEP 5 — MODEL TRAINING
# =============================================================

print("\n" + "=" * 60)
print("STEP 5: MODEL TRAINING")
print("=" * 60)

# Logistic Regression (baseline)
print("\nTraining Logistic Regression (baseline)...")
lr_model = LogisticRegression(max_iter=1000, random_state=42)
lr_model.fit(X_train, y_train)
lr_preds = lr_model.predict(X_test)

# Random Forest Classifier
print("Training Random Forest Classifier...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
rf_model.fit(X_train, y_train)
rf_preds = rf_model.predict(X_test)

# =============================================================
# STEP 6 — MODEL EVALUATION
# =============================================================

print("\n" + "=" * 60)
print("STEP 6: MODEL EVALUATION")
print("=" * 60)

def evaluate_model(name, y_true, y_pred):
    print(f"\n--- {name} ---")
    print(f"Accuracy:  {round(accuracy_score(y_true, y_pred) * 100, 2)}%")
    print(f"Precision: {round(precision_score(y_true, y_pred) * 100, 2)}%")
    print(f"Recall:    {round(recall_score(y_true, y_pred) * 100, 2)}%")
    print(f"F1 Score:  {round(f1_score(y_true, y_pred) * 100, 2)}%")
    print(f"\nClassification Report:\n{classification_report(y_true, y_pred)}")

evaluate_model("Logistic Regression", y_test, lr_preds)
evaluate_model("Random Forest Classifier", y_test, rf_preds)

# Confusion Matrix
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

for ax, preds, title in zip(axes, [lr_preds, rf_preds],
                             ['Logistic Regression', 'Random Forest']):
    cm = confusion_matrix(y_test, preds)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Purples',
                xticklabels=['Retained', 'Churned'],
                yticklabels=['Retained', 'Churned'], ax=ax)
    ax.set_title(f'Confusion Matrix — {title}')
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')

plt.tight_layout()
plt.savefig('confusion_matrix.png', dpi=150, bbox_inches='tight')
plt.show()
print("\nConfusion matrix saved as 'confusion_matrix.png'")

# =============================================================
# STEP 7 — FEATURE IMPORTANCE
# =============================================================

print("\n" + "=" * 60)
print("STEP 7: FEATURE IMPORTANCE")
print("=" * 60)

feature_importance = pd.DataFrame({
    'Feature': X.columns,
    'Importance': rf_model.feature_importances_
}).sort_values('Importance', ascending=False).head(15)

print("\nTop 15 Features Driving Churn:")
print(feature_importance.to_string(index=False))

plt.figure(figsize=(10, 7))
plt.barh(feature_importance['Feature'][::-1],
         feature_importance['Importance'][::-1],
         color='#7c6ff7')
plt.title('Top 15 Features Driving Customer Churn', fontsize=14, fontweight='bold')
plt.xlabel('Feature Importance Score')
plt.tight_layout()
plt.savefig('feature_importance.png', dpi=150, bbox_inches='tight')
plt.show()
print("\nFeature importance chart saved as 'feature_importance.png'")

# =============================================================
# SUMMARY
# =============================================================

print("\n" + "=" * 60)
print("FINAL SUMMARY")
print("=" * 60)
print(f"\nBest Model: Random Forest Classifier")
print(f"Accuracy:   {round(accuracy_score(y_test, rf_preds) * 100, 2)}%")
print(f"F1 Score:   {round(f1_score(y_test, rf_preds) * 100, 2)}%")
print(f"\nTop 3 Churn Drivers:")
for i, row in feature_importance.head(3).iterrows():
    print(f"  {row['Feature']}: {round(row['Importance'] * 100, 2)}%")
print("\nAnalysis complete. Check saved charts for visual output.")
