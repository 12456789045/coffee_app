#!/usr/bin/env python3
"""
Database initialization script for Coffee Shop Management System.
Run this script to set up the database with sample data.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from db import create_tables, execute_query
from models import User, Inventory
from config import MENU_ITEMS
import bcrypt


def initialize_database():
    """Initialize database with sample data."""
    print("🚀 Initializing Coffee Shop Management System Database...")

    try:
        # Create tables
        print("📋 Creating database tables...")
        create_tables()

        # Create default admin user
        print("👤 Creating default admin user...")
        try:
            admin_password = bcrypt.hashpw(
                "admin123".encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            execute_query(
                """
                INSERT INTO users (username, password, role, email, phone)
                VALUES (%s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                password = VALUES(password),
                role = VALUES(role)
            """,
                (
                    "admin",
                    admin_password,
                    "admin",
                    "admin@coffeeshop.com",
                    "+91 98765 43210",
                ),
            )
        except Exception as e:
            print(f"⚠️ Admin user creation note: {e}")

        # Initialize inventory with menu items
        print("📦 Initializing inventory...")
        for item_name, price in MENU_ITEMS.items():
            try:
                Inventory.add_or_update_item(
                    item_name=item_name,
                    stock_quantity=50,  # Default stock
                    unit_price=float(price),
                    category="Coffee",
                )
            except Exception as e:
                print(f"⚠️ Inventory item '{item_name}' note: {e}")

        # Add some additional inventory items
        additional_items = [
            ("Croissant", 60.0, 30, "Food"),
            ("Muffin", 45.0, 25, "Food"),
            ("Brownie", 80.0, 20, "Food"),
            ("Mineral Water", 25.0, 100, "Beverage"),
            ("Cold Drink", 40.0, 50, "Beverage"),
        ]

        for item_name, price, stock, category in additional_items:
            try:
                Inventory.add_or_update_item(
                    item_name=item_name,
                    stock_quantity=stock,
                    unit_price=price,
                    category=category,
                )
            except Exception as e:
                print(f"⚠️ Additional item '{item_name}' note: {e}")

        print("✅ Database initialization completed successfully!")
        print("\n📊 Sample Data Created:")
        print("👤 Admin User: admin / admin123")
        print(
            f"📦 Inventory: {len(MENU_ITEMS) + len(additional_items)} items initialized"
        )
        print("\n🚀 You can now run: streamlit run app.py")

    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    initialize_database()
