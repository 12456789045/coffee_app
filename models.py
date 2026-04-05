from db import execute_query, get_connection
from config import MENU_ITEMS, SIZE_OPTIONS, APP_CONFIG, DB_TYPE
import bcrypt
import logging
from datetime import datetime, timedelta
import pandas as pd

logger = logging.getLogger(__name__)

# SQL placeholder based on database type
SQL_PLACEHOLDER = "?" if DB_TYPE == "sqlite" else "%s"


class User:
    @staticmethod
    def authenticate(username, password):
        """Authenticate user with username and password."""
        try:
            query = f"""
                SELECT id, username, password, role, email, phone, is_active
                FROM users
                WHERE username = {SQL_PLACEHOLDER} AND is_active = 1
            """
            result = execute_query(query, (username,), fetch=True)

            if result and bcrypt.checkpw(
                password.encode("utf-8"), result[0]["password"].encode("utf-8")
            ):
                return result[0]
            return None
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return None

    @staticmethod
    def register(username, password, role="user", email=None, phone=None):
        """Register a new user."""
        try:
            # Check if user exists
            existing = execute_query(
                f"SELECT id FROM users WHERE username = {SQL_PLACEHOLDER}",
                (username,),
                fetch=True,
            )
            if existing:
                raise ValueError("Username already exists")

            # Hash password
            hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

            # Insert user
            query = f"""
                INSERT INTO users (username, password, role, email, phone)
                VALUES ({SQL_PLACEHOLDER}, {SQL_PLACEHOLDER}, {SQL_PLACEHOLDER}, {SQL_PLACEHOLDER}, {SQL_PLACEHOLDER})
            """
            execute_query(query, (username, hashed.decode("utf-8"), role, email, phone))

            return True
        except Exception as e:
            logger.error(f"Registration error: {e}")
            raise

    @staticmethod
    def get_all_users():
        """Get all users for admin management."""
        query = "SELECT id, username, role, email, phone, created_at, is_active FROM users ORDER BY created_at DESC"
        return execute_query(query, fetch=True)

    @staticmethod
    def update_user_status(user_id, is_active):
        """Update user active status."""
        query = f"UPDATE users SET is_active = {SQL_PLACEHOLDER} WHERE id = {SQL_PLACEHOLDER}"
        execute_query(query, (is_active, user_id))


class Inventory:
    @staticmethod
    def get_all_items():
        """Get all inventory items."""
        query = "SELECT * FROM inventory ORDER BY item_name"
        return execute_query(query, fetch=True)

    @staticmethod
    def add_or_update_item(item_name, stock_quantity, unit_price, category=None):
        """Add or update inventory item."""
        if DB_TYPE == "sqlite":
            # SQLite approach: try to insert, if it fails, update
            try:
                query = f"""
                    INSERT INTO inventory (item_name, stock_quantity, unit_price, category)
                    VALUES ({SQL_PLACEHOLDER}, {SQL_PLACEHOLDER}, {SQL_PLACEHOLDER}, {SQL_PLACEHOLDER})
                """
                execute_query(query, (item_name, stock_quantity, unit_price, category))
            except:
                # If insert fails (duplicate), update instead
                query = f"""
                    UPDATE inventory
                    SET stock_quantity = {SQL_PLACEHOLDER}, unit_price = {SQL_PLACEHOLDER},
                        category = {SQL_PLACEHOLDER}, updated_at = CURRENT_TIMESTAMP
                    WHERE item_name = {SQL_PLACEHOLDER}
                """
                execute_query(query, (stock_quantity, unit_price, category, item_name))
        else:
            # MySQL approach with ON DUPLICATE KEY UPDATE
            query = f"""
                INSERT INTO inventory (item_name, stock_quantity, unit_price, category)
                VALUES ({SQL_PLACEHOLDER}, {SQL_PLACEHOLDER}, {SQL_PLACEHOLDER}, {SQL_PLACEHOLDER})
                ON DUPLICATE KEY UPDATE
                stock_quantity = VALUES(stock_quantity),
                unit_price = VALUES(unit_price),
                category = VALUES(category),
                updated_at = CURRENT_TIMESTAMP
            """
            execute_query(query, (item_name, stock_quantity, unit_price, category))

    @staticmethod
    def update_stock(item_name, quantity_change):
        """Update stock quantity."""
        query = f"UPDATE inventory SET stock_quantity = stock_quantity + {SQL_PLACEHOLDER} WHERE item_name = {SQL_PLACEHOLDER}"
        execute_query(query, (quantity_change, item_name))


