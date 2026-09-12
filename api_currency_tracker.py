"""
API Data Fetcher — Currency Exchange Rate Tracker
----------------------------------------------------
A portfolio project demonstrating API integration skills:
- Fetching live data from a public API (no key required)
- Parsing JSON responses
- Structuring API data into a usable format
- Tracking changes over multiple currencies
- Producing a simple visual report

Why this matters for clients: not all data lives on websites you scrape —
many services offer APIs instead. Knowing how to pull, clean, and present
API data is a separate, highly requested skill (e.g. "connect to our
payment provider's API and summarize daily transactions").

API used: exchangerate-api (free, open, no signup needed)
Run this in Google Colab: colab.research.google.com
"""

import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ===========================================================
# STEP 1: Fetch live data from the API
# ===========================================================
print("STEP 1: Fetching live exchange rate data...")

BASE_CURRENCY = "USD"
API_URL = f"https://open.er-api.com/v6/latest/{BASE_CURRENCY}"

response = requests.get(API_URL)
data = response.json()

if data.get("result") != "success":
    raise Exception("API request failed. Try again in a moment.")

rates = data["rates"]
last_updated = data["time_last_update_utc"]

print(f"Data last updated: {last_updated}")
print(f"Base currency: {BASE_CURRENCY}\n")

# ===========================================================
# STEP 2: Select currencies relevant to the client
# (In a real gig, the client tells you exactly which ones they need)
# ===========================================================
currencies_of_interest = ["NGN", "GBP", "EUR", "CAD", "ZAR", "GHS", "KES", "INR"]

selected_rates = {
    currency: rates[currency]
    for currency in currencies_of_interest
    if currency in rates
}

df = pd.DataFrame(
    list(selected_rates.items()),
    columns=["Currency", f"Rate (per 1 {BASE_CURRENCY})"]
)

print("STEP 2: Selected currencies:")
print(df.to_string(index=False))
print()

# ===========================================================
# STEP 3: Calculate a derived column
# (Example: how much local currency for a common freelance payment)
# ===========================================================
print("STEP 3: Calculating example conversions...")

SAMPLE_AMOUNT = 50  # e.g. a $50 gig payment
df["Value of $50"] = (df[f"Rate (per 1 {BASE_CURRENCY})"] * SAMPLE_AMOUNT).round(2)

print(df.to_string(index=False))
print()

# ===========================================================
# STEP 4: Visualize
# ===========================================================
print("STEP 4: Generating chart...")

plt.figure(figsize=(7, 4))
plt.bar(df["Currency"], df["Value of $50"], color="seagreen")
plt.title(f"Value of $50 USD Across Currencies ({datetime.now().strftime('%Y-%m-%d')})")
plt.ylabel("Local Currency Value")
plt.xlabel("Currency")
plt.tight_layout()
plt.savefig("currency_comparison_chart.png")
plt.show()

# ===========================================================
# STEP 5: Export the report
# ===========================================================
df.to_csv("exchange_rate_report.csv", index=False)
print("\nReport exported to exchange_rate_report.csv")
print("Chart saved to currency_comparison_chart.png")

# ===========================================================
# NOTE FOR REAL CLIENT GIGS:
# - Many APIs require a free API key (weather, stock data, social media).
#   The pattern is the same: fetch -> parse JSON -> structure -> report.
# - Always check API rate limits so you don't get temporarily blocked
#   from making requests.
# - Wrap requests in try/except for production use, since APIs can
#   go down or return errors.
# ===========================================================
