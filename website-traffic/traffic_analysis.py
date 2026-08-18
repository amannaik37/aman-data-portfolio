# =============================================================
# Website Traffic Analysis & Performance Dashboard
# Author: Aman Naik
# Tools: Python, Pandas, Matplotlib, Seaborn, NumPy
# =============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from datetime import datetime, timedelta
import random
import warnings
warnings.filterwarnings('ignore')

# =============================================================
# STEP 1 — GENERATE / LOAD DATA
# =============================================================
# In a real project, replace this with:
# df = pd.read_csv('web_sessions.csv')
# or connect via Google Analytics API export

print("=" * 60)
print("WEBSITE TRAFFIC ANALYSIS & PERFORMANCE DASHBOARD")
print("=" * 60)

random.seed(42)
np.random.seed(42)

n = 50000
channels = ['Organic Search', 'Paid Search', 'Social Media', 'Direct',
            'Email', 'Referral', 'Display Ads', 'Affiliate']
channel_weights = [0.30, 0.20, 0.15, 0.12, 0.08, 0.07, 0.05, 0.03]
devices = ['Desktop', 'Mobile', 'Tablet']
device_weights = [0.48, 0.42, 0.10]
countries = ['India', 'United States', 'United Kingdom', 'Australia',
             'Canada', 'Germany', 'Singapore', 'UAE']
country_weights = [0.35, 0.25, 0.12, 0.08, 0.07, 0.05, 0.04, 0.04]

start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 6, 30)
date_range = (end_date - start_date).days

dates = [start_date + timedelta(days=random.randint(0, date_range)) for _ in range(n)]
channel_list = random.choices(channels, weights=channel_weights, k=n)
device_list = random.choices(devices, weights=device_weights, k=n)
country_list = random.choices(countries, weights=country_weights, k=n)

# Bounce rate varies by channel
bounce_probs = {
    'Organic Search': 0.35, 'Paid Search': 0.45, 'Social Media': 0.55,
    'Direct': 0.60, 'Email': 0.30, 'Referral': 0.40,
    'Display Ads': 0.65, 'Affiliate': 0.50
}
bounced = [1 if random.random() < bounce_probs[c] else 0 for c in channel_list]

# Conversion rate varies by channel and device
conv_probs = {
    ('Organic Search', 'Desktop'): 0.05, ('Organic Search', 'Mobile'): 0.03,
    ('Paid Search', 'Desktop'): 0.06, ('Paid Search', 'Mobile'): 0.04,
    ('Email', 'Desktop'): 0.08, ('Email', 'Mobile'): 0.05,
    ('Social Media', 'Desktop'): 0.02, ('Social Media', 'Mobile'): 0.015,
    ('Direct', 'Desktop'): 0.04, ('Direct', 'Mobile'): 0.025,
    ('Referral', 'Desktop'): 0.045, ('Referral', 'Mobile'): 0.03,
    ('Display Ads', 'Desktop'): 0.015, ('Display Ads', 'Mobile'): 0.01,
    ('Affiliate', 'Desktop'): 0.035, ('Affiliate', 'Mobile'): 0.02,
}
converted = [
    0 if bounced[i] == 1 else (
        1 if random.random() < conv_probs.get((channel_list[i], device_list[i]), 0.03) else 0
    )
    for i in range(n)
]

session_durations = [
    0 if bounced[i] == 1 else max(30, int(np.random.normal(180, 90)))
    for i in range(n)
]
pages_viewed = [
    1 if bounced[i] == 1 else max(2, int(np.random.normal(4.5, 2)))
    for i in range(n)
]
revenue = [
    round(np.random.uniform(20, 500), 2) if converted[i] == 1 else 0.0
    for i in range(n)
]

df = pd.DataFrame({
    'session_id': [f'S{str(i).zfill(6)}' for i in range(n)],
    'date': dates,
    'channel': channel_list,
    'device': device_list,
    'country': country_list,
    'session_duration_sec': session_durations,
    'pages_viewed': pages_viewed,
    'bounced': bounced,
    'converted': converted,
    'revenue': revenue
})

df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.to_period('M')
df['week'] = df['date'].dt.isocalendar().week
df['day_of_week'] = df['date'].dt.day_name()
df['hour'] = df['date'].dt.hour

print(f"\nDataset loaded: {df.shape[0]:,} sessions")
print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
print(f"Channels: {df['channel'].nunique()}")
print(f"Countries: {df['country'].nunique()}")

# =============================================================
# STEP 2 — DATA QUALITY CHECK
# =============================================================

