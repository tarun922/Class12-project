# Class12-project

# Restaurant Food Ordering System - Class 12 Project

A complete online food ordering system built with Python and MySQL using only syllabus-approved modules.

## 📋 Project Structure

```
restaurant_ordering_system/
├── main.py                 # Database module with all operations
├── client.py               # Console-based client interface
├── database_setup.sql      # SQL script for database initialization
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🛠️ Technologies Used

- **Programming Language**: Python 3.x
- **Database**: MySQL
- **Python Modules**:
  - `mysql.connector` - MySQL database connectivity
  - `csv` - CSV file operations
  - `math` - Mathematical calculations
  - `hashlib` - Password hashing
  - `datetime` - Date and time operations
  - `os` - Operating system interface
  - `sys` - System-specific functions

## 📦 Installation Steps

### 1. Install Python Dependencies

Only one external package is required:

```bash
pip install mysql-connector-python
```

All other modules (csv, math, hashlib, datetime, os, sys) are built-in Python modules.

You can also create a `requirements.txt` file:
```
mysql-connector-python==8.2.0
```

Then install:
```bash
pip install -r requirements.txt
```

### 2. Setup MySQL Database

1. Install MySQL Server on your system
2. Open MySQL Command Line or MySQL Workbench
3. Run the SQL script:

```sql
SOURCE database_setup.sql;
```

Or manually copy and execute the SQL commands from `database_setup.sql`

### 3. Configure Database Connection

Edit `main.py` and update the database configuration in the `RestaurantDatabase` class:

```python
self.DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',           # Your MySQL username
    'password': 'your_password',  # Your MySQL password
    'database': 'restaurant_db'
}
```

## 🚀 Running the Application

### Step 1: Test Database Connection

First, test if the database module works correctly:

```bash
python main.py
```

You should see:
```
✓ Database connected successfully!
Database initialized successfully!
```

### Step 2: Run the Client Application

```bash
python client.py
```

The console-based menu system will appear!

## 📱 Features

### User Features
1. **User Registration** - Create a new account with name, email, password, phone
2. **User Login** - Secure authentication with SHA-256 hashed passwords
3. **Browse Menu** - View all available items, filter by category
4. **Add to Cart** - Select items and quantities
5. **View Cart** - Review cart with automatic price calculations
6. **Modify Cart** - Update quantities, remove items, clear cart
7. **Place Order** - Confirm and place orders with bill generation
8. **Order History** - View all past orders with details

### Admin Features
1. **Add Menu Items** - Add new dishes to the menu
2. **View All Orders** - Monitor all orders in system
3. **Export Menu** - Export menu data to CSV file
4. **Export Orders** - Export order history to CSV file
5. **View Analytics** - See revenue, popular items, category sales

### System Features
- **Password Security**: SHA-256 hashing using `hashlib` module
- **Tax Calculation**: Automatic 5% GST calculation using `math.ceil()` for proper rounding
- **Real-time Calculations**: Dynamic price calculations for cart and orders
- **Database Transactions**: Ensures data consistency during order placement
- **CSV Export**: Export data using `csv` module for reports
- **Error Handling**: Comprehensive error handling throughout

## 📊 Database Schema

### Tables

**users**
- user_id (Primary Key, Auto Increment)
- name (VARCHAR 100)
- email (VARCHAR 100, Unique)
- password (VARCHAR 255, Hashed)
- phone (VARCHAR 15)
- created_at (TIMESTAMP)

**menu**
- item_id (Primary Key, Auto Increment)
- name (VARCHAR 100)
- category (VARCHAR 50)
- price (DECIMAL 10,2)
- availability (BOOLEAN)
- created_at (TIMESTAMP)

**orders**
- order_id (Primary Key, Auto Increment)
- user_id (Foreign Key → users)
- order_date (TIMESTAMP)
- total_amount (DECIMAL 10,2)
- tax_amount (DECIMAL 10,2)
- final_amount (DECIMAL 10,2)
- status (VARCHAR 20)

**order_details**
- detail_id (Primary Key, Auto Increment)
- order_id (Foreign Key → orders)
- item_id (Foreign Key → menu)
- quantity (INT)
- price (DECIMAL 10,2)
- subtotal (DECIMAL 10,2)

## 💡 Usage Example

### Sample User Journey:

1. **Run the Application**
   ```bash
   python client.py
   ```

2. **Register Account**
   - Select option 1 (Register)
   - Enter: Name, Email, Password, Phone

3. **Login**
   - Select option 2 (Login)
   - Enter your email and password

4. **Browse Menu**
   - Select option 3 (Browse Menu)
   - Choose a category or view all items

5. **Order Food**
   - Select option 4 (Add to Cart)
   - Enter item ID and quantity
   - Repeat for multiple items
   - Select option 5 to view cart
   - Select option 7 to place order

6. **View Order History**
   - Select option 8 (Order History)
   - See all your past orders

## 🧮 Module Usage Details

### 1. mysql.connector Module
```python
import mysql.connector
from mysql.connector import Error

