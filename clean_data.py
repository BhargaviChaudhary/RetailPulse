
import pandas as pd

# Load original dataset
retail_data = pd.read_csv(
    "data/retail_data.csv",
    parse_dates=["InvoiceDate"],
    dtype={
        "Invoice": "string",
        "StockCode": "string"
    }
)

print("\n========== RETAILPULSE DATA CLEANING ==========")

original_count = len(retail_data)
print("\nOriginal records:", original_count)

# Step 1: Remove exact duplicate rows
retail_data = retail_data.drop_duplicates().copy()

duplicates_removed = original_count - len(retail_data)
print("Exact duplicates removed:", duplicates_removed)

# Step 2: Identify cancelled invoices
cancelled = retail_data["Invoice"].str.startswith("C", na=False)
print("Cancelled invoice records:", cancelled.sum())

# Step 3: Keep only valid sales records
sales_data = retail_data[
    (~cancelled) &
    (retail_data["Quantity"] > 0) &
    (retail_data["Price"] > 0)
].copy()

# Step 4: Calculate total sales
sales_data["TotalSales"] = (
    sales_data["Quantity"] * sales_data["Price"]
)

# Step 5: Save cleaned dataset
sales_data.to_csv(
    "data/cleaned_sales_data.csv",
    index=False
)

# Step 6: Display results
print("\n========== CLEANING RESULTS ==========")
print("Original records:", original_count)
print("Duplicates removed:", duplicates_removed)
print("Cleaned sales records:", len(sales_data))
print("Records excluded:", len(retail_data) - len(sales_data))

print("\nRemaining missing values:")
print(sales_data.isnull().sum())

print("\nFirst 5 cleaned records:")
print(sales_data.head())

print("\nTotal sales amount:",
      round(sales_data["TotalSales"].sum(), 2))

print("\nCleaned dataset saved successfully!")
