
import pandas as pd

# Load the dataset
retail_data = pd.read_csv(
    "data/retail_data.csv",
    parse_dates=["InvoiceDate"],
    dtype={"Invoice": "string", "StockCode": "string"}
)

print("\n========== INSPECTING DATA ISSUES ==========")

# 1. Duplicate records
print("\n1. DUPLICATE RECORD EXAMPLES:")
duplicates = retail_data[
    retail_data.duplicated(keep=False)
]
print(duplicates.head(10))

# 2. Cancelled invoices
print("\n2. CANCELLED INVOICE EXAMPLES:")
cancelled = retail_data[
    retail_data["Invoice"].str.startswith("C", na=False)
]
print(cancelled.head(10))

# 3. Negative quantities
print("\n3. NEGATIVE QUANTITY EXAMPLES:")
negative_quantity = retail_data[
    retail_data["Quantity"] < 0
]
print(negative_quantity.head(10))

# 4. Zero-price records
print("\n4. ZERO-PRICE EXAMPLES:")
zero_price = retail_data[
    retail_data["Price"] == 0
]
print(zero_price.head(10))

# 5. Negative-price records
print("\n5. NEGATIVE-PRICE EXAMPLES:")
negative_price = retail_data[
    retail_data["Price"] < 0
]
print(negative_price.head(10))

print("\n========== INSPECTION COMPLETED ==========")
