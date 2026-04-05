import streamlit as st
import pandas as pd
from datetime import datetime
from config import APP_CONFIG
import logging

logger = logging.getLogger(__name__)


def format_currency(amount):
    """Format amount as currency."""
    return f"{APP_CONFIG['currency']}{amount:,.2f}"


def calculate_order_total(items):
    """Calculate order totals including GST."""
    subtotal = sum(item["total_price"] for item in items)
    gst_amount = subtotal * APP_CONFIG["gst_rate"]
    final_total = subtotal + gst_amount

    return {"subtotal": subtotal, "gst_amount": gst_amount, "final_total": final_total}


def validate_input(data, required_fields):
    """Validate input data."""
    errors = []
    for field in required_fields:
        if not data.get(field):
            errors.append(f"{field.replace('_', ' ').title()} is required")
    return errors


def show_success_message(message):
    """Show success message with styling."""
    st.success(f"✅ {message}")


def show_error_message(message):
    """Show error message with styling."""
    st.error(f"❌ {message}")


def show_warning_message(message):
    """Show warning message with styling."""
    st.warning(f"⚠️ {message}")


def show_info_message(message):
    """Show info message with styling."""
    st.info(f"ℹ️ {message}")


def create_order_summary(order_data):
    """Create a formatted order summary."""
    summary = f"""
**Order Summary**
- Customer: {order_data['customer_name']}
- Phone: {order_data.get('customer_phone', 'N/A')}
- Items: {len(order_data.get('items', []))}
- Total: {format_currency(order_data['final_amount'])}
- Status: {order_data['order_status'].title()}
- Date: {order_data['created_at'].strftime('%Y-%m-%d %H:%M')}
    """
    return summary


def export_to_csv(data, filename):
    """Export data to CSV."""
    df = pd.DataFrame(data)
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV", data=csv, file_name=filename, mime="text/csv"
    )


def get_current_user():
    """Get current logged in user info."""
    if st.session_state.get("logged_in") and st.session_state.get("user_id"):
        return {
            "id": st.session_state["user_id"],
            "username": st.session_state["username"],
            "role": st.session_state["role"],
        }
    return None


def require_role(required_role):
    """Check if current user has required role."""
    user = get_current_user()
    if not user:
        return False
    return user["role"] == required_role or user["role"] == "admin"


def setup_page_config():
    """Setup Streamlit page configuration."""
    st.set_page_config(
        page_title=APP_CONFIG["name"],
        page_icon="☕",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def add_custom_css():
    """Add custom CSS for better styling."""
    st.markdown(
        """
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 2rem;
    }
    .card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 5px solid #2E8B57;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .status-completed {
        color: #28a745;
        font-weight: bold;
    }
    .status-pending {
        color: #ffc107;
        font-weight: bold;
    }
    .status-cancelled {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


def create_metrics_cards(metrics_data):
    """Create metrics cards for dashboard."""
    cols = st.columns(len(metrics_data))

    for i, (title, value, delta) in enumerate(metrics_data):
        with cols[i]:
            st.markdown(
                f"""
            <div class="metric-card">
                <h3>{value}</h3>
                <p>{title}</p>
                {f'<small>{delta}</small>' if delta else ''}
            </div>
            """,
                unsafe_allow_html=True,
            )


def handle_db_error(error):
    """Handle database errors gracefully."""
    logger.error(f"Database error: {error}")
    show_error_message("A database error occurred. Please try again later.")
    st.stop()


def confirm_action(message):
    """Show confirmation dialog."""
    return st.checkbox(f"✅ {message}")


def get_status_color(status):
    """Get color for status."""
    colors = {
        "completed": "status-completed",
        "pending": "status-pending",
        "cancelled": "status-cancelled",
        "preparing": "status-pending",
        "ready": "status-completed",
    }
    return colors.get(status.lower(), "")
