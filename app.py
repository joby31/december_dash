import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Pantry Dashboard", layout="wide")

st.markdown(
    "<h1 style='text-align:center;'>📊 Pantry Monthly Performance Dashboard</h1>",
    unsafe_allow_html=True
)

# ---------------- DATA PATH ----------------
DATA_DIR = "data"

FILES = {
    "new_old": "Dec_2025_New_vs_Old_Customers.xlsx",
    "monthly": "monthly customer count.xlsx",
    "retention": "Dec_2025_Daily_Retention (1).xlsx",
    "profit": "December_2025_Gross_Profit.xlsx"
}

# ---------------- FILE CHECK ----------------
for f in FILES.values():
    if not os.path.exists(os.path.join(DATA_DIR, f)):
        st.error(f"❌ File not found: data/{f}")
        st.stop()

# ---------------- LOAD DATA ----------------
new_old_df = pd.read_excel(os.path.join(DATA_DIR, FILES["new_old"]))
monthly_df = pd.read_excel(os.path.join(DATA_DIR, FILES["monthly"]))
retention_df = pd.read_excel(os.path.join(DATA_DIR, FILES["retention"]))
profit_df = pd.read_excel(os.path.join(DATA_DIR, FILES["profit"]))

# ---------------- DATE FIX ----------------
def fix_date(df):
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    return df.dropna(subset=["Date"])

monthly_df = fix_date(monthly_df)
retention_df = fix_date(retention_df)
profit_df = fix_date(profit_df)

# ---------------- AUTO FIND NUMERIC COLUMN ----------------
def get_numeric_column(df):
    numeric_cols = df.select_dtypes(include="number").columns
    if len(numeric_cols) == 0:
        st.error("❌ No numeric column found")
        st.stop()
    return numeric_cols[0]

monthly_col = get_numeric_column(monthly_df)
retention_col = get_numeric_column(retention_df)
profit_col = get_numeric_column(profit_df)

# ---------------- KPI CALCULATIONS ----------------
total_customers = int(monthly_df[monthly_col].sum())
avg_customers = int(monthly_df[monthly_col].mean())
total_retention = int(retention_df[retention_col].sum())
total_profit = int(profit_df[profit_col].sum())

# ---------------- KPI CARDS ----------------
k1, k2, k3, k4 = st.columns(4)

k1.metric("👥 Total Customers", f"{total_customers:,}")
k2.metric("📊 Avg Daily Customers", avg_customers)
k3.metric("🔁 Total Retention", f"{total_retention:,}")
k4.metric("💰 Gross Profit", f"₹ {total_profit:,}")

st.markdown("---")

# ---------------- ROW 1 ----------------
c1, c2 = st.columns(2)

pie_fig = px.pie(
    new_old_df,
    names=new_old_df.columns[0],
    values=new_old_df.columns[1],
    hole=0.4,
    title="New vs Old Customers"
)
pie_fig.update_layout(title_x=0.5)
c1.plotly_chart(pie_fig, use_container_width=True)

line_monthly = px.line(
    monthly_df,
    x="Date",
    y=monthly_col,
    markers=True,
    title="Monthly Customer Count Trend"
)
line_monthly.update_layout(title_x=0.5)
c2.plotly_chart(line_monthly, use_container_width=True)

# ---------------- ROW 2 ----------------
c3, c4 = st.columns(2)

line_retention = px.line(
    retention_df,
    x="Date",
    y=retention_col,
    markers=True,
    title="Day-wise Customer Retention"
)
line_retention.update_layout(title_x=0.5)
c3.plotly_chart(line_retention, use_container_width=True)

line_profit = px.line(
    profit_df,
    x="Date",
    y=profit_col,
    markers=True,
    title="Daily Gross Profit Trend"
)
line_profit.update_layout(title_x=0.5)
c4.plotly_chart(line_profit, use_container_width=True)

# ---------------- FOOTER ----------------
st.markdown(
    "<p style='text-align:center;color:gray;'>Power BI Style Dashboard | Streamlit</p>",
    unsafe_allow_html=True
)
