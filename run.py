from app.integrations.queries import get_invoices
from app.integrations.queries import get_company_info
from app.integrations.client import ensure_tokens
from app.ingest.ingest import normalize_invoices
from app.ingest.ingest import clean_company_info
from app.ingest.save import save_dataframe
from app.web.app import create_app

def ingest():
    raw_invoices = get_invoices()
    df_invoices = normalize_invoices(raw_invoices)
    save_dataframe(df_invoices, "invoices")
    print(f"Ingested {len(df_invoices)} invoices.")
    raw_company_info = get_company_info()
    df_company_info = clean_company_info(raw_company_info)
    save_dataframe(df_company_info, "company_info")

def run_server():
    app = create_app()
    app.run(debug=True)

if __name__ == "__main__":
    try:
        ensure_tokens()
        ingest()
    except Exception as e:
        print(f"Showing sample database. Error during ingestion: {e}")
    run_server()