## cashflow-assistant
This app pulls QuickBooks data and automatically flags **overdue cash** so operators see cashflow problems before they happen. It ingests invoice data from QuickBooks, identifies invoices overdue 30+ days, calculates total overdue exposure, and displays results in a simple web dashboard.

Most small and mid-sized businesses lose money because billing lags operations, overdue invoices aren't actually monitored, and problems are discovered too late. This tool surfaces those problems automatically.

Run it by running the following commands to create a virtual environment, install requirements, and run the app.
```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```
The application shows sample data at first. To show data from your own QuickBooks account, fill out .env with your own keys and redirect URI, then go to the following link to receive your authorization code and realm ID and put those in .env as well.
```
https://appcenter.intuit.com/connect/oauth2?
client_id=YOUR_CLIENT_ID
&response_type=code
&scope=com.intuit.quickbooks.accounting%20openid%20profile%20email
&redirect_uri=YOUR_REDIRECT_URI
&state=123
```
Then, simply run the app from the entry point.
```
python run.py
```
Open http://127.0.0.1:5000 in your web browser and voilà.

The structure is as follows:
- **integrations/** - external systems (QuickBooks)
- **ingest/** - data cleanup and persistence
- **analyze/** - business rules (what counts as overdue) and email function
- **web/** - Flash UI

Notes:
- Uses QuickBooks sandbox data
- Designed as an internal tool, not SaaS
- Easy to extend with alerts or reports