print("\n" + "=" * 60)
print("STEP 2: DATA QUALITY CHECK")
print("=" * 60)

print(f"\nMissing values:\n{df.isnull().sum()}")
print(f"\nDuplicate session IDs: {df['session_id'].duplicated().sum()}")
print(f"\nData types:\n{df.dtypes}")

# =============================================================
# STEP 3 — OVERALL PERFORMANCE SUMMARY
# =============================================================

print("\n" + "=" * 60)
print("STEP 3: OVERALL PERFORMANCE SUMMARY")
print("=" * 60)

total_sessions = len(df)
total_conversions = df['converted'].sum()
total_revenue = df['revenue'].sum()
overall_cvr = total_conversions / total_sessions * 100
overall_bounce = df['bounced'].mean() * 100
avg_duration = df[df['bounced'] == 0]['session_duration_sec'].mean()
avg_pages = df[df['bounced'] == 0]['pages_viewed'].mean()

print(f"\nTotal Sessions:       {total_sessions:,}")
print(f"Total Conversions:    {total_conversions:,}")
print(f"Total Revenue:        ${total_revenue:,.2f}")
print(f"Overall CVR:          {overall_cvr:.2f}%")
print(f"Overall Bounce Rate:  {overall_bounce:.2f}%")
print(f"Avg Session Duration: {avg_duration:.0f} seconds ({avg_duration/60:.1f} mins)")
print(f"Avg Pages per Visit:  {avg_pages:.1f}")

# =============================================================
# STEP 4 — CHANNEL PERFORMANCE ANALYSIS
# =============================================================

print("\n" + "=" * 60)
print("STEP 4: CHANNEL PERFORMANCE ANALYSIS")
print("=" * 60)

channel_perf = df.groupby('channel').agg(
    sessions=('session_id', 'count'),
    conversions=('converted', 'sum'),
    revenue=('revenue', 'sum'),
    bounce_rate=('bounced', 'mean'),
    avg_duration=('session_duration_sec', 'mean'),
    avg_pages=('pages_viewed', 'mean')
).reset_index()

channel_perf['cvr'] = channel_perf['conversions'] / channel_perf['sessions'] * 100
channel_perf['bounce_rate'] = channel_perf['bounce_rate'] * 100
channel_perf['revenue_per_session'] = channel_perf['revenue'] / channel_perf['sessions']
channel_perf = channel_perf.sort_values('sessions', ascending=False)

print("\nChannel Performance Summary:")
print(channel_perf[['channel', 'sessions', 'conversions', 'cvr', 'bounce_rate', 'revenue']].to_string(index=False))

# =============================================================
# STEP 5 — MONTHLY TREND ANALYSIS
# =============================================================

print("\n" + "=" * 60)
print("STEP 5: MONTHLY TREND ANALYSIS")
print("=" * 60)

monthly = df.groupby('month').agg(
    sessions=('session_id', 'count'),
    conversions=('converted', 'sum'),
    revenue=('revenue', 'sum'),
    bounce_rate=('bounced', 'mean')
).reset_index()
monthly['cvr'] = monthly['conversions'] / monthly['sessions'] * 100
monthly['bounce_rate'] = monthly['bounce_rate'] * 100

print("\nMonthly Summary:")
print(monthly.to_string(index=False))

monthly_channel = df.groupby(['month', 'channel'])['session_id'].count().reset_index()
monthly_channel.columns = ['month', 'channel', 'sessions']

# =============================================================
# STEP 6 — DEVICE & GEOGRAPHY ANALYSIS
# =============================================================

print("\n" + "=" * 60)
print("STEP 6: DEVICE & GEOGRAPHY ANALYSIS")
print("=" * 60)

device_perf = df.groupby('device').agg(
    sessions=('session_id', 'count'),
    conversions=('converted', 'sum'),
    revenue=('revenue', 'sum'),
    bounce_rate=('bounced', 'mean')
).reset_index()
device_perf['cvr'] = device_perf['conversions'] / device_perf['sessions'] * 100
device_perf['bounce_rate'] = device_perf['bounce_rate'] * 100
print("\nDevice Performance:")
print(device_perf.to_string(index=False))

country_perf = df.groupby('country').agg(
    sessions=('session_id', 'count'),
    conversions=('converted', 'sum'),
    revenue=('revenue', 'sum')
).reset_index()
country_perf['cvr'] = country_perf['conversions'] / country_perf['sessions'] * 100
country_perf = country_perf.sort_values('sessions', ascending=False)
print("\nTop Countries:")
print(country_perf.to_string(index=False))

