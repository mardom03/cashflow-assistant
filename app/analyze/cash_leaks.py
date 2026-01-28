from datetime import datetime
import pandas as pd

def overdue_invoices(df, days=30):
    df["DueDate"] = pd.to_datetime(df["DueDate"])
    cutoff = datetime.now() - pd.Timedelta(days=days)

    return df[
        (df["Balance"] > 0) &
        (df["DueDate"] < cutoff)
    ]