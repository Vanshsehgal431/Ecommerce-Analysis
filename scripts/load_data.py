import pandas as pd


def load_data():
    orders = pd.read_csv("data/raw/olist_orders_dataset.csv")
    customers = pd.read_csv("data/raw/olist_customers_dataset.csv")
    order_items = pd.read_csv("data/raw/olist_order_items_dataset.csv")
    payments = pd.read_csv("data/raw/olist_order_payments_dataset.csv")
    products = pd.read_csv("data/raw/olist_products_dataset.csv")

    return orders, customers, order_items, payments, products
