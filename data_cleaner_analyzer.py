"""
Sales Data Cleaner & Analyzer
------------------------------
A portfolio project demonstrating real-world data cleaning skills:
- Handling missing values
- Fixing inconsistent formatting (dates, text case, currency symbols)
- Removing duplicates
- Generating summary statistics
- Producing a simple chart

Run this in Google Colab: colab.research.google.com
Just paste this whole file into a new notebook cell and run it.
"""

import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

# ---------------------------------------------------------
# STEP 1: Sample "messy" data (pretend this came from a client)
# In a real gig, you'd load this with: pd.read_csv("client_file.csv")
# ---------------------------------------------------------
messy_csv = """Date,Product,Region,Sales,Rep
2024-01-05, laptop , North,  1200 , John
01/06/2024,Laptop,south, 950,Mary
2024-01-07,PHONE,North,$300,John
2024-01-07,Phone,North,$300,John
,Tablet,East,450,
2024-01-09,laptop,West,1100,Sarah
2024-01-10,phone,south,N/A,Mary
"""

df = pd.read_csv(StringIO(messy_csv))

print("=== RAW DATA (messy) ===")
print(df)
print(f"\nRows before cleaning: {len(df)}")

# ---------------------------------------------------------
# STEP 2: Clean the data
# ---------------------------------------------------------

# Strip whitespace from text columns
for col in ["Product", "Region", "Rep"]:
    df[col] = df[col].astype(str).str.strip()

# Standardize text case (Title Case for names/products)
df["Product"] = df["Product"].str.title()
df["Region"] = df["Region"].str.title()

# Clean the Sales column: remove $ signs, spaces, convert "N/A" to NaN
df["Sales"] = (
    df["Sales"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.strip()
    .replace("N/A", pd.NA)
)
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")

# Drop rows with missing Date or Sales (can't analyze those reliably)
df = df.dropna(subset=["Date", "Sales"])

# Standardize dates (handles mixed formats like "2024-01-05" and "01/06/2024")
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])

# Remove exact duplicate rows
df = df.drop_duplicates()

# Reset index after cleaning
df = df.reset_index(drop=True)

print("\n=== CLEANED DATA ===")
print(df)
print(f"\nRows after cleaning: {len(df)}")

# ---------------------------------------------------------
# STEP 3: Analysis — summary stats
# ---------------------------------------------------------
print("\n=== SUMMARY STATS ===")
print(f"Total Sales: ${df['Sales'].sum():,.2f}")
print(f"Average Sale: ${df['Sales'].mean():,.2f}")
print(f"Top Product by Sales:\n{df.groupby('Product')['Sales'].sum().sort_values(ascending=False)}")
print(f"\nSales by Region:\n{df.groupby('Region')['Sales'].sum().sort_values(ascending=False)}")

# ---------------------------------------------------------
# STEP 4: Simple chart
# ---------------------------------------------------------
sales_by_product = df.groupby("Product")["Sales"].sum().sort_values(ascending=False)

plt.figure(figsize=(6, 4))
sales_by_product.plot(kind="bar", color="steelblue")
plt.title("Total Sales by Product")
plt.ylabel("Sales ($)")
plt.xlabel("Product")
plt.tight_layout()
plt.savefig("sales_by_product.png")
plt.show()

print("\nChart saved as sales_by_product.png")

# ---------------------------------------------------------
# STEP 5: Export cleaned data (this is the deliverable a client pays for)
# ---------------------------------------------------------
df.to_csv("cleaned_sales_data.csv", index=False)
print("\nCleaned data exported to cleaned_sales_data.csv")
