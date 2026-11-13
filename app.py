
import streamlit as st
import pandas as pd

# ==========================================
# RETAILPULSE - BUSINESS INTELLIGENCE
# ==========================================

st.set_page_config(
    page_title="RetailPulse | Business Intelligence",
    page_icon="📊",
    layout="wide"
)

st.title("📊 RetailPulse")
st.subheader("Sales Forecasting & Inventory Intelligence")
st.caption("Historical retail sales analysis | UCI Online Retail II dataset")


# ==========================================
# LOAD DASHBOARD DATA
# ==========================================

@st.cache_data
def load_data():

    monthly = pd.read_csv(
        "data/monthly_sales.csv",
        parse_dates=["Month"]
    )

    monthly = monthly[
        monthly["IsCompleteMonth"] == True
    ].copy()

    forecasts = pd.read_csv(
        "outputs/future_sales_forecast.csv",
        parse_dates=["Month"]
    )

    comparison = pd.read_csv(
        "outputs/model_comparison.csv"
    )

    predictions = pd.read_csv(
        "outputs/test_predictions.csv",
        parse_dates=["Month"]
    )

    country_data = pd.read_csv(
        "outputs/dashboard_country_revenue.csv"
    )

    product_data = pd.read_csv(
        "outputs/dashboard_product_demand.csv"
    )

    return (
        monthly,
        forecasts,
        comparison,
        predictions,
        country_data,
        product_data
    )


try:
    (
        monthly,
        forecasts,
        comparison,
        predictions,
        country_data,
        product_data
    ) = load_data()

except Exception as error:
    st.error(f"Unable to load project data: {error}")
    st.stop()


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("RetailPulse Navigation")

page = st.sidebar.radio(
    "Select Dashboard",
    [
        "Business Overview",
        "Sales Forecasting",
        "Inventory Intelligence"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "Project: RetailPulse\n\n"
    "Technology: Python, Pandas, Scikit-learn, Streamlit"
)


# ==========================================
# PAGE 1 - BUSINESS OVERVIEW
# ==========================================

if page == "Business Overview":

    st.header("Business Overview")

    total_revenue = monthly["Revenue"].sum()
    total_orders = monthly["Orders"].sum()
    total_units = monthly["UnitsSold"].sum()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Revenue",
        f"£{total_revenue:,.0f}"
    )

    col2.metric(
        "Total Orders",
        f"{total_orders:,.0f}"
    )

    col3.metric(
        "Total Units Sold",
        f"{total_units:,.0f}"
    )

    st.divider()

    st.subheader("Monthly Revenue Trend")

    st.line_chart(
        monthly.set_index("Month")[["Revenue"]]
    )

    st.subheader("Monthly Orders")

    st.bar_chart(
        monthly.set_index("Month")[["Orders"]]
    )

    st.subheader("Top 10 Countries by Revenue")

    st.dataframe(
        country_data.head(10).round(2),
        use_container_width=True,
        hide_index=True
    )


# ==========================================
# PAGE 2 - SALES FORECASTING
# ==========================================

elif page == "Sales Forecasting":

    st.header("Machine Learning Sales Forecasting")

    st.write(
        "Comparison of machine learning models "
        "and predicted future monthly revenue."
    )

    st.subheader("Model Performance")

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )

    best_model = comparison.sort_values(
        "MAE"
    ).iloc[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Selected Model",
        best_model["Model"]
    )

    col2.metric(
        "Best Model MAE",
        f"£{best_model['MAE']:,.0f}"
    )

    col3.metric(
        "R² Score",
        f"{best_model['R2 Score']:.4f}"
    )

    st.caption(
        "Evaluation uses a chronological test set of five observations. "
        "Results are preliminary because only 24 complete historical "
        "months are available."
    )

    st.divider()

    st.subheader("Actual vs Predicted Revenue")

    st.line_chart(
        predictions.set_index("Month")[
            ["ActualRevenue", "PredictedRevenue"]
        ]
    )

    st.subheader("Future Monthly Revenue Forecast")

    st.line_chart(
        forecasts.set_index("Month")[["PredictedRevenue"]]
    )

    st.dataframe(
        forecasts,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "These are historical demonstration forecasts for "
        "December 2011 to February 2012, not current sales forecasts."
    )


# ==========================================
# PAGE 3 - INVENTORY INTELLIGENCE
# ==========================================

elif page == "Inventory Intelligence":

    st.header("Inventory Intelligence")

    st.write(
        "Product demand analysis and estimated "
        "replenishment planning based on historical sales."
    )

    st.warning(
        "The source dataset does not contain actual stock levels, "
        "supplier lead times or purchase costs. These are demand "
        "estimates, not actual reorder alerts."
    )

    st.subheader("Top 10 Products by Quantity Sold")

    top_products = product_data.head(10).copy()

    st.bar_chart(
        top_products.set_index("Description")[
            ["TotalUnitsSold"]
        ]
    )

    st.subheader("Estimated Product Demand")

    display_products = top_products[
        [
            "Description",
            "TotalUnitsSold",
            "AverageMonthlyDemand",
            "Estimated21DayDemand"
        ]
    ].copy()

    display_products["AverageMonthlyDemand"] = (
        display_products["AverageMonthlyDemand"].round(0)
    )

    st.dataframe(
        display_products,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "Planning assumption: 30 days per month and 21 days "
        "of demand coverage. The 21-day figure is an illustrative "
        "planning target, not a calculated reorder quantity."
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "RetailPulse | Built with Python, Pandas, Scikit-learn and Streamlit"
)

st.caption(
    "Dataset: UCI Online Retail II | Historical data: 2009–2011"
)
