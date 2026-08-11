from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc, func

import models
import schemas
from database import engine, get_db

# This line looks at models.py and actually CREATES the tables

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Retail Sales Analytics API")

# Allows the React dev server (localhost:5173) to call this API.
# In production you'd restrict this to your actual frontend's deployed URL.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Just a health-check endpoint to confirm the server is running."""
    return {"message": "Retail Sales Analytics API is running"}


@app.post("/sales", response_model=schemas.SaleResponse)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    """
    Receives a new sale (e.g. from our generator script later),
    saves it to the database, and returns the saved record.
    """
    new_sale = models.Sale(
        product_id=sale.product_id,
        quantity=sale.quantity,
        region=sale.region,
    )
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)  # refreshes new_sale with the auto-generated id + timestamp
    return new_sale


@app.get("/sales", response_model=list[schemas.SaleResponse])
def get_sales(limit: int = 10, db: Session = Depends(get_db)):
    """
    Returns the most recent sales. Used to manually check
    that data is actually being saved correctly.
    """
    sales = db.query(models.Sale).order_by(desc(models.Sale.timestamp)).limit(limit).all()
    return sales


# ─────────────────────────────────────────────
# KPI / ANALYTICS ENDPOINTS (Day 3)
# ─────────────────────────────────────────────

@app.get("/kpi/revenue")
def get_total_revenue(db: Session = Depends(get_db)):
    """
    Total revenue = SUM(price * quantity) across every sale,
    joining sales -> products to get each item's price.
    """
    result = (
        db.query(func.sum(models.Product.price * models.Sale.quantity))
        .select_from(models.Sale)
        .join(models.Product, models.Sale.product_id == models.Product.id)
        .scalar()
    )
    total_revenue = float(result) if result else 0.0
    return {"total_revenue": round(total_revenue, 2)}


@app.get("/kpi/top-products")
def get_top_products(limit: int = 5, db: Session = Depends(get_db)):
    """
    Top-selling products by total revenue.
    GROUP BY product, SUM(price * quantity), ordered highest first.
    """
    results = (
        db.query(
            models.Product.name,
            models.Product.brand,
            func.sum(models.Product.price * models.Sale.quantity).label("revenue"),
            func.sum(models.Sale.quantity).label("units_sold"),
        )
        .select_from(models.Sale)
        .join(models.Product, models.Sale.product_id == models.Product.id)
        .group_by(models.Product.id, models.Product.name, models.Product.brand)
        .order_by(desc("revenue"))
        .limit(limit)
        .all()
    )

    return [
        {
            "product": row.name,
            "brand": row.brand,
            "revenue": round(float(row.revenue), 2),
            "units_sold": row.units_sold,
        }
        for row in results
    ]


@app.get("/kpi/by-region")
def get_revenue_by_region(db: Session = Depends(get_db)):
    """
    Revenue broken down by region.
    Useful for a bar chart: which cities are driving the most sales.
    """
    results = (
        db.query(
            models.Sale.region,
            func.sum(models.Product.price * models.Sale.quantity).label("revenue"),
        )
        .select_from(models.Sale)
        .join(models.Product, models.Sale.product_id == models.Product.id)
        .group_by(models.Sale.region)
        .order_by(desc("revenue"))
        .all()
    )

    return [
        {"region": row.region, "revenue": round(float(row.revenue), 2)}
        for row in results
    ]


@app.get("/kpi/trend")
def get_revenue_trend(db: Session = Depends(get_db)):
    """
    Revenue grouped by minute — shows how sales are trending
    over time as the generator script keeps sending new data.
    """
    results = (
        db.query(
            func.date_format(models.Sale.timestamp, "%Y-%m-%d %H:%i").label("minute"),
            func.sum(models.Product.price * models.Sale.quantity).label("revenue"),
        )
        .join(models.Product, models.Sale.product_id == models.Product.id)
        .group_by("minute")
        .order_by("minute")
        .all()
    )

    return [
        {"minute": row.minute, "revenue": round(float(row.revenue), 2)}
        for row in results
    ]


@app.get("/kpi/by-category")
def get_revenue_by_category(db: Session = Depends(get_db)):
    """
    Revenue broken down by category (Sneakers, Jeans, Hoodies, etc.)
    Useful for showing category mix on the dashboard.
    """
    results = (
        db.query(
            models.Product.category,
            func.sum(models.Product.price * models.Sale.quantity).label("revenue"),
        )
        .join(models.Sale, models.Sale.product_id == models.Product.id)
        .group_by(models.Product.category)
        .order_by(desc("revenue"))
        .all()
    )

    return [
        {"category": row.category, "revenue": round(float(row.revenue), 2)}
        for row in results
    ]