class Order:
    @staticmethod
    def create_order(
        customer_name, customer_phone, items, payment_method="cash", created_by=None
    ):
        """Create a new order."""
        try:
            # Calculate totals
            subtotal = sum(item["total_price"] for item in items)
            gst_amount = subtotal * APP_CONFIG["gst_rate"]
            final_amount = subtotal + gst_amount

            # Insert order
            order_query = f"""
                INSERT INTO orders (customer_name, customer_phone, total_amount, gst_amount, final_amount, payment_method, created_by)
                VALUES ({SQL_PLACEHOLDER}, {SQL_PLACEHOLDER}, {SQL_PLACEHOLDER}, {SQL_PLACEHOLDER}, {SQL_PLACEHOLDER}, {SQL_PLACEHOLDER}, {SQL_PLACEHOLDER})
            """
            order_id = execute_query(
                order_query,
                (
                    customer_name,
                    customer_phone,
                    subtotal,
                    gst_amount,
                    final_amount,
                    payment_method,
                    created_by,
                ),
                return_id=True,
            )

            # Insert order items
            for item in items:
                item_query = f"""
                    INSERT INTO order_items (order_id, item_name, size, quantity, unit_price, total_price)
                    VALUES ({SQL_PLACEHOLDER}, {SQL_PLACEHOLDER}, {SQL_PLACEHOLDER}, {SQL_PLACEHOLDER}, {SQL_PLACEHOLDER}, {SQL_PLACEHOLDER})
                """
                execute_query(
                    item_query,
                    (
                        order_id,
                        item["item_name"],
                        item.get("size"),
                        item["quantity"],
                        item["unit_price"],
                        item["total_price"],
                    ),
                )

                # Update inventory
                Inventory.update_stock(item["item_name"], -item["quantity"])

            return order_id
        except Exception as e:
            logger.error(f"Order creation error: {e}")
            raise

    @staticmethod
    def get_orders(limit=50, offset=0):
        """Get orders with pagination."""
        query = f"""
            SELECT o.*, u.username as created_by_name
            FROM orders o
            LEFT JOIN users u ON o.created_by = u.id
            ORDER BY o.created_at DESC
            LIMIT {SQL_PLACEHOLDER} OFFSET {SQL_PLACEHOLDER}
        """
        return execute_query(query, (limit, offset), fetch=True)

    @staticmethod
    def get_order_details(order_id):
        """Get order with items."""
        order_query = f"SELECT * FROM orders WHERE id = {SQL_PLACEHOLDER}"
        order = execute_query(order_query, (order_id,), fetch=True)

        if order:
            items_query = (
                f"SELECT * FROM order_items WHERE order_id = {SQL_PLACEHOLDER}"
            )
            items = execute_query(items_query, (order_id,), fetch=True)
            order[0]["items"] = items
            return order[0]
        return None

    @staticmethod
    def update_order_status(order_id, status):
        """Update order status."""
        query = "UPDATE orders SET order_status = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s"
        execute_query(query, (status, order_id))

    @staticmethod
    def get_sales_report(start_date=None, end_date=None):
        """Get sales report."""
        if not start_date:
            start_date = datetime.now() - timedelta(days=30)
        if not end_date:
            end_date = datetime.now()

        query = """
            SELECT
                DATE(created_at) as date,
                COUNT(*) as orders_count,
                SUM(final_amount) as total_sales,
                SUM(gst_amount) as total_gst,
                AVG(final_amount) as avg_order_value
            FROM orders
            WHERE created_at BETWEEN %s AND %s
            AND order_status != 'cancelled'
            GROUP BY DATE(created_at)
            ORDER BY date DESC
        """
        return execute_query(query, (start_date, end_date), fetch=True)

    @staticmethod
    def get_popular_items(limit=10):
        """Get most popular items."""
        query = """
            SELECT
                item_name,
                SUM(quantity) as total_quantity,
                SUM(total_price) as total_revenue,
                COUNT(DISTINCT order_id) as orders_count
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.id
            WHERE o.order_status != 'cancelled'
            GROUP BY item_name
            ORDER BY total_quantity DESC
            LIMIT %s
        """
        return execute_query(query, (limit,), fetch=True)
