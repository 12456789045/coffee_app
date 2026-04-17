import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configuration
DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()  # mysql or sqlite

if DB_TYPE == "sqlite":
    # SQLite doesn't need connection parameters
    DB_CONFIG = {}
else:
    # MySQL configuration
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", 3306)),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "change_me"),
        "database": os.getenv("DB_NAME", "coffee_shop"),
    }

# Application Configuration
APP_CONFIG = {
    "name": "Coffee Shop Management System",
    "version": "1.0.0",
    "gst_rate": 0.05,
    "currency": "₹",
    "upi_id": os.getenv("UPI_ID", "yourupi@okaxis"),
}

# Menu Items
MENU_ITEMS = {
    "Espresso": 80,
    "Americano": 90,
    "Latte": 120,
    "Cappuccino": 140,
    "Mocha": 160,
    "Flat White": 110,
    "Macchiato": 130,
    "Cold Brew": 100,
    "Affogato": 170,
    "Cortado": 125,
    "Turkish Coffee": 95,
    "Irish Coffee": 190,
    "Nitro Cold Brew": 180,
    "Chai Latte": 110,
    "Matcha Latte": 150,
    "Caramel Macchiato": 165,
    "Vienna Coffee": 145,
    "Piccolo Latte": 130,
    "Hazelnut Latte": 155,
    "Vanilla Latte": 150,
}

# Size Options
SIZE_OPTIONS = {
    "Small": 0,
    "Medium": 20,
    "Large": 40,
}

# User Roles
USER_ROLES = ["user", "admin", "manager"]
