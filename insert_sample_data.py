#!/usr/bin/env python3
"""
Script to insert sample customer data for testing autocomplete functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Database
from config import DB_CONFIG

def insert_sample_customers():
    """Insert sample customers for testing"""
    db = Database(DB_CONFIG)

    # Sample customer data
    customers = [
        ("John Doe", "9876543210", "15/05/1990", "john@example.com"),
        ("Jane Smith", "9876543211", "20/08/1985", "jane@example.com"),
        ("Bob Johnson", "9876543212", "10/12/1992", "bob@example.com"),
        ("Alice Brown", "9876543213", "25/03/1988", "alice@example.com"),
        ("Charlie Wilson", "9876543214", "05/11/1995", "charlie@example.com"),
        ("Diana Davis", "9876543215", "30/07/1980", "diana@example.com"),
        ("Edward Miller", "9876543216", "12/09/1993", "edward@example.com"),
        ("Fiona Garcia", "9876543217", "18/01/1987", "fiona@example.com"),
        ("George Taylor", "9876543218", "22/06/1991", "george@example.com"),
        ("Helen Anderson", "9876543219", "08/04/1989", "helen@example.com")
    ]

    print("Inserting sample customers...")

    for name, mobile, dob, email in customers:
        customer_id = db.save_customer(name, mobile, dob, email)
        if customer_id:
            print(f"[OK] Inserted: {name} ({mobile})")
        else:
            print(f"[FAIL] Failed to insert: {name}")

    db.close()
    print("\nSample data insertion complete!")

if __name__ == "__main__":
    insert_sample_customers()