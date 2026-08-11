# 👟 Drop Deck — Live Sneaker Sales Analytics

A full-stack, real-time sales analytics platform simulating live sneaker sales for a multi-brand retailer. Built to demonstrate an end-to-end data pipeline: live ingestion, relational storage, SQL aggregation, and a continuously refreshing dashboard.

## Overview

Drop Deck simulates a sneaker retailer's live order stream and turns it into real-time business insight. A generator script continuously "sells" sneakers across 18 SKUs and 8 brands, an API ingests and stores every transaction in MySQL, and a Streamlit dashboard auto-refreshes every 5 seconds to surface revenue, top products, regional performance, and category trends — all backed by live SQL aggregation, not static data.

## Architecture

```
[Generator Script]  →  POST /sales  →  [FastAPI Backend]  →  [MySQL Database]
  (simulates live                                                    │
   customer orders)                                                  │
                                                          [SQL aggregation:
                                                           JOIN, GROUP BY, SUM]
                                                                      │
                                                                      ▼
                                                    [Streamlit Dashboard]
                                                    Live KPIs · Plotly charts
                                                    Auto-refresh every 5s
```

## Features

- **Live order simulation** — a generator script continuously creates realistic sneaker purchases across regions, brands, and categories
- **REST API backend** (FastAPI) — ingests live sales and exposes 5 KPI aggregation endpoints
- **Relational schema** (MySQL) — `products` and `sales` tables with a proper foreign key relationship
- **Real-time dashboard** (Streamlit + Plotly) — auto-refreshes every 5 seconds, dark theme, interactive charts for revenue, top products, regional performance, category mix, and revenue trend over time
- **18 SKUs across 8 brands** — Nike, Adidas, Puma, Converse, Vans, New Balance, Reebok, ASICS — spanning 5 categories: Running, Basketball, Lifestyle, Retro, Skate

## Tech Stack

| Layer | Technology |
|---|---|
| Backend API | FastAPI, SQLAlchemy, Pydantic, Uvicorn |
| Database | MySQL, PyMySQL |
| Dashboard | Streamlit, Plotly, streamlit-autorefresh, Pandas |
| Data simulation | Python, Requests |

## Project Structure

```
Sneaker-Sales-Live-Dashboard/
├── database.py         # MySQL connection setup
├── models.py            # SQLAlchemy table definitions (products, sales)
├── schemas.py            # Pydantic request/response validation
├── main.py               # FastAPI app and all API endpoints
├── seed_products.py       # One-time script to populate the products table
├── generator.py            # Simulates continuous live sales via the API
├── dashboard.py             # Streamlit dashboard (reads from the API)
└── requirements.txt          # Python dependencies
```

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| POST | `/sales` | Records a new sale |
| GET | `/sales` | Returns recent sales |
| GET | `/kpi/revenue` | Total revenue across all sales |
| GET | `/kpi/top-products` | Top 5 products by revenue |
| GET | `/kpi/by-region` | Revenue broken down by region |
| GET | `/kpi/by-category` | Revenue broken down by sneaker type |
| GET | `/kpi/trend` | Revenue grouped by minute, for trend visualization |

## Setup

**1. Clone and create a virtual environment**
```bash
git clone <your-repo-url>
cd Sneaker-Sales-Live-Dashboard
python -m venv venv
source venv/Scripts/activate   # Windows (Git Bash)
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
pip install plotly streamlit-autorefresh
```

**3. Set up MySQL**

Create the database:
```sql
CREATE DATABASE sales_db;
```

⚠️ **Update `database.py` with your own MySQL password.** Never commit real database credentials to a public repository — consider moving this to a `.env` file (excluded via `.gitignore`) before pushing.

**4. Seed the product catalog**
```bash
python seed_products.py
```

**5. Run all three processes** (in separate terminals)
```bash
# Terminal 1 — API
uvicorn main:app --reload

# Terminal 2 — Live sales generator
python generator.py

# Terminal 3 — Dashboard
streamlit run dashboard.py
```

**6. Open the dashboard**
```
http://localhost:8501
```

## What This Project Demonstrates

- Designing and consuming a REST API with proper request/response validation
- Relational database schema design with foreign key relationships
- Writing SQL aggregation queries (joins, `GROUP BY`, `SUM`) to power live business KPIs
- Building a real-time, auto-refreshing dashboard on top of a live backend
- Debugging real-world issues in a live system (e.g., SQLAlchemy join ambiguity, MySQL connection pooling)

## License

This project was built for portfolio and educational purposes.
