import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from models import User, Inventory, Order
from utils import (
    show_success_message,
    show_error_message,
    show_warning_message,
    format_currency,
    create_metrics_cards,
    export_to_csv,
    add_custom_css,
    require_role,
    get_current_user,
)
from config import MENU_ITEMS


def admin_panel():
    """Comprehensive admin dashboard."""
    add_custom_css()

    st.markdown(
        '<h1 class="main-header">🖥️ Admin Dashboard</h1>', unsafe_allow_html=True
    )

    # Check permissions
    user = get_current_user()
    if not user or user["role"] not in ["admin", "manager"]:
        show_error_message("Access denied. Admin or Manager role required.")
        return

    # Navigation tabs
    tabs = st.tabs(
        [
            "📊 Dashboard",
            "👥 User Management",
            "📦 Inventory",
            "📋 Orders",
            "📈 Reports",
        ]
    )

    with tabs[0]:
        dashboard_overview()

    with tabs[1]:
        user_management()

    with tabs[2]:
        inventory_management()

    with tabs[3]:
        order_management()

    with tabs[4]:
        sales_reports()


def dashboard_overview():
    """Dashboard overview with key metrics."""
    st.subheader("📊 Overview")

    try:
        # Get today's sales
        today = datetime.now().date()
        today_orders = Order.get_sales_report(today, today)
        today_sales = today_orders[0]["total_sales"] if today_orders else 0
        today_orders_count = today_orders[0]["orders_count"] if today_orders else 0

        # Get this month's sales
        month_start = datetime.now().replace(day=1)
        month_orders = Order.get_sales_report(month_start, datetime.now())
        month_sales = (
            sum(order["total_sales"] for order in month_orders) if month_orders else 0
        )

        # Get total inventory value
        inventory = Inventory.get_all_items()
        total_inventory_value = sum(
            item["stock_quantity"] * item["unit_price"] for item in inventory
        )

        # Get pending orders
        all_orders = Order.get_orders(1000, 0)
        pending_orders = len([o for o in all_orders if o["order_status"] == "pending"])

        # Metrics data
        metrics = [
            (
                "Today's Sales",
                format_currency(today_sales),
                f"{today_orders_count} orders",
            ),
            ("Monthly Sales", format_currency(month_sales), ""),
            ("Inventory Value", format_currency(total_inventory_value), ""),
            ("Pending Orders", str(pending_orders), ""),
        ]

        create_metrics_cards(metrics)

        # Recent orders
        st.subheader("📋 Recent Orders")
        recent_orders = Order.get_orders(10, 0)
        if recent_orders:
            df = pd.DataFrame(recent_orders)
            df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime(
                "%Y-%m-%d %H:%M"
            )
            df["final_amount"] = df["final_amount"].apply(format_currency)
            st.dataframe(
                df[
                    [
                        "id",
                        "customer_name",
                        "final_amount",
                        "order_status",
                        "created_at",
                    ]
                ],
                use_container_width=True,
            )
        else:
            st.info("No orders found")

    except Exception as e:
        show_error_message(f"Error loading dashboard: {str(e)}")


def user_management():
    """User management interface."""
    st.subheader("👥 User Management")

    # Add new user section
    with st.expander("➕ Add New User"):
        with st.form("add_user_form"):
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Username")
                email = st.text_input("Email")
            with col2:
                password = st.text_input("Password", type="password")
                role = st.selectbox("Role", ["user", "manager", "admin"])

            phone = st.text_input("Phone")

            if st.form_submit_button("Add User"):
                try:
                    User.register(username, password, role, email, phone)
                    show_success_message("User added successfully")
                    st.rerun()
                except Exception as e:
                    show_error_message(str(e))

    # Users list
    st.subheader("📋 All Users")
    try:
        users = User.get_all_users()
        if users:
            df = pd.DataFrame(users)
            df["created_at"] = pd.to_datetime(df["created_at"]).dt.strftime("%Y-%m-%d")

            # Add action buttons
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.dataframe(
                    df[
                        [
                            "username",
                            "role",
                            "email",
                            "phone",
                            "is_active",
                            "created_at",
                        ]
                    ],
                    use_container_width=True,
                )

            # User actions
            st.subheader("User Actions")
            selected_user = st.selectbox(
                "Select User", [f"{u['username']} ({u['role']})" for u in users]
            )
            if selected_user:
                user_id = next(
                    u["id"]
                    for u in users
                    if f"{u['username']} ({u['role']})" == selected_user
                )

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🔓 Activate User"):
                        User.update_user_status(user_id, True)
                        show_success_message("User activated")
                        st.rerun()
                with col2:
                    if st.button("🔒 Deactivate User"):
                        User.update_user_status(user_id, False)
                        show_success_message("User deactivated")
                        st.rerun()
        else:
            st.info("No users found")
    except Exception as e:
        show_error_message(f"Error loading users: {str(e)}")


