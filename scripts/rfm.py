import pandas as pd


def compute_rfm(df):
    snapshot_date = df["order_purchase_timestamp"].max()

    rfm = df.groupby("customer_unique_id").agg(
        {
            "order_purchase_timestamp": lambda x: (snapshot_date - x.max()).days,
            "order_id": "nunique",
            "payment_value": "sum",
        }
    )

    rfm.columns = ["Recency", "Frequency", "Monetary"]

    rfm["R"] = pd.qcut(rfm["Recency"].rank(method="first"), 4, labels=[4, 3, 2, 1])

    rfm["F"] = pd.qcut(rfm["Frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4])

    rfm["M"] = pd.qcut(rfm["Monetary"].rank(method="first"), 4, labels=[1, 2, 3, 4])

    rfm["Score"] = rfm[["R", "F", "M"]].astype(int).sum(axis=1)

    return rfm
