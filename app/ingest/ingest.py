import pandas as pd

def normalize_invoices(raw):
    rows = raw["QueryResponse"].get("Invoice", [])
    df = pd.DataFrame(rows)

    return df[[
        "Id",
        "TotalAmt",
        "Balance",
        "DueDate"
    ]]

def clean_company_info(raw):
    info = raw["QueryResponse"].get("CompanyInfo", [])
    return pd.DataFrame([{
        "CompanyName": info[0]["CompanyName"],
    }])