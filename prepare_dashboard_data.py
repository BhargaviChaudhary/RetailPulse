
import pandas as pd
import os

print("\n========== RETAILPULSE DASHBOARD DATA PREPARATION ==========")

os.makedirs("outputs", exist_ok=True)

# Load monthly data
monthly = pd.read_csv(
    "data/monthly_sales.csv",
    parse_dates=["Month"]
)

monthly = monthly[
    monthly["IsCompleteMonth"] == True
].copy()

number_of_months = len(monthly)
latest_month = monthly["Month"].max()

# Load cleaned sales data locally
retail = pd.read_csv(
    "data/cleaned_sales_data.csv",
    parse_dates=["InvoiceDate"],
    low_memory=False
)

# Keep only complete months
retail = retail[
    retail["InvoiceDate"] <
    (latest_month + pd.DateOffset(months=1))
].copy()

# 1. Country revenue summary
country_data = (
    retail.groupby("Country")["TotalSales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

country_data.to_csv(
    "outputs/dashboard_country_revenue.csv",
    index=False
)

# 2. Product demand summary
product_data = (
    retail.groupby("Description")
    .agg(
        TotalUnitsSold=("Quantity", "sum"),
        Revenue=("TotalSales", "sum")
    )
    .reset_index()
)

product_data["AverageMonthlyDemand"] = (
    product_data["TotalUnitsSold"] / number_of_months
)

product_data["Estimated21DayDemand"] = (
    product_data["AverageMonthlyDemand"] / 30 * 21
).round(0).astype(int)

product_data = product_data.sort_values(
    "TotalUnitsSold",
    ascending=False
)

product_data.to_csv(
    "outputs/dashboard_product_demand.csv",
    index=False
)

print("\nDashboard summary files created successfully!")

print("Countries:", len(country_data))
print("Products:", len(product_data))
print("Complete months:", number_of_months)

print("\nTop 5 products:")
print(product_data.head())

print("\nSaved files:")
print("outputs/dashboard_country_revenue.csv")
print("outputs/dashboard_product_demand.csv")

print("\n========== TASK COMPLETED ==========")
