import os
import sqlite3
import mysql.connector
from mysql.connector import Error
from config import DB_CONFIG
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database type configuration
DB_TYPE = os.getenv("DB_TYPE", "mysql").lower()  # mysql or sqlite


def get_connection():
    """Create and return a database connection with error handling."""
    if DB_TYPE == "sqlite":
        return get_sqlite_connection()
    else:
        # Try MySQL first, fallback to SQLite if it fails
        try:
            return get_mysql_connection()
        except Exception as e:
            logger.warning(f"MySQL connection failed: {e}. Falling back to SQLite.")
            return get_sqlite_connection()


def get_mysql_connection():
    """Create MySQL database connection."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            logger.info("Successfully connected to MySQL database")
            return connection
    except Error as e:
        logger.error(f"Error connecting to MySQL database: {e}")
        raise Exception(f"Database connection failed: {e}")


def get_sqlite_connection():
    """Create SQLite database connection."""
    try:
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        connection = sqlite3.connect("data/coffee_shop.db")
        connection.execute("PRAGMA foreign_keys = ON")  # Enable foreign key support
        logger.info("Successfully connected to SQLite database")
        return connection
    except Exception as e:
        logger.error(f"Error connecting to SQLite database: {e}")
        raise Exception(f"Database connection failed: {e}")


def create_tables():
    """Create necessary tables if they don't exist."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        if DB_TYPE == "sqlite":
            create_sqlite_tables(cursor)
        else:
            create_mysql_tables(cursor)

        connection.commit()
        logger.info("Database tables created successfully")

    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        if connection:
            connection.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def create_mysql_tables(cursor):
    """Create tables for MySQL database."""
    # Users table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role ENUM('user', 'admin', 'manager') DEFAULT 'user',
            email VARCHAR(255),
            phone VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
        )
    """
    )

    # Inventory table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS inventory (
            id INT AUTO_INCREMENT PRIMARY KEY,
            item_name VARCHAR(255) NOT NULL,
            stock_quantity INT DEFAULT 0,
            unit_price DECIMAL(10,2) NOT NULL,
            category VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
    """
    )

    # Orders table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_name VARCHAR(255) NOT NULL,
            customer_phone VARCHAR(20),
            total_amount DECIMAL(10,2) NOT NULL,
            gst_amount DECIMAL(10,2) DEFAULT 0,
            final_amount DECIMAL(10,2) NOT NULL,
            payment_method ENUM('cash', 'upi', 'card') DEFAULT 'cash',
            order_status ENUM('pending', 'completed', 'cancelled') DEFAULT 'pending',
            created_by INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    """
    )

    # Order items table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS order_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            item_name VARCHAR(255) NOT NULL,
            size VARCHAR(20),
            quantity INT NOT NULL,
            unit_price DECIMAL(10,2) NOT NULL,
            total_price DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
        )
    """
    )


def create_sqlite_tables(cursor):
    """Create tables for SQLite database."""
    # Users table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user' CHECK (role IN ('user', 'admin', 'manager')),
            email TEXT,
            phone TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    """
    )

    # Inventory table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            stock_quantity INTEGER DEFAULT 0,
            unit_price REAL NOT NULL,
            category TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # Orders table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_phone TEXT,
            total_amount REAL NOT NULL,
            gst_amount REAL DEFAULT 0,
            final_amount REAL NOT NULL,
            payment_method TEXT DEFAULT 'cash' CHECK (payment_method IN ('cash', 'upi', 'card')),
            order_status TEXT DEFAULT 'pending' CHECK (order_status IN ('pending', 'completed', 'cancelled')),
            created_by INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
    """
    )

    # Order items table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            item_name TEXT NOT NULL,
            size TEXT,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
        )
    """
    )


def execute_query(query, params=None, fetch=False, return_id=False):
    """Execute a database query with proper error handling."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        is_sqlite = isinstance(connection, sqlite3.Connection)

        if is_sqlite:
            cursor = connection.cursor()
        else:
            cursor = connection.cursor(dictionary=True)

        cursor.execute(query, params or ())

        if fetch:
            if is_sqlite:
                # SQLite returns list of tuples, convert to dict format
                columns = (
                    [desc[0] for desc in cursor.description]
                    if cursor.description
                    else []
                )
                result = [dict(zip(columns, row)) for row in cursor.fetchall()]
                return result
            else:
                result = cursor.fetchall()
                return result
        else:
            connection.commit()
            if return_id:
                if is_sqlite:
                    return cursor.lastrowid
                else:
                    return cursor.lastrowid
            else:
                return cursor.rowcount

    except Exception as e:
        logger.error(f"Database query error: {e}")
        if connection:
            connection.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
