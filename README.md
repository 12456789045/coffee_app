# ☕ Coffee Shop Management System

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://mysql.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

A comprehensive, production-ready coffee shop management system built with Streamlit, featuring modern authentication, inventory management, order processing, and detailed analytics. Perfect for small to medium-sized coffee shops looking to digitize their operations.

## ✨ Features

### 👤 User Management

- **🔐 Secure Authentication**: bcrypt password hashing with salt
- **👥 Role-based Access Control**: Admin, Manager, and Staff roles
- **📝 Self-service Registration**: User-friendly account creation
- **👤 Profile Management**: User information and status management

### 🛒 Order Management

- **📋 Dynamic Menu System**: Easily configurable coffee items and pricing
- **📦 Real-time Inventory**: Automatic stock checking and updates
- **💰 Order Processing**: Complete order lifecycle from creation to completion
- **💳 Multiple Payment Methods**: Cash, UPI, and card payment support
- **📄 Professional Bills**: PDF receipt generation with company branding

### 📦 Inventory Management

- **📊 Stock Tracking**: Real-time inventory monitoring with alerts
- **🔄 Automatic Updates**: Stock deduction on successful orders
- **⚠️ Low Stock Alerts**: Configurable inventory threshold warnings
- **🏷️ Category Organization**: Organized inventory by product categories

### 📊 Analytics & Reporting

- **📈 Sales Reports**: Daily, weekly, and monthly revenue analytics
- **🔥 Popular Items**: Best-selling products tracking and insights
- **💵 Revenue Analysis**: Comprehensive financial reporting with GST
- **📚 Order History**: Complete order tracking with search and filtering

### 🖥️ Admin Dashboard

- **👥 User Management**: Add, edit, deactivate, and manage user accounts
- **📦 Inventory Control**: Full CRUD operations for inventory management
- **📋 Order Oversight**: Monitor, update, and manage order statuses
- **📊 Business Intelligence**: KPIs, trends, and performance metrics

## 🛠️ Technology Stack

| Component           | Technology    | Purpose                        |
| ------------------- | ------------- | ------------------------------ |
| **Frontend**        | Streamlit     | Web application framework      |
| **Backend**         | Python 3.8+   | Core application logic         |
| **Database**        | MySQL         | Data persistence and storage   |
| **Security**        | bcrypt        | Password hashing and security  |
| **PDF Generation**  | ReportLab     | Professional bill creation     |
| **Data Processing** | Pandas        | Data manipulation and analysis |
| **Environment**     | python-dotenv | Configuration management       |

## 📋 Prerequisites

Before running this application, ensure you have the following installed:

### Required Software

