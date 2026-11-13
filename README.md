
# RetailPulse 📊
### Sales Forecasting & Inventory Intelligence

RetailPulse is a data-driven retail analytics project that analyzes historical sales transactions, identifies business trends, compares machine learning forecasting models, and provides product demand insights through an interactive dashboard.

## 🎯 Project Objectives

- Analyze historical retail sales data.
- Identify monthly revenue and order trends.
- Discover top-selling products and countries.
- Build machine learning models to forecast monthly revenue.
- Estimate product demand to support inventory planning.
- Present insights through an interactive Streamlit dashboard.

## 🛠️ Technologies Used

- Python
- Pandas and NumPy
- Matplotlib and Seaborn
- Scikit-learn
- Streamlit
- Jupyter / VS Code

## 📂 Project Structure

```text
RetailPulse/
│
├── data/
├── charts/
├── outputs/
│
├── explore_data.py
├── combine_data.py
├── check_data.py
├── inspect_issues.py
├── clean_data.py
├── eda_analysis.py
├── prepare_monthly_data.py
├── train_forecasting_model.py
├── app.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## 📈 Key Features

### 1. Data Cleaning
- Removed exact duplicate records.
- Excluded cancelled invoices.
- Removed non-positive quantities and prices.
- Calculated total sales for each transaction.

### 2. Exploratory Data Analysis
- Monthly revenue analysis.
- Monthly order trends.
- Top 10 best-selling products.
- Top 10 countries by revenue.

### 3. Machine Learning Forecasting
- Linear Regression.
- Random Forest Regression.
- Model comparison using MAE, RMSE and R².
- Three-month historical demonstration forecast.

### 4. Inventory Intelligence
- Product demand analysis.
- Average monthly product demand.
- Estimated 21-day demand coverage.

### 5. Interactive Dashboard
The Streamlit dashboard includes:
- Business Overview
- Sales Forecasting
- Inventory Intelligence

## 📊 Project Results

| Metric | Result |
|---|---:|
| Original records | 1,067,371 |
| Cleaned sales records | 1,007,913 |
| Products analysed | 5,399 |
| Countries analysed | 43 |
| Historical revenue | £20,476,260.45 |
| Best forecasting model | Random Forest |
| Random Forest MAE | £134,488.17 |
| Random Forest R² | 0.5863 |

## 🤖 Model Evaluation

Two machine learning models were compared:

| Model | MAE | R² |
|---|---:|---:|
| Linear Regression | £206,011.18 | 0.3073 |
| Random Forest | £134,488.17 | 0.5863 |

Random Forest achieved the lower test MAE and was selected as the final model.

**Note:** The model uses only 24 complete historical months, with five observations in the chronological test set. Performance is preliminary and should not be treated as production-level forecasting.

## 📦 Dataset

**Source:** UCI Machine Learning Repository – Online Retail II

https://archive.ics.uci.edu/dataset/502/online+retail+ii

The dataset contains historical retail transactions from December 2009 to December 2011.

## ⚠️ Important Limitations

- Forecasts are historical demonstration predictions for December 2011 to February 2012, not current sales forecasts.
- The dataset does not contain actual stock levels, supplier lead times or purchase costs.
- Inventory insights are based on historical product demand and an illustrative 21-day coverage assumption.
- The final month of December 2011 is incomplete and excluded from forecasting model training.

## 🚀 How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/BhargaviChaudhary/RetailPulse.git
cd RetailPulse
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
uv pip install -r requirements.txt
```

### 5. Download and prepare the dataset

Download Online Retail II from the UCI repository and place the extracted Excel file in the `data/extracted/` folder.

Run the project scripts in this order:

```bash
python explore_data.py
python combine_data.py
python check_data.py
python inspect_issues.py
python clean_data.py
python eda_analysis.py
python prepare_monthly_data.py
python train_forecasting_model.py
```

### 6. Launch the dashboard

```bash
streamlit run app.py
```

## 👩‍💻 Author

**Bhargavi Chaudhary**

B.Tech Computer Science and Engineering

GitHub: https://github.com/BhargaviChaudhary

---

*RetailPulse – Turning historical retail data into meaningful business insights.*
