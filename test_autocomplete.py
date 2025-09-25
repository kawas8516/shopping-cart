#!/usr/bin/env python3
"""
Test script to verify autocomplete functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Database
from config import DB_CONFIG

def test_autocomplete():
    """Test autocomplete functionality"""
    db = Database(DB_CONFIG)

    print("Testing autocomplete functionality...\n")

    # Test name suggestions
    print("Testing name suggestions:")
    test_names = ["Jo", "Ja", "Bo", "Al", "Ch", "Di", "Ed", "Fi", "Ge", "He"]

    for prefix in test_names:
        suggestions = db.search_customers_by_name(prefix)
        print(f"  '{prefix}' -> {suggestions}")

    print("\nTesting mobile suggestions:")
    test_mobiles = ["987654321", "98765432", "9876543"]

    for prefix in test_mobiles:
        suggestions = db.search_customers_by_mobile(prefix)
        print(f"  '{prefix}' -> {suggestions}")

    db.close()
    print("\nAutocomplete test completed!")

if __name__ == "__main__":
    test_autocomplete()