- **Python 3.8 or higher** - [Download from python.org](https://python.org)
- **MySQL Server 8.0+** - [Download from mysql.com](https://mysql.com)
- **Git** - [Download from git-scm.com](https://git-scm.com)

### System Requirements

- **Operating System**: Windows 10+, macOS 10.15+, or Linux
- **RAM**: Minimum 4GB (8GB recommended)
- **Storage**: 500MB free space for application and database

### Optional (Recommended)

- **Visual Studio Code** - For development and debugging
- **MySQL Workbench** - For database management and visualization

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/12456789045/coffee_app.git
cd coffee_app
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

**For Local Development (MySQL):**

```bash
# Copy the environment template
cp .env.example .env

# Edit .env with your MySQL credentials
```

**For Cloud Deployment (SQLite - Recommended for Streamlit Cloud):**

```env
# Set database type to SQLite for cloud deployment
DB_TYPE=sqlite

# Application settings
APP_NAME=Coffee Shop Management System
UPI_ID=merchant@upi
GST_RATE=0.05
SECRET_KEY=your-secret-key-here
```

**Example `.env` for Local MySQL:**

```env
# Database Configuration
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=coffee_shop

# Application Settings
APP_NAME=Coffee Shop Management System
UPI_ID=merchant@upi
GST_RATE=0.05
SECRET_KEY=generate-a-secure-random-key
```

### 5. Set Up MySQL Database

```bash
# Create database
mysql -u root -p -e "CREATE DATABASE coffee_shop;"

# The application will automatically create tables on first run
```

### 6. Initialize the Application

```bash
# Run database initialization (optional - tables are created automatically)
python init_db.py
```

### 7. Start the Application

```bash
streamlit run app.py
```

**Access the application at:** `http://localhost:8501`

## 🔧 Detailed Configuration

### Database Configuration

The application supports various MySQL configurations:

```env
# Local MySQL Server
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=coffee_shop

# Remote MySQL Server
DB_HOST=your-server.com
DB_PORT=3306
DB_USER=app_user
DB_PASSWORD=secure_password
DB_NAME=coffee_db
```

### Application Settings

```env
# Company Information
APP_NAME=Your Coffee Shop Name
UPI_ID=merchant@upi

# Tax Settings
GST_RATE=0.05  # 5% GST

# Security
SECRET_KEY=generate-a-secure-random-key
```

## 📁 Project Structure

```
coffee_app/
├── 📄 app.py                 # Main application entry point
├── 🔐 login.py              # Authentication and user management
├── 👑 admin.py              # Admin dashboard and management
├── 🗄️ models.py             # Database models and business logic
├── 🛠️ utils.py              # Utility functions and helpers
├── ⚙️ config.py             # Application configuration and constants
├── 💾 db.py                 # Database connection and operations
├── 📄 billing.py            # PDF bill generation system
├── 📋 init_db.py            # Database initialization script
├── 📦 requirements.txt      # Python dependencies
├── 🔒 .env                  # Environment variables (not in repo)
├── 🚫 .gitignore           # Git ignore rules
├── 📖 README.md            # This documentation
└── 📁 bills/               # Generated PDF bills (auto-created)
```

## 👥 User Roles & Permissions

| Role        | Permissions                          | Description                                          |
| ----------- | ------------------------------------ | ---------------------------------------------------- |
| **Admin**   | Full access to all features          | System administration, user management, full reports |
| **Manager** | Order management, inventory, reports | Daily operations management                          |
| **Staff**   | Order creation, basic inventory view | Front-line operations                                |

### Default Admin Account

- **Username**: `admin`
- **Password**: `admin123`
- **Role**: Admin

⚠️ **Important**: Change the default password immediately after first login!

## 📊 Database Schema

### Core Tables

```sql
-- User accounts and authentication
users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE,
    password_hash VARCHAR(255),
    email VARCHAR(100),
    phone VARCHAR(15),
    role ENUM('admin', 'manager', 'staff'),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

-- Product inventory
inventory (
    id INT PRIMARY KEY AUTO_INCREMENT,
    item_name VARCHAR(100),
    category VARCHAR(50),
    stock_quantity INT,
    unit_price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

-- Customer orders
orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer_name VARCHAR(100),
    customer_phone VARCHAR(15),
    total_amount DECIMAL(10,2),
    gst_amount DECIMAL(10,2),
    final_amount DECIMAL(10,2),
    payment_method ENUM('cash', 'upi', 'card'),
    order_status ENUM('pending', 'completed', 'cancelled'),
    created_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (created_by) REFERENCES users(id)
)

-- Order line items
order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT,
    item_name VARCHAR(100),
    size VARCHAR(20),
    quantity INT,
    unit_price DECIMAL(10,2),
    total_price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(id)
)
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Database Connection Failed

```
Error: Can't connect to MySQL server
```

**Solutions:**

- Verify MySQL server is running
- Check database credentials in `.env`
- Ensure user has proper permissions
- Test connection: `mysql -h localhost -u username -p`

#### 2. Import Errors

```
ModuleNotFoundError: No module named 'streamlit'
```

**Solutions:**

- Activate virtual environment: `venv\Scripts\activate`
- Install dependencies: `pip install -r requirements.txt`
- Check Python version: `python --version`

#### 3. Permission Denied

```
Error: Access denied for user
```

**Solutions:**

- Grant MySQL permissions:

```sql
GRANT ALL PRIVILEGES ON coffee_shop.* TO 'username'@'localhost';
FLUSH PRIVILEGES;
```

#### 4. Port Already in Use

```
Error: Port 8501 is already in use
```

**Solutions:**

- Kill existing process: `pkill -f streamlit`
- Use different port: `streamlit run app.py --server.port 8502`

### Debug Mode

Run with debug logging:

```bash
streamlit run app.py --logger.level=debug
```

### Database Reset

To reset the database:

```bash
# Drop and recreate database
mysql -u root -p -e "DROP DATABASE coffee_shop; CREATE DATABASE coffee_shop;"

# Reinitialize
python init_db.py
```

## 🚀 Deployment

### Local Development

```bash
# Development mode with auto-reload
streamlit run app.py --server.headless true --server.port 8501
```

### Production Deployment

#### Using Docker (Recommended)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.headless", "true"]
```

#### Using Streamlit Cloud

1. **Push code to GitHub** (already done!)
2. **Connect to [share.streamlit.io](https://share.streamlit.io)**
3. **Deploy directly from repository**
4. **Set environment variables in Streamlit Cloud:**
   - `DB_TYPE=sqlite` (uses file-based database)
   - `SECRET_KEY=your-secret-key-here`
   - Other app settings as needed

**Note:** Streamlit Cloud automatically uses the `.env` file or secrets management for environment variables.

#### Using Heroku/VPS

1. Set up production database (AWS RDS, Google Cloud SQL, etc.)
2. Configure environment variables
3. Use Gunicorn for production serving

## 🤝 Contributing

We welcome contributions! Please follow these steps:

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Run tests: `python -m pytest` (if tests exist)
5. Commit changes: `git commit -am 'Add feature'`
6. Push to branch: `git push origin feature-name`
7. Submit a Pull Request

### Code Standards

- Follow PEP 8 Python style guide
- Use descriptive variable names
- Add docstrings to functions
- Test your changes thoroughly

### Reporting Issues

- Use GitHub Issues for bug reports
- Include steps to reproduce
- Add screenshots for UI issues
- Specify your environment (OS, Python version, etc.)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Streamlit** - For the amazing web app framework
- **ReportLab** - For PDF generation capabilities
- **bcrypt** - For secure password hashing
- **MySQL** - For reliable database operations

## 📞 Support

For support and questions:

- 📧 **Email**: [your-email@example.com]
- 🐛 **Issues**: [GitHub Issues](https://github.com/12456789045/coffee_app/issues)
- 📖 **Documentation**: This README and inline code comments

---

**Made with ❤️ for coffee shop owners everywhere**

⭐ Star this repository if you find it helpful! 5. Order completion with stock updates 6. PDF bill generation

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
## 👨‍💻 Author

**Hrishikesh Kulkarni**

[![GitHub](https://github.com/12456789045)
[![LinkedIn](www.linkedin.com/in/hrishikesh-kulkarni-52b7b3259)

🚀 FastAPI Developer
🤖 Agentic AI Enthusiast
🐍 Python Developer
📊 Streamlit Developer

---



**Built with ❤️ for coffee shop owners everywhere**