# Connecting to database
connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='password',
    database='restaurant_db'
)

# Using cursor for queries
cursor = connection.cursor(dictionary=True)
cursor.execute("SELECT * FROM menu")
results = cursor.fetchall()
```

**Used for:**
- Database connectivity
- Executing SQL queries
- Fetching results
- Transaction management

### 2. csv Module
```python
import csv

# Writing to CSV
with open('menu_export.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['ID', 'Name', 'Price'])
    writer.writerows(data)
```

**Used for:**
- Exporting menu to CSV files
- Exporting orders to CSV files
- Creating reports for analysis

### 3. math Module
```python
import math

# Tax calculation with proper rounding
total = 1000
tax = math.ceil(total * 0.05 * 100) / 100
# Result: 50.00 (rounded up to 2 decimal places)
```

**Used for:**
- Calculating GST (5% tax)
- Rounding up amounts using `math.ceil()`
- Ensuring accurate financial calculations

### 4. hashlib Module
```python
import hashlib

# Hashing passwords
password = "mypassword"
hashed = hashlib.sha256(password.encode()).hexdigest()
# Result: Secure SHA-256 hash
```

**Used for:**
- Password encryption
- Secure user authentication
- Data security

### 5. datetime Module
```python
from datetime import datetime

# Timestamps are handled automatically by MySQL
# But datetime can be used for date formatting
current_time = datetime.now()
```

**Used for:**
- Date and time operations
- Order timestamps
- Time-based queries

### 6. os and sys Modules
```python
import os
import sys

# Clear screen
os.system('cls' if os.name == 'nt' else 'clear')

# Exit program
sys.exit(1)
```

**Used for:**
- Screen clearing for better UI
- System operations
- Program control flow

## 📁 Sample Menu Categories

The database comes pre-loaded with 18 items across 6 categories:

- **Starters**: Paneer Tikka (₹250), Chicken Tikka (₹300), Veg Spring Roll (₹180)
- **Main Course**: Butter Chicken (₹350), Paneer Butter Masala (₹280), Dal Makhani (₹220)
- **Rice**: Veg Biryani (₹240), Chicken Biryani (₹320), Jeera Rice (₹150)
- **Breads**: Naan (₹40), Butter Naan (₹50), Garlic Naan (₹60)
- **Desserts**: Gulab Jamun (₹80), Ice Cream (₹100), Rasgulla (₹70)
- **Beverages**: Coke (₹40), Lassi (₹60), Fresh Lime Soda (₹50)

## 🎓 Class 12 Project Highlights

This project demonstrates:

1. **Python Programming**
   - Functions and methods
   - Object-oriented programming (Classes)
   - Error handling (try-except)
   - Module imports
   - File I/O operations

2. **Database Management**
   - Database connectivity
   - CRUD operations (Create, Read, Update, Delete)
   - SQL queries (SELECT, INSERT, UPDATE)
   - Joins and aggregations
   - Foreign key relationships

3. **Data Structures**
   - Lists for cart management
   - Dictionaries for data storage
   - Tuples from database results

4. **Mathematical Operations**
   - Price calculations
   - Tax computation using `math.ceil()`
   - Subtotal and total calculations

5. **File Handling**
   - CSV file creation
   - Writing data to files
   - Exporting database records

6. **Security**
   - Password hashing with SHA-256
   - SQL injection prevention
   - Input validation

7. **User Interface**
   - Console-based menu system
   - Formatted output
   - User input handling

## 🐛 Troubleshooting

### Common Issues:

**1. Database Connection Error**
```
Error: Can't connect to MySQL server
```
**Solution:**
- Verify MySQL is running
- Check username/password in `main.py`
- Ensure database 'restaurant_db' exists

**2. Module Not Found Error**
```
ModuleNotFoundError: No module named 'mysql'
```
**Solution:**
```bash
pip install mysql-connector-python
```

**3. Import Error in client.py**
```
ImportError: No module named 'main'
```
**Solution:**
- Ensure `main.py` is in the same directory as `client.py`
- Run `client.py` from the project directory

**4. Permission Denied on CSV Export**
```
PermissionError: [Errno 13] Permission denied
```
**Solution:**
- Close any CSV files if they're open
- Check folder write permissions

**5. Table Already Exists Error**
```
Table 'users' already exists
```
**Solution:**
- This is normal if tables were created before
- The application will continue to work

## 📚 Code Walkthrough for Presentation

### 1. Database Module (main.py)

**Key Components:**
```python
# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'restaurant_db'
}

