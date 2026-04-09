import pandas as pd


def clean_orders(orders):
    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"], errors="coerce"
    )
    return orders.dropna()


def clean_payments(payments):
    return payments[payments["payment_value"] > 0]
