import pandas as pd


def create_master_df(orders, customers, order_items, payments, products):
    df = (
        orders.merge(customers, on="customer_id")
        .merge(order_items, on="order_id")
        .merge(payments, on="order_id")
        .merge(products, on="product_id")
    )
    return df


def revenue_analysis(df):
    total_revenue = df["payment_value"].sum()
    avg_order_value = df.groupby("order_id")["payment_value"].sum().mean()
    return total_revenue, avg_order_value