# Password Hashing
def hash_password(self, password):
    return hashlib.sha256(password.encode()).hexdigest()

# Tax Calculation with math.ceil
tax = math.ceil(total * 0.05 * 100) / 100
```

### 2. Client Application (client.py)

**Key Features:**
```python
# Cart Management
self.cart = []  # List to store cart items

# Adding to cart
self.cart.append({
    'item_id': item_id,
    'name': item['name'],
    'price': float(item['price']),
    'quantity': quantity
})

# Order placement with database transaction
result = self.db.place_order(user_id, items)
```

### 3. SQL Operations

**Sample Queries:**
```sql
-- User Registration
INSERT INTO users (name, email, password, phone) 
VALUES (%s, %s, %s, %s)

-- Get Menu Items
SELECT * FROM menu WHERE category = %s AND availability = TRUE

-- Place Order
INSERT INTO orders (user_id, total_amount, tax_amount, final_amount) 
VALUES (%s, %s, %s, %s)
```

## 🎯 Project Demonstration Tips

1. **Start with Overview**
   - Explain the project purpose
   - Show the technology stack
   - Demonstrate real-world application

2. **Database Schema**
   - Show ER diagram or table relationships
   - Explain foreign keys and normalization
   - Display sample data

3. **Module Explanation**
   - Explain why each module was used
   - Show specific code examples
   - Demonstrate module functionality

4. **Live Demonstration**
   - Register a new user
   - Browse menu and add items to cart
   - Place an order
   - Show order in database
   - Export data to CSV

5. **Security Features**
   - Demonstrate password hashing
   - Show hashed passwords in database
   - Explain SQL injection prevention

6. **Mathematical Calculations**
   - Show tax calculation code
   - Explain `math.ceil()` usage
   - Demonstrate with examples

7. **CSV Export**
   - Export menu to CSV
   - Open and show the file
   - Explain practical use cases

## 💻 Sample Output Screenshots (Describe These)

**Main Menu:**
```
======================================================================
             RESTAURANT FOOD ORDERING SYSTEM
======================================================================

Logged in as: John Doe (john@example.com)
Cart items: 2

1.  Register
2.  Login
3.  Browse Menu
4.  Add to Cart
5.  View Cart
...
```

**Order Confirmation:**
```
======================================================================
                    ORDER PLACED SUCCESSFULLY!
======================================================================
Order ID: 1
Total: ₹525.00
Payment Mode: Cash on Delivery

Thank you for your order, John Doe!
======================================================================
```

## 🔄 Future Enhancements

- GUI using Tkinter
- Payment gateway integration
- Email notifications
- Rating and review system
- Delivery tracking
- Admin dashboard with graphs
- Mobile app integration
- Online payment options

## 📞 Support

For any issues or questions:
1. Check the troubleshooting section
2. Verify all modules are installed
3. Ensure MySQL is running
4. Check database configuration

## ✅ Project Checklist

Before submission, ensure:
- [ ] All modules are syllabus-approved
- [ ] Database is properly normalized
- [ ] Code is well-commented
- [ ] All features work correctly
- [ ] Security measures implemented
- [ ] CSV export functions work
- [ ] Documentation is complete
- [ ] Sample data is loaded
- [ ] Screenshots/outputs prepared
- [ ] Presentation ready

---

**Made for Class 12 Computer Science Project (2024-25)**

**Modules Used (All Syllabus-Approved):**
- mysql.connector
- csv
- math
- hashlib
- datetime
- os
- sys
