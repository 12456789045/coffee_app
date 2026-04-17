# ☕ Coffee Shop Management System - Deployment Guide

This guide covers deploying the Coffee Shop Management System to production environments.

## 📋 Prerequisites

- Python 3.10+ or Docker
- MySQL 8.0+ or use SQLite (default for cloud deployment)
- Git for version control

## 🚀 Quick Start - Local Development

### 1. Clone and Setup

```bash
git clone <your-repository>
cd streamlit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
nano .env
```

### 3. Initialize Database

```bash
python init_db.py
```

### 4. Run Application

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## 🐳 Docker Deployment

### Build Docker Image

```bash
docker build -t coffee-shop:latest .
```

### Run Container

```bash
docker run -d \
  -p 8501:8501 \
  -e DB_TYPE=mysql \
  -e DB_HOST=your-mysql-host \
  -e DB_PORT=3306 \
  -e DB_USER=your-db-user \
  -e DB_PASSWORD=your-db-password \
  -e DB_NAME=coffee_shop \
  -e SECRET_KEY=your-secret-key \
  -v data:/app/data \
  --name coffee-shop \
  coffee-shop:latest
```

## ☁️ Streamlit Cloud Deployment

### 1. Prepare Repository

```bash
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

### 2. Deploy on Streamlit Cloud

- Go to [https://share.streamlit.io](https://share.streamlit.io)
- Click "New app"
- Select your GitHub repository
- Select main branch and `app.py`
- Click "Deploy"

### 3. Configure Secrets (Streamlit Cloud)

In the app dashboard on Streamlit Cloud:

1. Click on your app settings (gear icon)
2. Select "Secrets"
3. Add your environment variables:

```toml
DB_TYPE = "sqlite"
UPI_ID = "merchant@upi"
SECRET_KEY = "your-production-secret-key"
APP_NAME = "Coffee Shop Management System"
```

## 🌐 Environment Variables

### Required for Production

```
DB_TYPE=mysql|sqlite
DB_HOST=your-database-host
DB_PORT=3306
DB_USER=database-user
DB_PASSWORD=secure-password
DB_NAME=coffee_shop
SECRET_KEY=production-secret-key
```

### Optional/Recommended

```
UPI_ID=your-upi-id
APP_NAME=Coffee Shop Management System
GST_RATE=0.05
CURRENCY=₹
ENVIRONMENT=production
DEBUG=false
```

## 🔒 Security Checklist

- [ ] Change default admin password immediately after first login
- [ ] Use strong, randomly generated SECRET_KEY
- [ ] Enable HTTPS on your domain
- [ ] Use environment variables for all sensitive data
- [ ] Keep dependencies updated: `pip list --outdated`
- [ ] Never commit `.env` file to version control
- [ ] Use BCRYPT_ROUNDS=13+ for password hashing (see config.py)
- [ ] Regularly backup your database
- [ ] Set up proper logging and monitoring
- [ ] Use database-specific security features (user permissions, SSL)

## 📊 High-Availability Setup

### With MySQL

```yaml
services:
  app:
    image: coffee-shop:latest
    environment:
      DB_TYPE: mysql
      DB_HOST: mysql-cluster
    depends_on:
      - mysql

  mysql:
    image: mysql:8.0
    volumes:
      - mysql-data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_PASSWORD}
      MYSQL_DATABASE: coffee_shop

volumes:
  mysql-data:
```

Run with: `docker-compose up -d`

## 🔧 Troubleshooting

### Database Connection Issues

```bash
# Test MySQL connection
mysql -h $DB_HOST -u $DB_USER -p$DB_PASSWORD -D $DB_NAME

# Check SQLite database
sqlite3 data/coffee_shop.db ".tables"
```

### Permission Denied on Linux

```bash
chmod +x /path/to/coffee_shop
chown -R app-user:app-group /path/to/coffee_shop
```

### Out of Memory

- Increase server memory allocation
- Optimize queries in `models.py`
- Consider database indexing for large datasets

## 📈 Monitoring & Maintenance

### Log Files

- Streamlit logs: Check container logs with `docker logs coffee-shop`
- Application logs: Configure in `config.py`

### Database Maintenance

```bash
# MySQL optimization
mysql> OPTIMIZE TABLE users, orders, inventory, bills;

# SQLite maintenance
sqlite3 data/coffee_shop.db "VACUUM;"
```

### Regular Backups

```bash
# MySQL backup
mysqldump -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME > backup.sql

# SQLite backup
cp data/coffee_shop.db data/coffee_shop.db.backup
```

## 🆘 Support

For issues and questions:

1. Check the main README.md
2. Review application logs
3. Test database connectivity
4. Verify environment variables are set correctly

## 📝 Version Notes

- **v1.0.0**: Initial production release
  - Supports MySQL 8.0+
  - SQLite for development/cloud deployment
  - RBAC with Admin/Manager/User roles
  - Order and inventory management
  - Analytics and reporting

---

**Last Updated**: April 2026
**Maintained By**: Development Team
