import streamlit as st
from models import User
from utils import (
    show_success_message,
    show_error_message,
    validate_input,
    add_custom_css,
)
from config import USER_ROLES


def login():
    """Main login and registration interface."""
    add_custom_css()

    st.markdown(
        '<h1 class="main-header">☕ Coffee Shop Management System</h1>',
        unsafe_allow_html=True,
    )
    st.markdown("### 🔐 Authentication Portal")

    tab1, tab2 = st.tabs(["🔑 Login", "📝 Register"])

    with tab1:
        login_form()

    with tab2:
        register_form()


def login_form():
    """Login form component."""
    st.subheader("Welcome Back!")

    # Create a more compact form layout
    with st.container():
        col1, col2, col3 = st.columns(
            [1, 2, 1]
        )  # Center the form with empty side columns

        with col2:
            with st.form("login_form"):
                username = st.text_input(
                    "👤 Username", placeholder="Enter your username"
                )
                password = st.text_input(
                    "🔒 Password", type="password", placeholder="Enter your password"
                )

                submitted = st.form_submit_button("🚀 Login", use_container_width=True)

                if submitted:
                    if not username or not password:
                        show_error_message("Please fill in all fields")
                        return

                    user = User.authenticate(username, password)

                    if user:
                        # Set session state
                        st.session_state.logged_in = True
                        st.session_state.user_id = user["id"]
                        st.session_state.username = user["username"]
                        st.session_state.role = user["role"]
                        st.session_state.user_email = user.get("email")
                        st.session_state.user_phone = user.get("phone")

                        show_success_message(f"Welcome back, {user['username']}!")
                        st.rerun()
                    else:
                        show_error_message("Invalid username or password")


def register_form():
    """Registration form component."""
    st.subheader("Create New Account")

    # Create a more compact form layout
    with st.container():
        col1, col2, col3 = st.columns(
            [1, 2, 1]
        )  # Center the form with empty side columns

        with col2:
            with st.form("register_form"):
                username = st.text_input("👤 Username", placeholder="Choose a username")
                email = st.text_input(
                    "📧 Email (Optional)", placeholder="your@email.com"
                )
                password = st.text_input(
                    "🔒 Password", type="password", placeholder="Create a password"
                )
                confirm_password = st.text_input(
                    "🔒 Confirm Password",
                    type="password",
                    placeholder="Confirm your password",
                )
                phone = st.text_input(
                    "📱 Phone (Optional)", placeholder="+91 XXXXX XXXXX"
                )
                role = st.selectbox(
                    "👥 Role",
                    USER_ROLES,
                    index=0,
                    help="Select your role in the system",
                )

                # Password strength indicator
                if password:
                    strength = check_password_strength(password)
                    if strength == "weak":
                        st.error(
                            "⚠️ Password is too weak. Use at least 8 characters with numbers and symbols."
                        )
                    elif strength == "medium":
                        st.warning("🟡 Password strength: Medium")
                    else:
                        st.success("🟢 Password strength: Strong")

                submitted = st.form_submit_button(
                    "📝 Create Account", use_container_width=True
                )

                if submitted:
                    # Validate input
                    data = {
                        "username": username,
                        "password": password,
                        "confirm_password": confirm_password,
                    }
                    errors = validate_input(
                        data, ["username", "password", "confirm_password"]
                    )

                    if errors:
                        for error in errors:
                            show_error_message(error)
                        return

                    # Additional validation
                    if password != confirm_password:
                        show_error_message("Passwords do not match")
                        return

                    if len(password) < 6:
                        show_error_message(
                            "Password must be at least 6 characters long"
                        )
                        return

                    if len(username) < 3:
                        show_error_message(
                            "Username must be at least 3 characters long"
                        )
                        return

                    # Attempt registration
                    try:
                        User.register(
                            username, password, role, email or None, phone or None
                        )
                        show_success_message(
                            "Account created successfully! Please login with your credentials."
                        )
                    except ValueError as e:
                        show_error_message(str(e))
                    except Exception as e:
                        show_error_message("Registration failed. Please try again.")


def check_password_strength(password):
    """Check password strength."""
    if len(password) < 8:
        return "weak"

    has_digit = any(char.isdigit() for char in password)
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    has_symbol = any(not char.isalnum() for char in password)

    score = sum([has_digit, has_upper, has_lower, has_symbol])

    if score < 3:
        return "weak"
    elif score < 4:
        return "medium"
    else:
        return "strong"
