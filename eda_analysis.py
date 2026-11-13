
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ==========================================
# RETAILPULSE - EXPLORATORY DATA ANALYSIS
# ==========================================

# Load cleaned dataset
retail_data = pd.read_csv(
    "data/cleaned_sales_data.csv",
    parse_dates=["InvoiceDate"],
    dtype={"Invoice": "string"},
    low_memory=False
)

# Create folder for graphs
os.makedirs("charts", exist_ok=True)

# Set graph style
sns.set_theme(style="whitegrid", palette="deep")

print("\n========== RETAILPULSE EDA ==========")

print("\nDataset shape:", retail_data.shape)

# ==========================================
# 1. MONTHLY REVENUE ANALYSIS
# ==========================================

retail_data["Month"] = (
    retail_data["InvoiceDate"].dt.to_period("M")
)

monthly_revenue = (
    retail_data.groupby("Month")["TotalSales"]
    .sum()
)

monthly_revenue.index = monthly_revenue.index.to_timestamp()

print("\nMONTHLY REVENUE (£):")
print(monthly_revenue.round(2))

plt.figure(figsize=(12, 6))

sns.lineplot(
    x=monthly_revenue.index,
    y=monthly_revenue.values,
    marker="o"
)

plt.title("Monthly Revenue Trend", fontsize=15)
plt.xlabel("Month")
plt.ylabel("Revenue (£)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("charts/monthly_revenue.png", dpi=300)
plt.show()
plt.close()


# ==========================================
# 2. TOP 10 BEST-SELLING PRODUCTS
# ==========================================

top_products = (
    retail_data.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTOP 10 BEST-SELLING PRODUCTS:")
print(top_products)

plt.figure(figsize=(12, 7))

sns.barplot(
    x=top_products.values,
    y=top_products.index
)

plt.title("Top 10 Best-Selling Products", fontsize=15)
plt.xlabel("Quantity Sold")
plt.ylabel("Product")

plt.tight_layout()

plt.savefig("charts/top_products.png", dpi=300)
plt.show()
plt.close()


# ==========================================
# 3. TOP 10 COUNTRIES BY REVENUE
# ==========================================

country_revenue = (
    retail_data.groupby("Country")["TotalSales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\nTOP 10 COUNTRIES BY REVENUE (£):")
print(country_revenue.round(2))

plt.figure(figsize=(12, 7))

sns.barplot(
    x=country_revenue.values,
    y=country_revenue.index
)

plt.title("Top 10 Countries by Revenue", fontsize=15)
plt.xlabel("Revenue (£)")
plt.ylabel("Country")

plt.tight_layout()

plt.savefig("charts/top_countries.png", dpi=300)
plt.show()
plt.close()


# ==========================================
# 4. MONTHLY ORDER TREND
# ==========================================

monthly_orders = (
    retail_data.groupby("Month")["Invoice"]
    .nunique()
)

monthly_orders.index = monthly_orders.index.to_timestamp()

print("\nMONTHLY ORDERS:")
print(monthly_orders)

plt.figure(figsize=(12, 6))

sns.lineplot(
    x=monthly_orders.index,
    y=monthly_orders.values,
    marker="o"
)

plt.title("Monthly Order Trend", fontsize=15)
plt.xlabel("Month")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("charts/monthly_orders.png", dpi=300)
plt.show()
plt.close()


# ==========================================
# FINAL SUMMARY
# ==========================================

print("\n========== EDA COMPLETED ==========")
print("Total records analysed:", len(retail_data))
print("Total products analysed:", retail_data["Description"].nunique())
print("Total countries analysed:", retail_data["Country"].nunique())
print("Total revenue (£):", round(retail_data["TotalSales"].sum(), 2))

print("\nAll graphs saved inside the charts folder!")
