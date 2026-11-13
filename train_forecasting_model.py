
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import joblib

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

print("\n========== RETAILPULSE SALES FORECASTING ==========")

# ------------------------------------------
# 1. LOAD MONTHLY SALES DATA
# ------------------------------------------

data = pd.read_csv(
    "data/monthly_sales.csv",
    parse_dates=["Month"]
)

# Use only complete months
data = data[data["IsCompleteMonth"] == True].copy()
data = data.sort_values("Month").reset_index(drop=True)

print("\nComplete months available:", len(data))

# ------------------------------------------
# 2. FEATURE ENGINEERING
# ------------------------------------------

data["MonthNumber"] = data["Month"].dt.month

data["Revenue_Lag_1"] = data["Revenue"].shift(1)
data["Revenue_Lag_2"] = data["Revenue"].shift(2)
data["Revenue_Lag_3"] = data["Revenue"].shift(3)

# Remove rows without previous-month information
data = data.dropna().reset_index(drop=True)

features = [
    "MonthNumber",
    "Revenue_Lag_1",
    "Revenue_Lag_2",
    "Revenue_Lag_3"
]

X = data[features]
y = data["Revenue"]

# ------------------------------------------
# 3. CHRONOLOGICAL TRAIN-TEST SPLIT
# ------------------------------------------

split_index = int(len(data) * 0.80)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))

# ------------------------------------------
# 4. TRAIN MACHINE LEARNING MODELS
# ------------------------------------------

models = {
    "Linear Regression": LinearRegression(),

    "Random Forest": RandomForestRegressor(
        n_estimators=200,
        max_depth=4,
        random_state=42
    )
}

results = []
predictions = {}

for name, model in models.items():

    model.fit(X_train, y_train)

    predicted = model.predict(X_test)

    mae = mean_absolute_error(y_test, predicted)

    rmse = np.sqrt(mean_squared_error(y_test, predicted))

    r2 = r2_score(y_test, predicted)

    results.append({
        "Model": name,
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "R2 Score": round(r2, 4)
    })

    predictions[name] = predicted

    print(f"\n{name}")
    print("MAE:", round(mae, 2))
    print("RMSE:", round(rmse, 2))
    print("R2 Score:", round(r2, 4))


# ------------------------------------------
# 5. COMPARE MODELS
# ------------------------------------------

results_df = pd.DataFrame(results)

results_df = results_df.sort_values("MAE")

print("\n========== MODEL COMPARISON ==========")
print(results_df.to_string(index=False))

os.makedirs("outputs", exist_ok=True)

results_df.to_csv(
    "outputs/model_comparison.csv",
    index=False
)

# ------------------------------------------
# 6. SELECT BEST MODEL
# ------------------------------------------

best_model_name = results_df.iloc[0]["Model"]

print("\nBest model based on test MAE:", best_model_name)

best_model = models[best_model_name]

# ------------------------------------------
# 7. REFIT BEST MODEL ON ALL AVAILABLE DATA
# ------------------------------------------

best_model.fit(X, y)

# Save trained model
joblib.dump(
    best_model,
    "outputs/best_sales_model.pkl"
)

print("\nBest model saved successfully!")

# ------------------------------------------
# 8. FORECAST NEXT 3 MONTHS
# ------------------------------------------

revenue_history = data["Revenue"].tolist()

last_month = data["Month"].max()

future_forecasts = []

for i in range(1, 4):

    future_month = last_month + pd.DateOffset(months=i)

    input_data = pd.DataFrame([{
        "MonthNumber": future_month.month,
        "Revenue_Lag_1": revenue_history[-1],
        "Revenue_Lag_2": revenue_history[-2],
        "Revenue_Lag_3": revenue_history[-3]
    }])

    predicted_revenue = best_model.predict(input_data)[0]

    predicted_revenue = max(0, predicted_revenue)

    future_forecasts.append({
        "Month": future_month,
        "PredictedRevenue": round(predicted_revenue, 2)
    })

    revenue_history.append(predicted_revenue)


forecast_df = pd.DataFrame(future_forecasts)

forecast_df.to_csv(
    "outputs/future_sales_forecast.csv",
    index=False
)

print("\n========== NEXT 3 MONTHS SALES FORECAST ==========")
print(forecast_df.to_string(index=False))

# ------------------------------------------
# 9. SAVE TEST PREDICTIONS
# ------------------------------------------

test_results = pd.DataFrame({
    "Month": data["Month"].iloc[split_index:].values,
    "ActualRevenue": y_test.values,
    "PredictedRevenue": predictions[best_model_name]
})

test_results.to_csv(
    "outputs/test_predictions.csv",
    index=False
)

# ------------------------------------------
# 10. PLOT MODEL COMPARISON
# ------------------------------------------

plt.figure(figsize=(9, 5))

plt.bar(
    results_df["Model"],
    results_df["MAE"]
)

plt.title("Sales Forecasting Model Comparison")
plt.xlabel("Machine Learning Model")
plt.ylabel("Mean Absolute Error (£)")

plt.tight_layout()

plt.savefig(
    "outputs/model_comparison.png",
    dpi=300
)

plt.show()
plt.close()

# ------------------------------------------
# 11. PLOT FUTURE FORECAST
# ------------------------------------------

plt.figure(figsize=(10, 5))

plt.plot(
    data["Month"].iloc[-6:],
    data["Revenue"].iloc[-6:],
    marker="o",
    label="Historical Revenue"
)

plt.plot(
    forecast_df["Month"],
    forecast_df["PredictedRevenue"],
    marker="o",
    linestyle="--",
    label="Predicted Revenue"
)

plt.title("RetailPulse - Future Sales Forecast")
plt.xlabel("Month")
plt.ylabel("Revenue (£)")
plt.legend()

plt.tight_layout()

plt.savefig(
    "outputs/future_sales_forecast.png",
    dpi=300
)

plt.show()
plt.close()

print("\n========== FORECASTING COMPLETED ==========")
print("Model comparison saved.")
print("Test predictions saved.")
print("Future forecasts saved.")
print("Trained model saved.")
print("\n========== RETAILPULSE ML SUCCESS ==========")
