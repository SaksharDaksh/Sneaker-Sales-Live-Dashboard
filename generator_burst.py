"""
Burst-mode sales generator — inserts a batch of random sales, then exits.

Unlike generator.py (which loops forever), this script is designed to be
triggered periodically by a free scheduled task (e.g. a Render Cron Job
running every 5 minutes), since keeping an always-on background worker
running 24/7 typically isn't available on free hosting tiers.

Usage (local):
    python generator_burst.py

Usage (Render Cron Job):
    Set the job's command to:  python generator_burst.py
    Set schedule to, e.g.:     */5 * * * *   (every 5 minutes)
    Set the API_URL environment variable to your deployed API's URL.
"""

import requests
import random
import os

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000") + "/sales"

# Product IDs 1-18 match the 18 sneakers seeded in seed_products.py
PRODUCT_IDS = list(range(1, 19))
REGIONS = ["Mumbai", "Delhi", "Bangalore", "Pune", "Kolkata", "Hyderabad", "Chennai"]

# How many fake sales to insert per run
BATCH_SIZE = 12


def generate_fake_sale():
    return {
        "product_id": random.choice(PRODUCT_IDS),
        "quantity": random.randint(1, 4),
        "region": random.choice(REGIONS),
    }


def run_burst():
    success = 0
    for _ in range(BATCH_SIZE):
        sale = generate_fake_sale()
        try:
            response = requests.post(API_URL, json=sale, timeout=10)
            if response.status_code == 200:
                success += 1
            else:
                print(f"⚠️  API returned {response.status_code}: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")

    print(f"✅ Inserted {success}/{BATCH_SIZE} sales in this batch.")


if __name__ == "__main__":
    run_burst()