# =============================================================
# STEP 7 — VISUALISATIONS
# =============================================================

print("\n" + "=" * 60)
print("STEP 7: GENERATING VISUALISATIONS")
print("=" * 60)

fig, axes = plt.subplots(2, 3, figsize=(18, 11))
fig.suptitle('Website Traffic Analysis — Jan to Jun 2024', fontsize=16, fontweight='bold', y=1.01)

# Chart 1: Monthly sessions trend
ax1 = axes[0, 0]
monthly_str = monthly.copy()
monthly_str['month'] = monthly_str['month'].astype(str)
ax1.plot(monthly_str['month'], monthly_str['sessions'], marker='o', color='#7c6ff7', linewidth=2.5)
ax1.fill_between(monthly_str['month'], monthly_str['sessions'], alpha=0.15, color='#7c6ff7')
ax1.set_title('Monthly Session Trend')
ax1.set_ylabel('Sessions')
ax1.tick_params(axis='x', rotation=30)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

# Chart 2: Channel sessions bar
ax2 = axes[0, 1]
ch_sorted = channel_perf.sort_values('sessions', ascending=True)
bars = ax2.barh(ch_sorted['channel'], ch_sorted['sessions'], color='#3ecfb2')
ax2.set_title('Sessions by Channel')
ax2.set_xlabel('Sessions')
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

# Chart 3: CVR by channel
ax3 = axes[0, 2]
ch_cvr = channel_perf.sort_values('cvr', ascending=True)
ax3.barh(ch_cvr['channel'], ch_cvr['cvr'], color='#f7c46f')
ax3.set_title('Conversion Rate by Channel (%)')
ax3.set_xlabel('CVR (%)')

# Chart 4: Device split
ax4 = axes[1, 0]
colors = ['#7c6ff7', '#3ecfb2', '#f7c46f']
ax4.pie(device_perf['sessions'], labels=device_perf['device'],
        autopct='%1.1f%%', colors=colors, startangle=90)
ax4.set_title('Sessions by Device')

# Chart 5: Bounce rate by channel
ax5 = axes[1, 1]
ch_bounce = channel_perf.sort_values('bounce_rate', ascending=True)
ax5.barh(ch_bounce['channel'], ch_bounce['bounce_rate'], color='#f76f6f')
ax5.set_title('Bounce Rate by Channel (%)')
ax5.set_xlabel('Bounce Rate (%)')

# Chart 6: Revenue by channel
ax6 = axes[1, 2]
ch_rev = channel_perf.sort_values('revenue', ascending=True)
ax6.barh(ch_rev['channel'], ch_rev['revenue'], color='#7c6ff7')
ax6.set_title('Revenue by Channel ($)')
ax6.set_xlabel('Revenue ($)')
ax6.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'${x:,.0f}'))

plt.tight_layout()
plt.savefig('traffic_dashboard.png', dpi=150, bbox_inches='tight')
plt.show()
print("\nDashboard chart saved as 'traffic_dashboard.png'")

# Heatmap: sessions by day and hour
pivot = df.groupby(['day_of_week', 'hour'])['session_id'].count().unstack(fill_value=0)
day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
pivot = pivot.reindex([d for d in day_order if d in pivot.index])

plt.figure(figsize=(16, 5))
sns.heatmap(pivot, cmap='Purples', linewidths=0.3, annot=False)
plt.title('Session Volume Heatmap — Day of Week vs Hour', fontsize=13, fontweight='bold')
plt.xlabel('Hour of Day')
plt.ylabel('Day of Week')
plt.tight_layout()
plt.savefig('session_heatmap.png', dpi=150, bbox_inches='tight')
plt.show()
print("Session heatmap saved as 'session_heatmap.png'")

# =============================================================
# SUMMARY
# =============================================================

print("\n" + "=" * 60)
print("FINAL SUMMARY")
print("=" * 60)
print(f"\nTotal Sessions Analyzed:  {total_sessions:,}")
print(f"Total Revenue Generated:  ${total_revenue:,.2f}")
print(f"Overall Conversion Rate:  {overall_cvr:.2f}%")
print(f"Overall Bounce Rate:      {overall_bounce:.2f}%")
best_channel = channel_perf.loc[channel_perf['cvr'].idxmax(), 'channel']
worst_bounce = channel_perf.loc[channel_perf['bounce_rate'].idxmax(), 'channel']
print(f"Best Converting Channel:  {best_channel}")
print(f"Highest Bounce Channel:   {worst_bounce}")
print("\nAnalysis complete. Check saved charts for visual output.")
