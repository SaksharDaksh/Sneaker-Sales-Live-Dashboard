"""
Live Sales Analytics Dashboard
Reads KPI data from your FastAPI backend and auto-refreshes every few seconds.

Usage:
    1. Make sure your API is running:        uvicorn main:app --reload
    2. Make sure the generator is running:   python generator.py
    3. Then run this dashboard:              streamlit run dashboard.py
"""

import streamlit as st
import requests
import pandas as pd
import time

API_URL = "http://127.0.0.1:8000"
REFRESH_SECONDS = 5

st.set_page_config(page_title="Live Sales Analytics", layout="wide")

st.title("👟 Live Retail Sales Analytics")
st.caption("Clothing & Sneakers Brand — Real-Time Dashboard")

# A placeholder container we can keep overwriting every refresh cycle,
# instead of stacking new charts below old ones each time.
placeholder = st.empty()


def fetch(endpoint: str):
    """Small helper to call the API and handle errors gracefully."""
    try:
        response = requests.get(f"{API_URL}{endpoint}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None


while True:
    revenue_data = fetch("/kpi/revenue")
    top_products = fetch("/kpi/top-products")
    by_region = fetch("/kpi/by-region")
    by_category = fetch("/kpi/by-category")
    trend = fetch("/kpi/trend")

    with placeholder.container():
        if revenue_data is None:
            st.error("⚠️ Can't reach the API. Is 'uvicorn main:app --reload' running?")
        else:
            # ── Top KPI cards ──────────────────────────────
            col1, col2, col3 = st.columns(3)
            col1.metric("💰 Total Revenue", f"₹{revenue_data['total_revenue']:,.0f}")

            if top_products:
                col2.metric("🏆 Top Product", top_products[0]["product"])
            if by_region:
                col3.metric("📍 Top Region", by_region[0]["region"])

            st.divider()

            # ── Charts row ──────────────────────────────────
            chart_col1, chart_col2 = st.columns(2)

            with chart_col1:
                st.subheader("Top 5 Products by Revenue")
                if top_products:
                    df = pd.DataFrame(top_products)
                    st.bar_chart(df.set_index("product")["revenue"])
                else:
                    st.info("No sales data yet.")

            with chart_col2:
                st.subheader("Revenue by Region")
                if by_region:
                    df = pd.DataFrame(by_region)
                    st.bar_chart(df.set_index("region")["revenue"])
                else:
                    st.info("No sales data yet.")

            chart_col3, chart_col4 = st.columns(2)

            with chart_col3:
                st.subheader("Revenue by Category")
                if by_category:
                    df = pd.DataFrame(by_category)
                    st.bar_chart(df.set_index("category")["revenue"])
                else:
                    st.info("No sales data yet.")

            with chart_col4:
                st.subheader("Revenue Trend (per minute)")
                if trend:
                    df = pd.DataFrame(trend)
                    st.line_chart(df.set_index("minute")["revenue"])
                else:
                    st.info("No sales data yet.")

            st.caption(f"Auto-refreshing every {REFRESH_SECONDS} seconds...")

    time.sleep(REFRESH_SECONDS)
