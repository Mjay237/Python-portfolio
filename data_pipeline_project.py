"""
End-to-End Data Pipeline: Scrape -> Clean -> Analyze -> Report
----------------------------------------------------------------
A portfolio project demonstrating a complete real-world data workflow:
1. SCRAPE: Pull data from a website
2. CLEAN: Fix formatting issues and remove bad records
3. ANALYZE: Generate summary statistics
4. REPORT: Export a polished summary report + chart

This is the kind of end-to-end project clients pay for when they want
"the whole job done" rather than just one isolated step.

Run this in Google Colab: colab.research.google.com
Paste the whole file into a cell and run it.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import time
from datetime import datetime

# ===========================================================
# STAGE 1: SCRAPE
# ===========================================================
print("STAGE 1: Scraping data...")

BASE_URL = "http://quotes.toscrape.com/page/{}/"
HEADERS = {"User-Agent": "Mozilla/5.0 (portfolio project pipeline)"}

raw_records = []
page = 1
while True:
    response = requests.get(BASE_URL.format(page), headers=HEADERS)
    if response.status_code != 200:
        break

    soup = BeautifulSoup(response.text, "html.parser")
    quote_blocks = soup.find_all("div", class_="quote")
    if not quote_blocks:
        break

    for block in quote_blocks:
        text = block.find("span", class_="text").get_text(strip=True)
        author = block.find("small", class_="author").get_text(strip=True)
        tags = [t.get_text(strip=True) for t in block.find_all("a", class_="tag")]

        raw_records.append({
            "Quote": text,
            "Author": "  " + author + "  ",   # intentionally messy spacing
            "Tags": ", ".join(tags) if tags else None,
            "Length": None  # will calculate during cleaning stage
        })

    page += 1
    time.sleep(1)

print(f"Scraped {len(raw_records)} raw records across {page - 1} pages.\n")

df = pd.DataFrame(raw_records)

# ===========================================================
# STAGE 2: CLEAN
# ===========================================================
print("STAGE 2: Cleaning data...")

rows_before = len(df)

# Fix messy whitespace in Author names
df["Author"] = df["Author"].str.strip()

# Fill missing tags with a placeholder instead of leaving blank
df["Tags"] = df["Tags"].fillna("Untagged")

# Calculate quote length (a derived/cleaned field)
df["Length"] = df["Quote"].str.len()

# Remove any accidental exact duplicates
df = df.drop_duplicates(subset=["Quote", "Author"]).reset_index(drop=True)

rows_after = len(df)
print(f"Cleaned {rows_before} records -> {rows_after} records after dedup.\n")

# ===========================================================
# STAGE 3: ANALYZE
# ===========================================================
print("STAGE 3: Analyzing data...")

top_authors = df["Author"].value_counts().head(5)
avg_length = df["Length"].mean()
longest_quote = df.loc[df["Length"].idxmax(), ["Quote", "Author"]]

print(f"Top 5 authors by quote count:\n{top_authors}\n")
print(f"Average quote length: {avg_length:.1f} characters")
print(f"Longest quote is by {longest_quote['Author']} ({df['Length'].max()} chars)\n")

# ===========================================================
# STAGE 4: REPORT
# ===========================================================
print("STAGE 4: Generating report...")

# Chart: top authors
plt.figure(figsize=(6, 4))
top_authors.plot(kind="barh", color="darkorange")
plt.title("Top 5 Authors by Quote Count")
plt.xlabel("Number of Quotes")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("top_authors_chart.png")
plt.show()

# Export cleaned dataset
df.to_csv("cleaned_quotes_dataset.csv", index=False)

# Generate a simple text summary report (the client-facing deliverable)
report_lines = [
    "DATA PIPELINE SUMMARY REPORT",
    "=" * 40,
    f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
    "",
    f"Total records scraped: {rows_before}",
    f"Total records after cleaning: {rows_after}",
    f"Average quote length: {avg_length:.1f} characters",
    "",
    "Top 5 Authors:",
]
for author, count in top_authors.items():
    report_lines.append(f"  - {author}: {count} quotes")

report_lines += [
    "",
    "Files delivered:",
    "  - cleaned_quotes_dataset.csv (full cleaned dataset)",
    "  - top_authors_chart.png (visualization)",
    "  - summary_report.txt (this report)",
]

with open("summary_report.txt", "w") as f:
    f.write("\n".join(report_lines))

print("\nPipeline complete. Files generated:")
print("  - cleaned_quotes_dataset.csv")
print("  - top_authors_chart.png")
print("  - summary_report.txt")

# ===========================================================
# NOTE FOR REAL CLIENT PROJECTS:
# - This same pattern (scrape -> clean -> analyze -> report) applies to
#   almost any client request: product prices, real estate listings,
#   job postings, review data, etc.
# - For paid gigs, wrap each stage in try/except and add logging so
#   errors are easy to diagnose if a website's structure changes.
# ===========================================================
