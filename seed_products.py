"""
Run this ONCE to fill the products table with sample data.
Usage: python seed_products.py

NOTE: If you're re-running this after already having old (clothing) data,
first drop the old tables in MySQL Workbench so IDs and categories don't clash:

    DROP TABLE IF EXISTS sales;
    DROP TABLE IF EXISTS products;

Then run this script again — it recreates both tables automatically.
"""

from database import SessionLocal, engine, Base
import models

Base.metadata.create_all(bind=engine)

# 18 sneakers across 6 brands and 5 "type" categories
# (category here = sneaker type: Running, Basketball, Lifestyle, Retro, Skate)
products = [
    {"name": "Air Max 90", "brand": "Nike", "category": "Lifestyle", "size": "UK 8", "price": 8999},
    {"name": "Air Force 1", "brand": "Nike", "category": "Lifestyle", "size": "UK 9", "price": 7499},
    {"name": "Air Zoom Pegasus 40", "brand": "Nike", "category": "Running", "size": "UK 9", "price": 11999},
    {"name": "LeBron 21", "brand": "Nike", "category": "Basketball", "size": "UK 10", "price": 15999},

    {"name": "Ultraboost 22", "brand": "Adidas", "category": "Running", "size": "UK 8", "price": 12999},
    {"name": "Stan Smith", "brand": "Adidas", "category": "Lifestyle", "size": "UK 7", "price": 6499},
    {"name": "Dame 8", "brand": "Adidas", "category": "Basketball", "size": "UK 9", "price": 9999},
    {"name": "Samba OG", "brand": "Adidas", "category": "Retro", "size": "UK 8", "price": 7999},

    {"name": "RS-X", "brand": "Puma", "category": "Lifestyle", "size": "UK 9", "price": 6999},
    {"name": "Velocity Nitro 2", "brand": "Puma", "category": "Running", "size": "UK 8", "price": 8499},

    {"name": "Chuck Taylor All Star", "brand": "Converse", "category": "Retro", "size": "UK 9", "price": 4499},
    {"name": "Run Star Hike", "brand": "Converse", "category": "Lifestyle", "size": "UK 8", "price": 6999},

    {"name": "Old Skool", "brand": "Vans", "category": "Skate", "size": "UK 8", "price": 5499},
    {"name": "Sk8-Hi", "brand": "Vans", "category": "Skate", "size": "UK 9", "price": 5999},

    {"name": "550", "brand": "New Balance", "category": "Retro", "size": "UK 9", "price": 8999},
    {"name": "990v5", "brand": "New Balance", "category": "Running", "size": "UK 9", "price": 17999},

    {"name": "Classic Leather", "brand": "Reebok", "category": "Retro", "size": "UK 8", "price": 5999},
    {"name": "Gel-Kayano 30", "brand": "ASICS", "category": "Running", "size": "UK 9", "price": 13999},
]

db = SessionLocal()

for p in products:
    product = models.Product(
        name=p["name"],
        brand=p["brand"],
        category=p["category"],
        size=p["size"],
        price=p["price"],
    )
    db.add(product)

db.commit()
db.close()

print(f"✅ Seeded {len(products)} sneakers successfully.")
