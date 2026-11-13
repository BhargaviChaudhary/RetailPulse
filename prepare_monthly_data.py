
import pandas as pd

print("\n========== RETAILPULSE MONTHLY DATA PREPARATION ==========")

# Load cleaned transaction data
retail_data = pd.read_csv(
    "data/cleaned_sales_data.csv",
    parse_dates=["InvoiceDate"],
    dtype={"Invoice": "string"},
    low_memory=False
)

# Create monthly period
retail_data["Month"] = retail_data["InvoiceDate"].dt.to_period("M")

# Aggregate transaction data by month
monthly_data = (
    retail_data.groupby("Month")
    .agg(
        Revenue=("TotalSales", "sum"),
        Orders=("Invoice", "nunique"),
        UnitsSold=("Quantity", "sum")
    )
    .reset_index()
)

# Identify incomplete final month
latest_date = retail_data["InvoiceDate"].max()
latest_month = latest_date.to_period("M")

monthly_data["IsCompleteMonth"] = (
    monthly_data["Month"] != latest_month
) | (
    latest_date.day == latest_date.days_in_month
)

# Convert month to a readable date
monthly_data["Month"] = (
    monthly_data["Month"].dt.to_timestamp()
)

# Round revenue
monthly_data["Revenue"] = monthly_data["Revenue"].round(2)

# Save monthly dataset
monthly_data.to_csv(
    "data/monthly_sales.csv",
    index=False
)

print("\nMonthly dataset created successfully!")

print("\nTotal months:", len(monthly_data))
print("Complete months:", monthly_data["IsCompleteMonth"].sum())
print("Incomplete months:", (~monthly_data["IsCompleteMonth"]).sum())

print("\nMonthly sales preview:")
print(monthly_data.head())

print("\nLast 5 months:")
print(monthly_data.tail())

print("\nTotal monthly revenue:",
      round(monthly_data["Revenue"].sum(), 2))

print("\nSaved file: data/monthly_sales.csv")
print("\n========== TASK 1 COMPLETED ==========")
