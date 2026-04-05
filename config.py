import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", "Hrishikesh@14"),
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
    "Latte": 120,
    "Cappuccino": 140,
    "Mocha": 160,
    "Americano": 90,
    "Macchiato": 130,
    "Flat White": 110,
    "Cold Brew": 100,
}

# Size Options
SIZE_OPTIONS = {
    "Small": 0,
    "Medium": 20,
    "Large": 40,
}

# User Roles
USER_ROLES = ["user", "admin", "manager"]
