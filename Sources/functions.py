import mysql.connector
import os
def menu(connected=False):
    """Display the menu."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Welcome to the database management program.")
    print("Please select an option:")
    print("1. Connect to database")
    print("2. Show assigned orders")
    print("3. Add PickOrder")
    print("4. Show order status")
    print("5. Add Product")
    print("6. Show all products")
    print("7. Show product stock")
    print("8. Search for product")
    print("9. Show pick order details")
    print("10. Show products low in stock")
    print("11. Close connection")
    print("12. Quit")
    print(f"Database connection status: {'Connected' if connected else 'Not Connected'}")

def connectToDatabase(hostIP="localhost",username="admin", auth="password", dbName="",):
    """Connect to the database."""
    try:
        return mysql.connector.connect(
        host=hostIP, user=username, password=auth, database=dbName)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
def showAssignedOrders(dbConnection):
    """Show PickOrders."""
    try:
        cursor = dbConnection.cursor()
        cursor.execute("SELECT po.pickOrd_ID, po.created, CONCAT(u.firstname, ' ', u.lastname) AS staff_name, po.status, po.priority, COUNT(poi.product_ID) AS num_rows, SUM(poi.quantity) 	AS total_quantity FROM PickOrders po JOIN Users u ON u.user_ID = po.user_ID LEFT JOIN PickOrderItems poi ON poi.pickOrd_ID = po.pickOrd_ID GROUP BY po.pickOrd_ID, po.created, staff_name, po.status, po.priority;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        cursor.close()
        input("Press Enter to return to main menu...")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        input("Press Enter to return to main menu...")

def addPickOrder(dbConnection, user_ID, priority, status, productID, quantity):
    """Add PickOrder to the database."""
    try:
        cursor = dbConnection.cursor()
        cursor.execute("INSERT INTO PickOrder (user_ID, product_ID, quantity, status, priority) VALUES (%s, %s, %s, %s, %s);", (user_ID, productID, quantity, status, priority))
        dbConnection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        input("Press Enter to return to main menu...")
        return False

def showOrderStatus(dbConnection):
    """Show status of PickOrders."""
    try:
        cursor = dbConnection.cursor()
        cursor.execute("SELECT u.user_ID, CONCAT(u.firstname, ' ', u.lastname) AS staff_name, COUNT(po.pickOrd_ID) 	AS orders_total, SUM(po.status <> 'Done') AS orders_open, SUM(po.status = 'Done') AS orders_done FROM Users u LEFT JOIN PickOrders po ON po.user_ID = u.user_ID GROUP BY u.user_ID, staff_name ORDER BY orders_open DESC, orders_total DESC;")
        reply = cursor.fetchall()
        for row in reply:
            print(row)
        cursor.close()
        input("Press Enter to return to main menu...")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        input("Press Enter to return to main menu...")

def addProduct(dbConnection, product_ID, productName, artNum, theType, stock, location):
    """Add Product to the database."""
    try:
        cursor = dbConnection.cursor()
        cursor.execute("INSERT INTO Product (product_ID, name, article_num, type, stock_quantity, location_ID) VALUES (%s, %s, %s, %s, %s, %s);", (product_ID, productName, artNum, theType, stock , location))
        dbConnection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        input("Press Enter to return to main menu...")
        return False

def showAllProducts(dbConnection):
    """Show all products in the database."""
    try:
        cursor = dbConnection.cursor()
        cursor.execute("SELECT p.product_ID, p.name, p.article_num, p.type, l.zone, l.aisle, l.shelf, p.stock_quantity FROM Products p JOIN Location l ON l.ID = p.location_ID;")
        rows = cursor.fetchall()
        for row in rows:
            print(row)
        cursor.close()
        input("Press Enter to return to main menu...")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        input("Press Enter to return to main menu...")

def showProductStock(dbConnection, product_ID):
    """Show stock of a product"""
    try:
        cursor=dbConnection.cursor()
        cursor.execute("CALL product_stock(%s)", (product_ID,))
        stock = cursor.fetchone()
        if stock:
            print(f"Stock for product {product_ID}: {stock[0]}")
        else:
            print(f"No stock information found for product {product_ID}.")
        cursor.close()
        input("Press Enter to return to main menu...")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        input("Press Enter to return to main menu...")

def searchForProduct(dbConnection, searchTerm):
    """Search for a product by name or article number."""
    try:
        cursor = dbConnection.cursor()
        cursor.execute("SELECT p.product_ID,p.name, p.article_num, p.type, l.zone, l.aisle, l.shelf, p.stock_quantity FROM Products p JOIN Location l ON l.ID = p.location_ID WHERE p.article_num LIKE %s OR p.name LIKE %s;", (f"%{searchTerm}%", f"%{searchTerm}%"))
        results = cursor.fetchall()
        if results:
            for result in results:
                print(result)
        else:
            print(f"No products found matching '{searchTerm}'.")
        cursor.close()
        input("Press Enter to return to main menu...")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        input("Press Enter to return to main menu...")

def showPickOrderDetails(dbConnection, pickOrd_ID):
    """Show details of a PickOrder."""
    try:
        cursor = dbConnection.cursor()
        cursor.execute("SELECT poi.pickOrd_ID, p.product_ID, p.name, poi.quantity, l.zone, l.aisle, l.shelf FROM PickOrderItems poi JOIN Products p ON p.product_ID = poi.product_ID JOIN Location l ON l.ID = p.location_ID WHERE poi.pickOrd_ID = %s;", (pickOrd_ID,))
        results = cursor.fetchall()
        if results:
            for result in results:
                print(result)
        else:
            print(f"No details found for PickOrder {pickOrd_ID}.")
        cursor.close()
        input("Press Enter to return to main menu...")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        input("Press Enter to return to main menu...")

def showProductsLowInStock(dbConnection):
    """Show products that are low in stock"""
    try:
        cursor = dbConnection.cursor()
        cursor.execute("SELECT p.product_ID, p.name, p.article_num, product_stock(p.product_ID) AS stock FROM Products p WHERE product_stock(p.product_ID) <= 5 ORDER BY stock ASC, p.name;")
        reply = cursor.fetchall()
        if reply:
            for product in reply:
                print(product)
        else:
            print("No products are low in stock.")
        cursor.close()
        input("Press Enter to return to main menu...")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        input("Press Enter to return to main menu...")
def closeConnection(dbConnection):
    """Close connection to databaase"""
    dbConnection.close()
    return None

def quit(dbConnection):
    """Ensures program exits properly."""
    if dbConnection != None:
        dbConnection.close()
        print("Connection closed.")
    print("Exiting program.")