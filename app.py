import streamlit as st
import pandas as pd
from datetime import datetime
from models import Order, Inventory
from utils import (
    show_success_message,
    show_error_message,
    format_currency,
    calculate_order_total,
    add_custom_css,
    setup_page_config,
    get_current_user,
    create_order_summary,
)
from config import MENU_ITEMS, SIZE_OPTIONS, APP_CONFIG
from billing import generate_bill

# Setup page configuration
setup_page_config()

# Initialize database tables
try:
    from db import create_tables

    create_tables()
except Exception as e:
    st.error(f"Database initialization failed: {e}")

# ------------------------- SESSION MANAGEMENT -------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.user_id = None

if "orders" not in st.session_state:
    st.session_state.orders = []

# ------------------------- AUTHENTICATION -------------------------
from login import login

if not st.session_state.logged_in:
    login()
    st.stop()


# ------------------------- MAIN APPLICATION -------------------------
def main():
    add_custom_css()

    # Sidebar
    with st.sidebar:
        st.markdown(
            '<h2 style="color: #2E8B57;">☕ Coffee Shop</h2>', unsafe_allow_html=True
        )

        # User info
        user = get_current_user()
        if user:
            st.write(f"👤 {user['username']}")
            st.write(f"👥 {user['role'].title()}")

        # Navigation
        page = st.selectbox(
            "Navigation",
            (
                ["🛒 Billing", "📋 My Orders", "🖥️ Admin Dashboard"]
                if user and user["role"] in ["admin", "manager"]
                else ["🛒 Billing", "📋 My Orders"]
            ),
        )

        # Logout
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.role = ""
            st.session_state.user_id = None
            st.session_state.orders = []
            st.rerun()

    # Route to pages
    if page == "🖥️ Admin Dashboard" and user and user["role"] in ["admin", "manager"]:
        from admin import admin_panel

        admin_panel()
    elif page == "📋 My Orders":
        order_history()
    else:
        billing_page()