def inventory_management():
    """Inventory management interface."""
    st.subheader("📦 Inventory Management")

    # Add/Update item
    with st.expander("➕ Add/Update Item"):
        with st.form("inventory_form"):
            col1, col2, col3 = st.columns(3)
            with col1:
                item_name = st.selectbox(
                    "Item Name", list(MENU_ITEMS.keys()) + ["Custom"]
                )
                if item_name == "Custom":
                    item_name = st.text_input("Custom Item Name")
            with col2:
                stock_quantity = st.number_input(
                    "Stock Quantity", min_value=0, value=10
                )
            with col3:
                unit_price = st.number_input(
                    "Unit Price", min_value=0.0, value=80.0, step=0.5
                )

            category = st.selectbox("Category", ["Coffee", "Beverage", "Food", "Other"])

            if st.form_submit_button("Add/Update Item"):
                try:
                    Inventory.add_or_update_item(
                        item_name, stock_quantity, unit_price, category
                    )
                    show_success_message("Inventory updated successfully")
                    st.rerun()
                except Exception as e:
                    show_error_message(str(e))

    # Inventory list
    st.subheader("📋 Current Inventory")
    try:
        inventory = Inventory.get_all_items()
        if inventory:
            df = pd.DataFrame(inventory)
            df["unit_price"] = df["unit_price"].apply(format_currency)
            df["total_value"] = (
                df["stock_quantity"]
                * df["unit_price"].str.replace("₹", "").astype(float)
            ).apply(format_currency)

            st.dataframe(
                df[
                    [
                        "item_name",
                        "stock_quantity",
                        "unit_price",
                        "category",
                        "total_value",
                    ]
                ],
                use_container_width=True,
            )

            # Export option
            if st.button("📥 Export Inventory"):
                export_to_csv(inventory, "inventory.csv")
        else:
            st.info("No inventory items found")
    except Exception as e:
        show_error_message(f"Error loading inventory: {str(e)}")


def order_management():
    """Order management interface."""
    st.subheader("📋 Order Management")

    # Order filters
    col1, col2, col3 = st.columns(3)
    with col1:
        status_filter = st.selectbox(
            "Status", ["All", "pending", "preparing", "ready", "completed", "cancelled"]
        )
    with col2:
        limit = st.selectbox("Show", [10, 25, 50, 100], index=1)
    with col3:
        search = st.text_input("Search customer", placeholder="Customer name...")

    try:
        # Get orders
        orders = Order.get_orders(limit, 0)

        if search:
            orders = [o for o in orders if search.lower() in o["customer_name"].lower()]

        if status_filter != "All":
            orders = [o for o in orders if o["order_status"] == status_filter]

        if orders:
            # Display orders
            for order in orders:
                with st.expander(
                    f"Order #{order['id']} - {order['customer_name']} - {format_currency(order['final_amount'])}"
                ):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**Status:** {order['order_status'].title()}")
                        st.write(f"**Payment:** {order['payment_method'].title()}")
                    with col2:
                        st.write(f"**Phone:** {order.get('customer_phone', 'N/A')}")
                        st.write(
                            f"**Created:** {order['created_at'].strftime('%Y-%m-%d %H:%M')}"
                        )
                    with col3:
                        st.write(
                            f"**Created by:** {order.get('created_by_name', 'N/A')}"
                        )

                    # Order items
                    order_details = Order.get_order_details(order["id"])
                    if order_details and "items" in order_details:
                        st.subheader("Items:")
                        items_df = pd.DataFrame(order_details["items"])
                        items_df["unit_price"] = items_df["unit_price"].apply(
                            format_currency
                        )
                        items_df["total_price"] = items_df["total_price"].apply(
                            format_currency
                        )
                        st.dataframe(
                            items_df[
                                [
                                    "item_name",
                                    "size",
                                    "quantity",
                                    "unit_price",
                                    "total_price",
                                ]
                            ],
                            use_container_width=True,
                        )

                    # Status update
                    if order["order_status"] != "completed":
                        new_status = st.selectbox(
                            "Update Status",
                            ["pending", "preparing", "ready", "completed", "cancelled"],
                            index=[
                                "pending",
                                "preparing",
                                "ready",
                                "completed",
                                "cancelled",
                            ].index(order["order_status"]),
                            key=f"status_{order['id']}",
                        )
                        if st.button("Update Status", key=f"update_{order['id']}"):
                            Order.update_order_status(order["id"], new_status)
                            show_success_message("Order status updated")
                            st.rerun()
        else:
            st.info("No orders found")
    except Exception as e:
        show_error_message(f"Error loading orders: {str(e)}")


def sales_reports():
    """Sales reports and analytics."""
    st.subheader("📈 Sales Reports")

    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime.now() - timedelta(days=30))
    with col2:
        end_date = st.date_input("End Date", datetime.now())

    if start_date > end_date:
        show_error_message("Start date cannot be after end date")
        return

    try:
        # Sales report
        sales_data = Order.get_sales_report(start_date, end_date)
        if sales_data:
            st.subheader("📊 Daily Sales")
            df = pd.DataFrame(sales_data)
            df["total_sales"] = df["total_sales"].apply(format_currency)
            df["total_gst"] = df["total_gst"].apply(format_currency)
            df["avg_order_value"] = df["avg_order_value"].apply(format_currency)
            st.dataframe(df, use_container_width=True)

            # Summary metrics
            total_sales = sum(
                float(row["total_sales"].replace("₹", "").replace(",", ""))
                for row in sales_data
            )
            total_orders = sum(row["orders_count"] for row in sales_data)
            avg_daily_sales = total_sales / len(sales_data) if sales_data else 0

            st.subheader("📋 Summary")
            metrics = [
                ("Total Sales", format_currency(total_sales), ""),
                ("Total Orders", str(total_orders), ""),
                ("Average Daily Sales", format_currency(avg_daily_sales), ""),
                ("Period Days", str(len(sales_data)), ""),
            ]
            create_metrics_cards(metrics)

            # Export option
            if st.button("📥 Export Sales Report"):
                export_to_csv(sales_data, f"sales_report_{start_date}_{end_date}.csv")
        else:
            st.info("No sales data found for the selected period")

        # Popular items
        st.subheader("🔥 Popular Items")
        popular_items = Order.get_popular_items(10)
        if popular_items:
            df = pd.DataFrame(popular_items)
            df["total_revenue"] = df["total_revenue"].apply(format_currency)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No item data available")

    except Exception as e:
        show_error_message(f"Error generating reports: {str(e)}")
