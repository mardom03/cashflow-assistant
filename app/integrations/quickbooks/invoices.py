from client import qb_request

def fetch_invoices():
    query = "SELECT Id, CustomerRef, TotalAmt, Balance, DueDate FROM Invoice"
    return qb_request(query)

if __name__ == "__main__":
    print(fetch_invoices())