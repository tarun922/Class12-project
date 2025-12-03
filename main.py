import mysql.connector
from mysql.connector import Error
import math
import csv
from datetime import datetime
import hashlib

class RestaurantDatabase:
    def __init__(self):
        self.connection = None
        self.DB_CONFIG = {
            'host': 'localhost',
            'user': 'root',
            'password': 'your_password',  # Change this
            'database': 'restaurant_db'
        }
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(**self.DB_CONFIG)
            if self.connection.is_connected():
                return True
        except Error as e:
            print(f"Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def initialize_database(self):
        """Create tables if they don't exist"""
        cursor = self.connection.cursor()
        
        # Create Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                phone VARCHAR(15),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create Menu table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS menu (
                item_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                category VARCHAR(50),
                price DECIMAL(10, 2) NOT NULL,
                availability BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create Orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT,
                order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                total_amount DECIMAL(10, 2),
                tax_amount DECIMAL(10, 2),
                final_amount DECIMAL(10, 2),
                status VARCHAR(20) DEFAULT 'Pending',
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Create Order Details table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_details (
                detail_id INT AUTO_INCREMENT PRIMARY KEY,
                order_id INT,
                item_id INT,
                quantity INT,
                price DECIMAL(10, 2),
                subtotal DECIMAL(10, 2),
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (item_id) REFERENCES menu(item_id)
            )
        """)
        
        self.connection.commit()
        cursor.close()
        print("Database initialized successfully!")
    
    # USER OPERATIONS
    
    def register_user(self, name, email, password, phone):
        """Register a new user"""
        cursor = self.connection.cursor()
        try:
            hashed_pwd = self.hash_password(password)
            cursor.execute(
                "INSERT INTO users (name, email, password, phone) VALUES (%s, %s, %s, %s)",
                (name, email, hashed_pwd, phone)
            )
            self.connection.commit()
            user_id = cursor.lastrowid
            cursor.close()
            return {"success": True, "user_id": user_id, "message": "User registered successfully"}
        except Error as e:
            cursor.close()
            return {"success": False, "message": f"Registration failed: {str(e)}"}
    
    def login_user(self, email, password):
        """Login user"""
        cursor = self.connection.cursor(dictionary=True)
        hashed_pwd = self.hash_password(password)
        
        cursor.execute(
            "SELECT user_id, name, email FROM users WHERE email = %s AND password = %s",
            (email, hashed_pwd)
        )
        user = cursor.fetchone()
        cursor.close()
        
        if user:
            return {"success": True, "user": user, "message": "Login successful"}
        else:
            return {"success": False, "message": "Invalid credentials"}
    
    # MENU OPERATIONS
    
    def get_menu(self, category=None):
        """Get menu items"""
        cursor = self.connection.cursor(dictionary=True)
        
        if category:
            cursor.execute("SELECT * FROM menu WHERE category = %s AND availability = TRUE", (category,))
        else:
            cursor.execute("SELECT * FROM menu WHERE availability = TRUE")
        
        items = cursor.fetchall()
        cursor.close()
        return items
    
    def add_menu_item(self, name, category, price, availability=True):
        """Add new menu item"""
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO menu (name, category, price, availability) VALUES (%s, %s, %s, %s)",
                (name, category, price, availability)
            )
            self.connection.commit()
            item_id = cursor.lastrowid
            cursor.close()
            return {"success": True, "item_id": item_id, "message": "Menu item added"}
        except Error as e:
            cursor.close()
            return {"success": False, "message": str(e)}
    
    def get_categories(self):
        """Get all menu categories"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT DISTINCT category FROM menu")
        categories = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return categories
    
    def get_item_by_id(self, item_id):
        """Get menu item by ID"""
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM menu WHERE item_id = %s", (item_id,))
        item = cursor.fetchone()
        cursor.close()
        return item
    
    # ORDER OPERATIONS
    
    def place_order(self, user_id, items):
        """Place a new order
        items: list of dicts [{"item_id": 1, "quantity": 2}, ...]
        """
        cursor = self.connection.cursor(dictionary=True)
        
        try:
            # Calculate order total
            total = 0
            order_items = []
            
            for item in items:
                cursor.execute("SELECT * FROM menu WHERE item_id = %s", (item['item_id'],))
                menu_item = cursor.fetchone()
                
                if not menu_item or not menu_item['availability']:
                    return {"success": False, "message": f"Item {item['item_id']} not available"}
                
                subtotal = float(menu_item['price']) * item['quantity']
                total += subtotal
                order_items.append({
                    'item_id': item['item_id'],
                    'quantity': item['quantity'],
                    'price': float(menu_item['price']),
                    'subtotal': subtotal
                })
            
            # Calculate tax (GST 5%) using math.ceil for rounding up
            tax = math.ceil(total * 0.05 * 100) / 100
            final_amount = total + tax
            
            # Insert order
            cursor.execute(
                "INSERT INTO orders (user_id, total_amount, tax_amount, final_amount) VALUES (%s, %s, %s, %s)",
                (user_id, total, tax, final_amount)
            )
            order_id = cursor.lastrowid
            
            # Insert order details
            for item in order_items:
                cursor.execute(
                    "INSERT INTO order_details (order_id, item_id, quantity, price, subtotal) VALUES (%s, %s, %s, %s, %s)",
                    (order_id, item['item_id'], item['quantity'], item['price'], item['subtotal'])
                )
            
            self.connection.commit()
            cursor.close()
            
            return {
                "success": True,
                "order_id": order_id,
                "total": total,
                "tax": tax,
                "final_amount": final_amount,
                "message": "Order placed successfully"
            }
        except Exception as e:
            self.connection.rollback()
            cursor.close()
            return {"success": False, "message": str(e)}
    
    def get_user_orders(self, user_id):
        """Get all orders for a user"""
        cursor = self.connection.cursor(dictionary=True)
        
        cursor.execute("""
            SELECT o.*, 
                   GROUP_CONCAT(CONCAT(m.name, ' x', od.quantity) SEPARATOR ', ') as items
            FROM orders o
            LEFT JOIN order_details od ON o.order_id = od.order_id
            LEFT JOIN menu m ON od.item_id = m.item_id
            WHERE o.user_id = %s
            GROUP BY o.order_id
            ORDER BY o.order_date DESC
        """, (user_id,))
        
        orders = cursor.fetchall()
        cursor.close()
        return orders
    
    def get_order_details(self, order_id):
        """Get detailed information about an order"""
        cursor = self.connection.cursor(dictionary=True)
        
        cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
        order = cursor.fetchone()
        
        if not order:
            cursor.close()
            return None
        
        cursor.execute("""
            SELECT od.*, m.name as item_name
            FROM order_details od
            JOIN menu m ON od.item_id = m.item_id
            WHERE od.order_id = %s
        """, (order_id,))
        
        details = cursor.fetchall()
        cursor.close()
        
        return {"order": order, "items": details}
    
    # CSV EXPORT OPERATIONS
    
    def export_menu_to_csv(self, filename='menu_export.csv'):
        """Export menu to CSV file"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM menu")
        rows = cursor.fetchall()
        
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Item ID', 'Name', 'Category', 'Price', 'Availability', 'Created At'])
            writer.writerows(rows)
        
        cursor.close()
        return f"Menu exported to {filename}"
    
    def export_orders_to_csv(self, filename='orders_export.csv'):
        """Export orders to CSV file"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM orders")
        rows = cursor.fetchall()
        
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Order ID', 'User ID', 'Order Date', 'Total', 'Tax', 'Final Amount', 'Status'])
            writer.writerows(rows)
        
        cursor.close()
        return f"Orders exported to {filename}"
    
    # ANALYTICS
    
    def get_total_revenue(self):
        """Calculate total revenue"""
        cursor = self.connection.cursor()
        cursor.execute("SELECT SUM(final_amount) as total_revenue FROM orders")
        result = cursor.fetchone()
        cursor.close()
        return result[0] if result[0] else 0
    
    def get_popular_items(self):
        """Get most popular menu items"""
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                m.name,
                SUM(od.quantity) as total_orders
            FROM order_details od
            JOIN menu m ON od.item_id = m.item_id
            GROUP BY m.item_id
            ORDER BY total_orders DESC
            LIMIT 5
        """)
        items = cursor.fetchall()
        cursor.close()
        return items
    
    def get_category_sales(self):
        """Get sales by category"""
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                m.category,
                SUM(od.subtotal) as category_revenue
            FROM order_details od
            JOIN menu m ON od.item_id = m.item_id
            GROUP BY m.category
            ORDER BY category_revenue DESC
        """)
        sales = cursor.fetchall()
        cursor.close()
        return sales


# Main execution
if __name__ == "__main__":
    print("="*60)
    print("Restaurant Food Ordering System - Database Module")
    print("="*60)
    
    # Initialize database
    db = RestaurantDatabase()
    
    if db.connect():
        print("\n✓ Database connected successfully!")
        
        # Initialize tables
        db.initialize_database()
        
        print("\nDatabase is ready to use!")
        print("\nYou can now run the client application (client.py)")
        
        db.disconnect()
    else:
        print("\n✗ Failed to connect to database!")
        print("Please check your database configuration.")
