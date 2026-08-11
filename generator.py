"""
Simulates live, real-time sales for a sneakers-only store.

Every few seconds, this script picks a random product, region, and quantity,
then sends it to your running FastAPI server (POST /sales) — just like a
real customer completing a purchase would trigger a backend event.

Usage:
    1. Make sure your API is running first:  uvicorn main:app --reload
    2. Then, in a SEPARATE terminal, run:     python generator.py
"""

import requests
import random
import time

API_URL = "http://127.0.0.1:8000/sales"

# Product IDs 1-18 match the 18 sneakers seeded in seed_products.py
PRODUCT_IDS = list(range(1, 19))

REGIONS = ["Mumbai", "Delhi", "Bangalore", "Pune", "Kolkata", "Hyderabad", "Chennai"]


def generate_fake_sale():
    """Builds one random, realistic-looking sale."""
    return {
        "product_id": random.choice(PRODUCT_IDS),
        "quantity": random.randint(1, 4),   # people rarely buy 10+ sneakers at once
        "region": random.choice(REGIONS),
    }


def run_generator():
    print("🚀 Sales generator started. Press Ctrl+C to stop.\n")
    sale_count = 0

    while True:
        sale = generate_fake_sale()

        try:
            response = requests.post(API_URL, json=sale)

            if response.status_code == 200:
                sale_count += 1
                data = response.json()
                print(
                    f"[{sale_count}] ✅ Sale saved | "
                    f"product_id={data['product_id']} | "
                    f"qty={data['quantity']} | "
                    f"region={data['region']} | "
                    f"time={data['timestamp']}"
                )
            else:
                print(f"⚠️  API returned an error: {response.status_code} - {response.text}")

        except requests.exceptions.ConnectionError:
            print("❌ Could not reach the API. Is 'uvicorn main:app --reload' running?")
            time.sleep(5)
            continue

        # Wait a random 1-4 seconds before the "next customer" buys something
        time.sleep(random.uniform(1, 4))


if __name__ == "__main__":
    run_generator()