def billing_page():
    """Enhanced billing page."""
    st.markdown(
        '<h1 class="main-header">🛒 Coffee Billing System</h1>', unsafe_allow_html=True
    )

    # Customer Information
    st.subheader("👤 Customer Details")

    # Use a more compact layout with columns
    col1, col2 = st.columns([3, 2])
    with col1:
        customer_name = st.text_input(
            "Customer Name", placeholder="Enter customer name", help="Required field"
        )
    with col2:
        customer_phone = st.text_input(
            "Phone Number", placeholder="+91 XXXXX XXXXX", help="Optional"
        )

    # Menu Selection
    st.subheader("☕ Order Items")

    # Create a more compact item selection form
    with st.container():
        # Item selection in a single row with better proportions
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

        with col1:
            selected_item = st.selectbox(
                "Select Item",
                list(MENU_ITEMS.keys()),
                help=f"Available: {len(MENU_ITEMS)} items",
            )

        with col2:
            selected_size = st.selectbox(
                "Size", list(SIZE_OPTIONS.keys()), help="Size affects price"
            )

        with col3:
            quantity = st.number_input(
                "Quantity",
                min_value=1,
                max_value=10,
                value=1,
                step=1,
                help="Max 10 items",
            )

        with col4:
            # Add some spacing and make button more prominent
            st.write("")  # Add vertical space
            if st.button("➕ Add Item", use_container_width=True, type="primary"):
                if not customer_name.strip():
                    show_error_message("Please enter customer name first")
                    return

                # Check inventory
                inventory = Inventory.get_all_items()
                item_stock = next(
                    (
                        item["stock_quantity"]
                        for item in inventory
                        if item["item_name"] == selected_item
                    ),
                    0,
                )

                if item_stock < quantity:
                    show_error_message(f"Insufficient stock. Available: {item_stock}")
                    return

                # Calculate price
                base_price = MENU_ITEMS[selected_item]
                size_adjustment = SIZE_OPTIONS[selected_size]
                unit_price = base_price + size_adjustment
                total_price = unit_price * quantity

                # Add to order
                order_item = {
                    "item_name": selected_item,
                    "size": selected_size,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "total_price": total_price,
                }

                st.session_state.orders.append(order_item)
                show_success_message(
                    f"Added {quantity} x {selected_item} ({selected_size})"
                )

                # Auto-scroll to order summary (optional)
                st.rerun()

    # Current Order
    if st.session_state.orders:
        st.subheader("📋 Current Order")

        # Order items table
        order_df = pd.DataFrame(st.session_state.orders)
        order_df["unit_price"] = order_df["unit_price"].apply(format_currency)
        order_df["total_price"] = order_df["total_price"].apply(format_currency)
        st.dataframe(
            order_df[["item_name", "size", "quantity", "unit_price", "total_price"]],
            use_container_width=True,
        )

        # Order totals
        totals = calculate_order_total(st.session_state.orders)
        st.markdown("---")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Subtotal", format_currency(totals["subtotal"]))
        with col2:
            st.metric("GST (5%)", format_currency(totals["gst_amount"]))
        with col3:
            st.metric("Total", format_currency(totals["final_total"]))

        # Payment method
        payment_method = st.selectbox("💳 Payment Method", ["cash", "upi", "card"])

        # Action buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💰 Complete Order", use_container_width=True):
                try:
                    user = get_current_user()
                    order_id = Order.create_order(
                        customer_name,
                        customer_phone,
                        st.session_state.orders,
                        payment_method,
                        user["id"] if user else None,
                    )

                    show_success_message(f"Order #{order_id} completed successfully!")

                    # Generate bill
                    bill_file = generate_bill(
                        customer_name,
                        st.session_state.orders,
                        totals["gst_amount"],
                        totals["final_total"],
                    )

                    # Clear order
                    st.session_state.orders = []

                    # Show download button
                    with open(bill_file, "rb") as f:
                        st.download_button(
                            label="📄 Download Bill",
                            data=f,
                            file_name=f"bill_{order_id}.pdf",
                            mime="application/pdf",
                        )

                except Exception as e:
                    show_error_message(f"Order completion failed: {str(e)}")

        with col2:
            if st.button("🗑️ Clear Order", use_container_width=True):
                st.session_state.orders = []
                show_success_message("Order cleared")

        with col3:
            if st.button("📷 Generate QR", use_container_width=True):
                # UPI QR Code
                upi_url = f"upi://pay?pa={APP_CONFIG['upi_id']}&pn=CoffeeShop&am={totals['final_total']}&cu=INR"
                qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={upi_url}"

                st.image(
                    qr_url,
                    caption=f"UPI Payment: {format_currency(totals['final_total'])}",
                )
                st.info(
                    f"Pay {format_currency(totals['final_total'])} to complete the order"
                )


def order_history():
    """Order history for current user."""
    st.markdown('<h1 class="main-header">📋 My Orders</h1>', unsafe_allow_html=True)

    user = get_current_user()
    if not user:
        show_error_message("User not authenticated")
        return

    try:
        # Get user's orders (assuming we can filter by created_by)
        # For now, show all orders since we don't have user-specific filtering in the model
        orders = Order.get_orders(50, 0)

        if orders:
            for order in orders:
                with st.expander(
                    f"Order #{order['id']} - {format_currency(order['final_amount'])} - {order['order_status'].title()}"
                ):
                    st.write(f"**Customer:** {order['customer_name']}")
                    st.write(
                        f"**Date:** {order['created_at'].strftime('%Y-%m-%d %H:%M')}"
                    )
                    st.write(f"**Payment:** {order['payment_method'].title()}")
                    st.write(f"**Status:** {order['order_status'].title()}")

                    # Order items
                    order_details = Order.get_order_details(order["id"])
                    if order_details and "items" in order_details:
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

                    # Order summary
                    st.markdown("---")
                    st.markdown(create_order_summary(order))
        else:
            st.info("No orders found")

    except Exception as e:
        show_error_message(f"Error loading orders: {str(e)}")


if __name__ == "__main__":
    main()
