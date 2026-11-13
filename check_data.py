
import pandas as pd

# Load combined retail dataset
retail_data = pd.read_csv(
    "data/retail_data.csv",
    parse_dates=["InvoiceDate"],
    dtype={"Invoice": "string", "StockCode": "string"}
)

print("\n========== RETAIL DATA QUALITY CHECK ==========")

# Total records
print("\nTotal records:", len(retail_data))

# Missing values
print("\nMissing values:")
print(retail_data.isnull().sum())

# Duplicate records
print("\nDuplicate records:")
print(retail_data.duplicated().sum())

# Cancelled invoices
cancelled = retail_data["Invoice"].str.startswith(
    "C", na=False
)

print("\nCancelled invoices:", cancelled.sum())

# Negative quantities (possible returns)
negative_quantity = retail_data["Quantity"] < 0

print("Negative quantity records:", negative_quantity.sum())

# Zero-price records
zero_price = retail_data["Price"] == 0

print("Zero price records:", zero_price.sum())

# Negative prices
negative_price = retail_data["Price"] < 0

print("Negative price records:", negative_price.sum())

print("\n========== CHECK COMPLETED ==========")
