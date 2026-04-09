import pandas as pd
import streamlit as st

from scripts.analysis import create_master_df
from scripts.clean_data import clean_orders, clean_payments
from scripts.load_data import load_data
from scripts.rfm import compute_rfm

st.set_page_config(page_title="E-commerce Analysis", layout="wide")

st.title("🛒 E-commerce Customer Behavior Analysis")
st.markdown("Understand revenue, trends, and customer segments")


@st.cache_data
def load_pipeline():
    orders, customers, items, payments, products = load_data()
    orders = clean_orders(orders)
    payments = clean_payments(payments)

    df = create_master_df(orders, customers, items, payments, products)
    rfm = compute_rfm(df)

    return df, rfm


df, rfm = load_pipeline()


st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

total_revenue = df["payment_value"].sum()
total_orders = df["order_id"].nunique()
avg_order = total_revenue / total_orders

col1.metric("💰 Revenue", f"{total_revenue:,.0f}")
col2.metric("📦 Orders", total_orders)
col3.metric("🧾 Avg Order", f"{avg_order:.2f}")

st.sidebar.title("Filters")

category = st.sidebar.selectbox(
    "Select Category", df["product_category_name"].dropna().unique()
)

filtered_df = df[df["product_category_name"] == category]

st.subheader("📈 Sales Trend")

filtered_df["date"] = pd.to_datetime(filtered_df["order_purchase_timestamp"]).dt.date
daily_sales = filtered_df.groupby("date")["payment_value"].sum()

st.line_chart(daily_sales)

col1, col2 = st.columns(2)

top_categories = (
    df.groupby("product_category_name")["payment_value"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

col1.subheader("🛒 Top Categories")
col1.bar_chart(top_categories)

col2.subheader("👤 Customer Segments")
col2.bar_chart(rfm["Score"].value_counts())


st.subheader("🏆 Top Customers")

top_customers = (
    df.groupby("customer_unique_id")["payment_value"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

st.table(top_customers)

st.subheader("🧠 Key Insights")

st.markdown(
    """
- Top customers generate majority of revenue  
- Some categories dominate sales  
- Repeat customers contribute higher value  
- Opportunity to improve retention strategies  
"""
)

st.subheader("🔥 Revenue by Category")

category_revenue = (
    df.groupby("product_category_name")["payment_value"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(category_revenue.head(10))
