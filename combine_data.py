
import pandas as pd

# Excel dataset location
file_path = "data/extracted/online_retail_II.xlsx"

# Read both sheets
year_2009 = pd.read_excel(
    file_path,
    sheet_name="Year 2009-2010"
)

year_2010 = pd.read_excel(
    file_path,
    sheet_name="Year 2010-2011"
)

# Combine both datasets
retail_data = pd.concat(
    [year_2009, year_2010],
    ignore_index=True
)

# Display results
print("\n========== COMBINED RETAIL DATA ==========")

print("Total rows and columns:", retail_data.shape)

print("\nFirst 5 records:")
print(retail_data.head())

print("\nLast 5 records:")
print(retail_data.tail())

print("\nMissing values:")
print(retail_data.isnull().sum())

print("\nDate range:")
print("Start:", retail_data["InvoiceDate"].min())
print("End:", retail_data["InvoiceDate"].max())

# Save combined dataset
retail_data.to_csv(
    "data/retail_data.csv",
    index=False
)

print("\nCombined dataset saved successfully!")
