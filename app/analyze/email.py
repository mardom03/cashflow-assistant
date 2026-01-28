import smtplib
def send_summary(overdue_total):
    if overdue_total <= 0:
        return
    
    message = f"Subject: Cashflow Alert\n\nOverdue invoices total: ${overdue_total:.2f}"
    server = smtplib.SMTP("localhost")
    server.sendmail("system@company.com", "martindomaradzki03@gmail.com", message)