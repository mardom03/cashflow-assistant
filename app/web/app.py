from flask import Flask
import pandas as pd
from app.analyze.cash_leaks import overdue_invoices

def create_app():
    app = Flask(__name__)

    @app.route("/")
    def dashboard():
        overdue = overdue_invoices(pd.read_sql("SELECT * FROM invoices", "sqlite:///db/app.db"))
        company_name = pd.read_sql("SELECT CompanyName FROM company_info LIMIT 1", "sqlite:///db/app.db").iloc[0, 0]
        total = overdue["Balance"].sum()

        return (
            f"<h1>${total:,.2f} overdue (30+ days) for {company_name}</h1>" + overdue.to_html()
        )
    
    return app