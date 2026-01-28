from app.integrations.client import qb_request

def get_invoices():
    query = "SELECT Id, CustomerRef, TotalAmt, Balance, DueDate FROM Invoice MAXRESULTS 50"
    return qb_request(query)

def get_company_info():
    query = "SELECT * FROM CompanyInfo"
    return qb_request(query)