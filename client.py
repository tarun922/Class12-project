import math
from datetime import datetime
import os
import sys

# Import the database module
try:
    from main import RestaurantDatabase
except ImportError:
    print("Error: main.py not found. Please ensure main.py is in the same directory.")
    sys.exit(1)


class RestaurantClient:
    def __init__(self):
        self.db = RestaurantDatabase()
        self.current_user = None
        self.cart = []
        
        # Connect to database
        if not self.db.connect():
            print("Failed to connect to database. Exiting...")
            sys.exit(1)
        
        # Initialize database tables
        self.db.initialize_database()
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self, title):
        """Print a formatted header"""
        print("\n" + "="*70)
        print(f"{title:^70}")
        print("="*70 + "\n")
    
    def print_line(self):
        """Print a separator line"""
        print("-"*70)
    
    # USER FUNCTIONS
    
    def register(self):
        """Register a new user"""
        self.print_header("USER REGISTRATION")
        
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        password = input("Enter password: ")
        phone = input("Enter phone number: ")
        
        result = self.db.register_user(name, email, password, phone)
        
        if result['success']:
            print(f"\n✓ {result['message']}")
            print(f"Your User ID: {result['user_id']}")
        else:
            print(f"\n✗ {result['message']}")
        
        input("\nPress Enter to continue...")
    
    def login(self):
        """Login user"""
        self.print_header("USER LOGIN")
        
        email = input("Enter email: ")
        password = input("Enter password: ")
        
        result = self.db.login_user(email, password)
        
        if result['success']:
            self.current_user = result['user']
            print(f"\n✓ Welcome, {self.current_user['name']}!")
        else:
            print(f"\n✗ {result['message']}")
        
        input("\nPress Enter to continue...")
    
    def logout(self):
        """Logout current user"""
        self.current_user = None
        self.cart = []
        print("\n✓ Logged out successfully!")
        input("\nPress Enter to continue...")
    
    # MENU FUNCTIONS
    
    def browse_menu(self):
        """Browse menu items"""
        self.print_header("RESTAURANT MENU")
        
        # Get categories
        categories = self.db.get_categories()
        
        print("Select Category:")
        for i, cat in enumerate(categories, 1):
            print(f"{i}. {cat}")
        print(f"{len(categories) + 1}. All Items")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter choice: ")
        
        if choice == '0':
            return
        
        # Get menu items
        if choice.isdigit() and 1 <= int(choice) <= len(categories):
            category = categories[int(choice) - 1]
            items = self.db.get_menu(category)
        else:
            items = self.db.get_menu()
        
        if not items:
            print("\nNo items available.")
        else:
            print("\n")
            self.print_line()
            print(f"{'ID':<6} {'Item Name':<30} {'Category':<15} {'Price':<10}")
            self.print_line()
            
            for item in items:
                print(f"{item['item_id']:<6} {item['name']:<30} {item['category']:<15} ₹{item['price']:<9.2f}")
            
            self.print_line()
        
        input("\nPress Enter to continue...")
    
    def add_to_cart(self):
        """Add item to cart"""
        if not self.current_user:
            print("\n✗ Please login first!")
            input("\nPress Enter to continue...")
            return
        
        self.print_header("ADD TO CART")
        
        # Display menu
        items = self.db.get_menu()
        
        if not items:
            print("No items available.")
            input("\nPress Enter to continue...")
            return
        
        print(f"{'ID':<6} {'Item Name':<35} {'Price':<10}")
        self.print_line()
        for item in items:
            print(f"{item['item_id']:<6} {item['name']:<35} ₹{item['price']:<9.2f}")
        self.print_line()
        
        try:
            item_id = int(input("\nEnter item ID (0 to cancel): "))
            
            if item_id == 0:
                return
            
            quantity = int(input("Enter quantity: "))
            
            if quantity <= 0:
                print("\n✗ Invalid quantity!")
                input("\nPress Enter to continue...")
                return
            
            # Find item
            menu_item = self.db.get_item_by_id(item_id)
            
            if menu_item:
                # Check if item already in cart
                cart_item = next((ci for ci in self.cart if ci['item_id'] == item_id), None)
                
                if cart_item:
                    cart_item['quantity'] += quantity
                else:
                    self.cart.append({
                        'item_id': item_id,
                        'name': menu_item['name'],
                        'price': float(menu_item['price']),
                        'quantity': quantity
                    })
                
                print(f"\n✓ Added {quantity} x {menu_item['name']} to cart")
            else:
                print("\n✗ Item not found!")
                
        except ValueError:
            print("\n✗ Invalid input!")
        
        input("\nPress Enter to continue...")
    
    def view_cart(self):
        """View shopping cart"""
        self.print_header("YOUR CART")
        
        if not self.cart:
            print("Your cart is empty!")
        else:
            print(f"{'Item Name':<35} {'Qty':<6} {'Price':<12} {'Subtotal':<12}")
            self.print_line()
            
            total = 0
            for item in self.cart:
                subtotal = item['price'] * item['quantity']
                total += subtotal
                print(f"{item['name']:<35} {item['quantity']:<6} ₹{item['price']:<11.2f} ₹{subtotal:<11.2f}")
            
            # Calculate tax using math.ceil
            tax = math.ceil(total * 0.05 * 100) / 100
            final_amount = total + tax
            
            self.print_line()
            print(f"{'Subtotal:':<55} ₹{total:.2f}")
            print(f"{'Tax (5%):':<55} ₹{tax:.2f}")
            print(f"{'Grand Total:':<55} ₹{final_amount:.2f}")
            self.print_line()
        
        input("\nPress Enter to continue...")
    
    def modify_cart(self):
        """Modify cart items"""
        if not self.cart:
            print("\n✗ Your cart is empty!")
            input("\nPress Enter to continue...")
            return
        
        self.print_header("MODIFY CART")
        
        print("Your Cart Items:")
        for i, item in enumerate(self.cart, 1):
            print(f"{i}. {item['name']} - Qty: {item['quantity']} - ₹{item['price']:.2f}")
        
        print("\n1. Remove Item")
        print("2. Update Quantity")
        print("3. Clear Cart")
        print("0. Back")
        
        choice = input("\nEnter choice: ")
        
        if choice == '1':
            try:
                idx = int(input("Enter item number to remove: ")) - 1
                if 0 <= idx < len(self.cart):
                    removed = self.cart.pop(idx)
                    print(f"\n✓ Removed {removed['name']} from cart")
                else:
                    print("\n✗ Invalid item number!")
            except ValueError:
                print("\n✗ Invalid input!")
        
        elif choice == '2':
            try:
                idx = int(input("Enter item number: ")) - 1
                if 0 <= idx < len(self.cart):
                    new_qty = int(input("Enter new quantity: "))
                    if new_qty > 0:
                        self.cart[idx]['quantity'] = new_qty
                        print(f"\n✓ Updated quantity to {new_qty}")
                    else:
                        print("\n✗ Invalid quantity!")
                else:
                    print("\n✗ Invalid item number!")
            except ValueError:
                print("\n✗ Invalid input!")
        
        elif choice == '3':
            confirm = input("Clear entire cart? (yes/no): ").lower()
            if confirm == 'yes':
                self.cart = []
                print("\n✓ Cart cleared!")
        
        input("\nPress Enter to continue...")
    
    def place_order(self):
        """Place order"""
        if not self.current_user:
            print("\n✗ Please login first!")
            input("\nPress Enter to continue...")
            return
        
        if not self.cart:
            print("\n✗ Your cart is empty!")
            input("\nPress Enter to continue...")
            return
        
        self.print_header("CONFIRM ORDER")
        
        # Show cart summary
        total = sum(item['price'] * item['quantity'] for item in self.cart)
        tax = math.ceil(total * 0.05 * 100) / 100
        final_amount = total + tax
        
        print(f"Items in cart: {len(self.cart)}")
        print(f"Total amount: ₹{final_amount:.2f}")
        print(f"\nDelivery to: {self.current_user['name']}")
        
        confirm = input("\nConfirm order? (yes/no): ").lower()
        
        if confirm == 'yes':
            # Prepare order items
            order_items = [{"item_id": item['item_id'], "quantity": item['quantity']} 
                          for item in self.cart]
            
            result = self.db.place_order(self.current_user['user_id'], order_items)
            
            if result['success']:
                print("\n" + "="*70)
                print("ORDER PLACED SUCCESSFULLY!")
                print("="*70)
                print(f"Order ID: {result['order_id']}")
                print(f"Total: ₹{result['final_amount']:.2f}")
                print(f"Payment Mode: Cash on Delivery")
                print(f"\nThank you for your order, {self.current_user['name']}!")
                print("="*70)
                
                self.cart = []  # Clear cart
            else:
                print(f"\n✗ {result['message']}")
        else:
            print("\nOrder cancelled.")
        
        input("\nPress Enter to continue...")
    
    def view_order_history(self):
        """View order history"""
        if not self.current_user:
            print("\n✗ Please login first!")
            input("\nPress Enter to continue...")
            return
        
        self.print_header("ORDER HISTORY")
        
        orders = self.db.get_user_orders(self.current_user['user_id'])
        
        if not orders:
            print("No orders found.")
        else:
            for order in orders:
                print(f"\nOrder ID: {order['order_id']}")
                print(f"Date: {order['order_date']}")
                print(f"Items: {order['items']}")
                print(f"Total: ₹{order['final_amount']:.2f}")
                print(f"Status: {order['status']}")
                self.print_line()
        
        input("\nPress Enter to continue...")
    
    # ADMIN FUNCTIONS
    
    def admin_menu(self):
        """Admin panel"""
        self.print_header("ADMIN PANEL")
        
        print("1. Add Menu Item")
        print("2. View All Orders")
        print("3. Export Menu to CSV")
        print("4. Export Orders to CSV")
        print("5. View Analytics")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter choice: ")
        
        if choice == '1':
            self.add_menu_item()
        elif choice == '2':
            self.view_all_orders()
        elif choice == '3':
            self.export_menu()
        elif choice == '4':
            self.export_orders()
        elif choice == '5':
            self.view_analytics()
    
    def add_menu_item(self):
        """Add new menu item"""
        self.print_header("ADD MENU ITEM")
        
        name = input("Item name: ")
        category = input("Category: ")
        
        try:
            price = float(input("Price: "))
            
            result = self.db.add_menu_item(name, category, price)
            
            if result['success']:
                print(f"\n✓ {result['message']}")
                print(f"Item ID: {result['item_id']}")
            else:
                print(f"\n✗ {result['message']}")
        except ValueError:
            print("\n✗ Invalid price!")
        
        input("\nPress Enter to continue...")
    
    def view_all_orders(self):
        """View all orders (admin)"""
        self.print_header("ALL ORDERS")
        
        # This is simplified - in real app you'd want pagination
        print("Feature: View all orders in database")
        print("(This would show all orders from all users)")
        
        input("\nPress Enter to continue...")
    
    def export_menu(self):
        """Export menu to CSV"""
        self.print_header("EXPORT MENU")
        
        message = self.db.export_menu_to_csv()
        print(f"\n✓ {message}")
        
        input("\nPress Enter to continue...")
    
    def export_orders(self):
        """Export orders to CSV"""
        self.print_header("EXPORT ORDERS")
        
        message = self.db.export_orders_to_csv()
        print(f"\n✓ {message}")
        
        input("\nPress Enter to continue...")
    
    def view_analytics(self):
        """View analytics"""
        self.print_header("ANALYTICS")
        
        # Total Revenue
        revenue = self.db.get_total_revenue()
        print(f"Total Revenue: ₹{revenue:.2f}\n")
        
        # Popular Items
        print("Top 5 Popular Items:")
        self.print_line()
        popular = self.db.get_popular_items()
        for item in popular:
            print(f"{item['name']:<40} Orders: {item['total_orders']}")
        
        # Category Sales
        print("\nCategory-wise Sales:")
        self.print_line()
        sales = self.db.get_category_sales()
        for cat in sales:
            print(f"{cat['category']:<40} ₹{cat['category_revenue']:.2f}")
        
        input("\nPress Enter to continue...")
    
    # MAIN MENU
    
    def main_menu(self):
        """Main menu loop"""
        while True:
            self.clear_screen()
            self.print_header("RESTAURANT FOOD ORDERING SYSTEM")
            
            if self.current_user:
                print(f"Logged in as: {self.current_user['name']} ({self.current_user['email']})")
                print(f"Cart items: {len(self.cart)}\n")
            else:
                print("Not logged in\n")
            
            print("1.  Register")
            print("2.  Login")
            print("3.  Browse Menu")
            print("4.  Add to Cart")
            print("5.  View Cart")
            print("6.  Modify Cart")
            print("7.  Place Order")
            print("8.  Order History")
            print("9.  Admin Panel")
            print("10. Logout")
            print("0.  Exit")
            
            choice = input("\nEnter your choice: ")
            
            if choice == '1':
                self.register()
            elif choice == '2':
                self.login()
            elif choice == '3':
                self.browse_menu()
            elif choice == '4':
                self.add_to_cart()
            elif choice == '5':
                self.view_cart()
            elif choice == '6':
                self.modify_cart()
            elif choice == '7':
                self.place_order()
            elif choice == '8':
                self.view_order_history()
            elif choice == '9':
                self.admin_menu()
            elif choice == '10':
                self.logout()
            elif choice == '0':
                print("\nThank you for using our system!")
                print("Goodbye!")
                self.db.disconnect()
                break
            else:
                print("\n✗ Invalid choice!")
                input("\nPress Enter to continue...")


if __name__ == "__main__":
    try:
        client = RestaurantClient()
        client.main_menu()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted. Exiting...")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        print("\nThank you!")
