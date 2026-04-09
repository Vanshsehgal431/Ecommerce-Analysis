import pandas as pd


def load_processed_master_df(df):
    df.to_csv("../data/processed/final_dataset.csv", index=False)


def load_processed_rfm(rfm):
    rfm.to_csv("../data/processed/rfm.csv", index=True)
