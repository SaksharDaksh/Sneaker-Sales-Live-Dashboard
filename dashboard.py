"""
Live Sales Analytics Dashboard
Reads KPI data from your FastAPI backend and auto-refreshes every few seconds.

Run:
1. uvicorn main:app --reload
2. python generator.py
3. streamlit run dashboard.py
"""

import os
import requests
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

# --------------------------------
# Configuration
# --------------------------------
API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")
REFRESH_SECONDS = 5

st.set_page_config(
    page_title="Live Retail Sales Analytics",
    page_icon="👟",
    layout="wide"
)

# Automatically rerun every 5 seconds
st_autorefresh(interval=REFRESH_SECONDS * 1000, key="sales_refresh")

# --------------------------------
# Custom CSS
# --------------------------------
st.markdown("""
<style>

.stApp{
    background-color:#0E1117;
}

[data-testid="stMetric"]{
    background:#1B263B;
    border:1px solid #2E4057;
    border-radius:15px;
    padding:20px;
    box-shadow:0 4px 15px rgba(0,0,0,.25);
}

[data-testid="stMetricLabel"]{
    color:#A5B4FC;
    font-size:16px;
}

[data-testid="stMetricValue"]{
    color:white;
    font-size:32px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# Title
# --------------------------------
st.title("👟 Live Retail Sales Analytics")
st.caption("Clothing & Sneakers Brand — Real-Time Dashboard")

# --------------------------------
# Helper Function
# --------------------------------
def fetch(endpoint):
    try:
        r = requests.get(f"{API_URL}{endpoint}", timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException:
        return None

# --------------------------------
# Fetch Data
# --------------------------------
revenue_data = fetch("/kpi/revenue")
top_products = fetch("/kpi/top-products")
by_region = fetch("/kpi/by-region")
by_category = fetch("/kpi/by-category")
trend = fetch("/kpi/trend")

if revenue_data is None:

    st.error("⚠ Unable to connect to FastAPI backend.")

else:

    # ---------------- KPI ----------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "$ Total Revenue",
        f"₹{revenue_data['total_revenue']:,.0f}"
    )

    if top_products:
        col2.metric(
            "🔝 Top Product",
            top_products[0]["product"]
        )

    if by_region:
        col3.metric(
            "⚲ Top Region",
            by_region[0]["region"]
        )

    st.divider()

    # ---------------- Row 1 ----------------

    left, right = st.columns(2)

    with left:

        st.subheader("Top 5 Products")

        if top_products:

            df = pd.DataFrame(top_products)

            fig = px.bar(
                df,
                x="product",
                y="revenue",
                color="revenue",
                color_continuous_scale="Blues",
                text="revenue"
            )

            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor="#0E1117",
                paper_bgcolor="#0E1117",
                coloraxis_showscale=False,
                height=420
            )

            fig.update_traces(
                texttemplate="₹%{y:,.0f}",
                textposition="outside"
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                key="top_products"
            )

    with right:

        st.subheader("Revenue by Region")

        if by_region:

            df = pd.DataFrame(by_region)

            fig = px.bar(
                df,
                x="region",
                y="revenue",
                color="revenue",
                color_continuous_scale="Viridis",
                text="revenue"
            )

            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor="#0E1117",
                paper_bgcolor="#0E1117",
                coloraxis_showscale=False,
                height=420
            )

            fig.update_traces(
                texttemplate="₹%{y:,.0f}",
                textposition="outside"
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                key="region_chart"
            )

    # ---------------- Row 2 ----------------

    left, right = st.columns(2)

    with left:

        st.subheader("Revenue by Category")

        if by_category:

            df = pd.DataFrame(by_category)

            fig = px.bar(
                df,
                x="category",
                y="revenue",
                color="category",
                text="revenue",
                color_discrete_sequence=[
                    "#3B82F6",
                    "#10B981",
                    "#F59E0B",
                    "#EF4444",
                    "#8B5CF6"
                ]
            )

            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor="#0E1117",
                paper_bgcolor="#0E1117",
                showlegend=False,
                height=420
            )

            fig.update_traces(
                texttemplate="₹%{y:,.0f}",
                textposition="outside"
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                key="category_chart"
            )

    with right:

        st.subheader("Revenue Trend")

        if trend:

            df = pd.DataFrame(trend)

            fig = go.Figure()

            fig.add_trace(
                go.Scatter(
                    x=df["minute"],
                    y=df["revenue"],
                    mode="lines+markers",
                    line=dict(
                        color="#00BFFF",
                        width=3
                    ),
                    fill="tozeroy",
                    fillcolor="rgba(0,191,255,0.15)"
                )
            )

            fig.update_layout(
                template="plotly_dark",
                plot_bgcolor="#0E1117",
                paper_bgcolor="#0E1117",
                height=420,
                hovermode="x unified",
                xaxis_title="Time",
                yaxis_title="Revenue"
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                key="trend_chart"
            )

st.caption(f"🔄 Refreshing every {REFRESH_SECONDS} seconds")
