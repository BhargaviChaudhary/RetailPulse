
import pandas as pd

# Dataset location
file_path = "data/extracted/online_retail_II.xlsx"

# Read both Excel sheets
year_2009 = pd.read_excel(
    file_path,
    sheet_name="Year 2009-2010"
)

year_2010 = pd.read_excel(
    file_path,
    sheet_name="Year 2010-2011"
)

# Display basic information
print("\n========== RETAILPULSE DATASET ==========")

print("\n2009-2010 DATA:")
print(year_2009.head())

print("\n2010-2011 DATA:")
print(year_2010.head())

# Display dataset shapes
print("\n========== DATASET SIZE ==========")

print("2009-2010:", year_2009.shape)
print("2010-2011:", year_2010.shape)

# Display column names
print("\n========== COLUMN NAMES ==========")

print(year_2009.columns.tolist())

# Display dataset information
print("\n========== DATA TYPES ==========")

print(year_2009.info())


print("\n========== SECOND SHEET INFORMATION ==========")

print(year_2010.info())

print("\n========== SECOND SHEET FIRST 5 ROWS ==========")

print(year_2010.head())

print("\n========== SECOND SHEET MISSING VALUES ==========")

print(year_2010.isnull().sum())
