# ☕ Coffee Shop Management System

A comprehensive, production-ready coffee shop management system built with Streamlit, featuring user authentication, inventory management, order processing, and detailed reporting.

## 🚀 Features

### 👤 User Management

- **Secure Authentication**: bcrypt password hashing
- **Role-based Access**: Admin, Manager, and User roles
- **User Registration**: Self-service account creation
- **Profile Management**: User information and status management

### 🛒 Order Management

- **Dynamic Menu**: Configurable coffee items and pricing
- **Real-time Inventory**: Stock checking and automatic updates
- **Order Processing**: Complete order lifecycle management
- **Payment Integration**: Support for cash, UPI, and card payments
- **Bill Generation**: Professional PDF receipts

### 📦 Inventory Management

- **Stock Tracking**: Real-time inventory monitoring
- **Automatic Updates**: Stock deduction on order completion
- **Low Stock Alerts**: Inventory management alerts
- **Category Organization**: Organized inventory by categories

### 📊 Analytics & Reporting

- **Sales Reports**: Daily, weekly, and monthly sales analytics
- **Popular Items**: Best-selling products tracking
- **Revenue Analysis**: Comprehensive financial reporting
- **Order History**: Complete order tracking and history

### 🖥️ Admin Dashboard

- **User Management**: Add, edit, and manage user accounts
- **Inventory Control**: Full inventory management interface
- **Order Oversight**: Monitor and update order statuses
- **System Analytics**: Business intelligence and KPIs

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Database**: MySQL
- **Security**: bcrypt password hashing
- **PDF Generation**: ReportLab
- **Data Processing**: Pandas
- **Environment Management**: python-dotenv

## 📋 Prerequisites

- Python 3.8+
- MySQL Server
- pip package manager

## ⚙️ Installation

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd coffee-shop-management
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   # or
   source venv/bin/activate     # Linux/Mac
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   - Copy `.env.example` to `.env`
   - Update database credentials and other settings

5. **Database Setup**
   - Create MySQL database: `coffee_shop`
   - The application will automatically create required tables

## 🚀 Running the Application

```bash
streamlit run app.py
```

Access the application at `http://localhost:8501`

## 📁 Project Structure

```
coffee-shop-management/
├── app.py                 # Main application entry point
├── login.py              # Authentication module
├── admin.py              # Admin dashboard
├── models.py             # Database models and business logic
├── utils.py              # Utility functions
├── config.py             # Application configuration
├── db.py                 # Database connection and operations
├── billing.py            # PDF bill generation
├── .env                  # Environment variables
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🔐 Default Credentials

After first run, create an admin account or use these defaults:

- **Username**: admin
- **Password**: admin123
- **Role**: admin

## 📊 Database Schema

### Tables

- `users`: User accounts and authentication
- `inventory`: Product inventory and stock
- `orders`: Customer orders
- `order_items`: Individual order line items

## 🔧 Configuration

Key configuration options in `config.py`:

- **Database Settings**: Connection parameters
- **Menu Items**: Coffee items and pricing
- **GST Rate**: Tax calculation
- **UPI ID**: Payment integration
- **User Roles**: Permission levels

## 📈 Features in Detail

### Order Processing

1. Customer information collection
2. Item selection with inventory checking
3. Real-time total calculation
4. Payment method selection
5. Order completion with stock updates
6. PDF bill generation

### Inventory Management

- Add/update inventory items
- Automatic stock deduction
- Low stock monitoring
- Category-based organization

### Reporting

- Sales analytics by date range
- Popular items analysis
- Revenue tracking
- Order status monitoring

## 🔒 Security Features

- **Password Hashing**: bcrypt with salt
- **SQL Injection Prevention**: Parameterized queries
- **Session Management**: Secure user sessions
- **Role-based Access**: Granular permissions
- **Input Validation**: Comprehensive data validation

## 📱 Responsive Design

- Mobile-friendly interface
- Adaptive layouts
- Touch-friendly controls
- Optimized for various screen sizes

## 🚀 Deployment

### Local Deployment

```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Production Deployment

- Use a production WSGI server (gunicorn)
- Configure reverse proxy (nginx)
- Set up SSL certificates
- Use environment variables for sensitive data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Check the documentation
- Review the code comments

## 🔄 Version History

### v1.0.0

- Initial release
- Basic order management
- User authentication
- Inventory tracking
- PDF bill generation
- Admin dashboard

---

**Built with ❤️ for coffee shop owners everywhere**
