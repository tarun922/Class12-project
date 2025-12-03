-- Create Database
CREATE DATABASE IF NOT EXISTS restaurant_db;
USE restaurant_db;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Menu Table
CREATE TABLE IF NOT EXISTS menu (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10, 2) NOT NULL,
    availability BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders Table
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2),
    tax_amount DECIMAL(10, 2),
    final_amount DECIMAL(10, 2),
    status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Order Details Table
CREATE TABLE IF NOT EXISTS order_details (
    detail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    item_id INT,
    quantity INT,
    price DECIMAL(10, 2),
    subtotal DECIMAL(10, 2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (item_id) REFERENCES menu(item_id)
);

-- Insert Sample Menu Items
INSERT INTO menu (name, category, price, availability) VALUES
('Paneer Tikka', 'Starters', 250.00, TRUE),
('Chicken Tikka', 'Starters', 300.00, TRUE),
('Veg Spring Roll', 'Starters', 180.00, TRUE),
('Butter Chicken', 'Main Course', 350.00, TRUE),
('Paneer Butter Masala', 'Main Course', 280.00, TRUE),
('Dal Makhani', 'Main Course', 220.00, TRUE),
('Veg Biryani', 'Rice', 240.00, TRUE),
('Chicken Biryani', 'Rice', 320.00, TRUE),
('Jeera Rice', 'Rice', 150.00, TRUE),
('Naan', 'Breads', 40.00, TRUE),
('Butter Naan', 'Breads', 50.00, TRUE),
('Garlic Naan', 'Breads', 60.00, TRUE),
('Gulab Jamun', 'Desserts', 80.00, TRUE),
('Ice Cream', 'Desserts', 100.00, TRUE),
('Rasgulla', 'Desserts', 70.00, TRUE),
('Coke', 'Beverages', 40.00, TRUE),
('Lassi', 'Beverages', 60.00, TRUE),
('Fresh Lime Soda', 'Beverages', 50.00, TRUE);

-- Sample queries for testing

-- View all menu items by category
SELECT * FROM menu WHERE category = 'Main Course';

-- View user orders with details
SELECT 
    o.order_id,
    u.name as customer_name,
    o.order_date,
    o.final_amount,
    GROUP_CONCAT(CONCAT(m.name, ' x', od.quantity) SEPARATOR ', ') as items
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN order_details od ON o.order_id = od.order_id
JOIN menu m ON od.item_id = m.item_id
GROUP BY o.order_id;

-- Calculate total revenue
SELECT SUM(final_amount) as total_revenue FROM orders;

-- Most popular items
SELECT 
    m.name,
    SUM(od.quantity) as total_orders
FROM order_details od
JOIN menu m ON od.item_id = m.item_id
GROUP BY m.item_id
ORDER BY total_orders DESC;

-- Category-wise sales
SELECT 
    m.category,
    SUM(od.subtotal) as category_revenue
FROM order_details od
JOIN menu m ON od.item_id = m.item_id
GROUP BY m.category
ORDER BY category_revenue DESC;
