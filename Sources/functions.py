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
        headers = [column[0] for column in cursor.description]

        # Define column widths
        column_widths = [10, 20, 20, 15, 10, 10, 15]

        # Print headers with custom widths
        header_line = " | ".join(f"{header:<{width}}" for header, width in zip(headers, column_widths))
        print(header_line)
        print("-" * len(header_line))

        # Print each row with custom widths
        for row in rows:
            pickOrd_ID, created, staff_name, status, priority, num_rows, total_quantity = row
            formatted_created = created.strftime("%Y-%m-%d %H:%M:%S")
            row_line = " | ".join([
            f"{pickOrd_ID:<{column_widths[0]}}",
            f"{formatted_created:<{column_widths[1]}}",
            f"{staff_name:<{column_widths[2]}}",
            f"{status:<{column_widths[3]}}",
            f"{priority:<{column_widths[4]}}",
            f"{num_rows:<{column_widths[5]}}",
            f"{total_quantity:<{column_widths[6]}}"
            ])
            print(row_line)
        cursor.close()
        input("Press Enter to continue...")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        input("Press Enter to continue...")

def addPickOrder(dbConnection, user_ID, priority, status, productID, quantity):
    """Add PickOrder to the database."""
    try:
        cursor = dbConnection.cursor()
        cursor.execute("INSERT INTO PickOrders (user_ID, status, priority) VALUES (%s, %s, %s);", (user_ID, status, priority))
        dbConnection.commit()
        # Get the last inserted pickOrd_ID
        cursor.execute("SELECT LAST_INSERT_ID();")
        pickOrd_ID = cursor.fetchone()[0]
        # Insert into PickOrderItems
        cursor.execute("INSERT INTO PickOrderItems (pickOrd_ID, product_ID, quantity) VALUES (%s, %s, %s);", (pickOrd_ID, productID, quantity))
        dbConnection.commit()
        cursor.close()
        print("PickOrder added successfully.")
        input("Press Enter to continue...")
        return True
    except mysql.connector.Error as err:
        dbConnection.rollback()
        print(f"Error: {err}")
        input("Press Enter to continue...")
        return False

def showOrderStatus(dbConnection):
    """Show status of PickOrders."""
    try:
        cursor = dbConnection.cursor()
        cursor.execute("SELECT u.user_ID, CONCAT(u.firstname, ' ', u.lastname) AS staff_name, COUNT(po.pickOrd_ID) 	AS orders_total, SUM(po.status <> 'Done') AS orders_open, SUM(po.status = 'Done') AS orders_done FROM Users u LEFT JOIN PickOrders po ON po.user_ID = u.user_ID GROUP BY u.user_ID, staff_name ORDER BY orders_open DESC, orders_total DESC;")
        reply = cursor.fetchall()
        headers = [column[0] for column in cursor.description]
        # Define column widths
        column_widths = [10, 25, 10, 10, 10]

        # Print headers with custom widths
        header_line = " | ".join(f"{header:<{width}}" for header, width in zip(headers, column_widths))
        print(header_line)
        print("-" * len(header_line))

        # Print each row with custom widths
        for row in reply:
            row_line = " | ".join(f"{str(value):<{width}}" for value, width in zip(row, column_widths))
            print(row_line)
        cursor.close()
        input("Press Enter to continue...")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        input("Press Enter to continue...")

def addProduct(dbConnection, productName, artNum, theType, stock):
    """Add Product to the database."""
    try:
        print("Enter location details for the product(must be unique):")
        zone = input("Enter location zone(A,B,C,...): ")
        aisle = input("Enter location aisle(1,2,3,...): ")
        shelf = input("Enter location shelf(1,2,3,...): ")
        # Create location and get its ID
        createLocation(dbConnection, zone, aisle, shelf)
        
        cursor = dbConnection.cursor()
        cursor.execute("SELECT LAST_INSERT_ID();")
        location = cursor.fetchone()[0]

        cursor.execute("INSERT INTO Products (name, article_num, type, stock_quantity, location_ID) VALUES (%s, %s, %s, %s, %s);", (productName, artNum, theType, stock , location))
        dbConnection.commit()
        cursor.close()
        print("Product added successfully.")
        input("Press Enter to continue...")
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        input("Press Enter to continue...")
        return False

def showAllProducts(dbConnection):
    """Show all products in the database."""
    try:
        cursor = dbConnection.cursor()
        cursor.execute("SELECT p.product_ID, p.name, p.article_num, p.type, l.zone, l.aisle, l.shelf, p.stock_quantity FROM Products p JOIN Location l ON l.ID = p.location_ID;")
        rows = cursor.fetchall()
        headers = [column[0] for column in cursor.description]

        column_widths = [10, 20, 15, 15, 8, 8, 8, 12]

        # Print headers with custom widths
        header_line = " | ".join(f"{header:<{width}}" for header, width in zip(headers, column_widths))
        print(header_line)
        print("-" * len(header_line))

        # Print each row with custom widths
        for row in rows:
            row_line = " | ".join(f"{str(value):<{width}}" for value, width in zip(row, column_widths))
            print(row_line)
        cursor.close()
        input("Press Enter to continue...")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        input("Press Enter to continue...")

def showProductStock(dbConnection, product_ID):
    """Show stock of a product"""
    try:
        cursor=dbConnection.cursor()
        cursor.execute("SELECT product_stock(%s)", (product_ID,))
        stock = cursor.fetchone()
        if stock:
            print(f"Stock for product {product_ID}: {stock[0]}")
        else:
            print(f"No stock information found for product {product_ID}.")
        cursor.close()
        input("Press Enter to continue...")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        input("Press Enter to continue...")

def searchForProduct(dbConnection, searchTerm):
    """Search for a product by name or article number."""
    try:
        cursor = dbConnection.cursor()
        cursor.execute("SELECT p.product_ID,p.name, p.article_num, p.type, l.zone, l.aisle, l.shelf, p.stock_quantity FROM Products p JOIN Location l ON l.ID = p.location_ID WHERE p.article_num LIKE %s OR p.name LIKE %s;", (f"%{searchTerm}%", f"%{searchTerm}%"))
        results = cursor.fetchall()
        if results:
            headers = [column[0] for column in cursor.description]

            # Print headers
            header_line = " | ".join(f"{header:<15}" for header in headers)
            print(header_line)
            print("-" * len(header_line))

            # Print each row with formatted values
            for result in results:
                row_line = " | ".join(f"{str(value):<15}" for value in result)
                print(row_line)
        else:
            print(f"No products found matching '{searchTerm}'.")
        cursor.close()
        input("Press Enter to continue...")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        input("Press Enter to continue...")

def showPickOrderDetails(dbConnection, pickOrd_ID):
    """Show details of a PickOrder."""
    try:
        cursor = dbConnection.cursor()
        cursor.execute("SELECT poi.pickOrd_ID, p.product_ID, p.name, poi.quantity, l.zone, l.aisle, l.shelf FROM PickOrderItems poi JOIN Products p ON p.product_ID = poi.product_ID JOIN Location l ON l.ID = p.location_ID WHERE poi.pickOrd_ID = %s;", (pickOrd_ID,))
        results = cursor.fetchall()
        column_widths = [12, 12, 20, 10, 8, 8, 8]
        if results:
            # Get column headers
            headers = [column[0] for column in cursor.description]

            # Print headers with custom widths
            header_line = " | ".join(f"{header:<{width}}" for header, width in zip(headers, column_widths))
            print(header_line)
            print("-" * len(header_line))

            # Print each row with custom widths
            for result in results:
                row_line = " | ".join(f"{str(value):<{width}}" for value, width in zip(result, column_widths))
                print(row_line)
        else:
            print(f"No details found for PickOrder {pickOrd_ID}.")
        cursor.close()
        input("Press Enter to continue...")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        input("Press Enter to continue...")

def showProductsLowInStock(dbConnection):
    """Show products that are low in stock"""
    try:
        cursor = dbConnection.cursor()
        cursor.execute("SELECT p.product_ID, p.name, p.article_num, product_stock(p.product_ID) AS stock FROM Products p WHERE product_stock(p.product_ID) <= 5 ORDER BY stock ASC, p.name;")
        reply = cursor.fetchall()
        column_widths = [12, 20, 15, 10]
        if reply:
            headers = [column[0] for column in cursor.description]
            
            header_line = " | ".join(f"{header:<{width}}" for header, width in zip(headers, column_widths))
            print(header_line)
            print("-" * len(header_line))
            for product in reply:
                row_line = " | ".join(f"{str(value):<{width}}" for value, width in zip(product, column_widths))
                print(row_line)
        else:
            print("No products are low in stock.")
        cursor.close()
        input("Press Enter to continue...")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        input("Press Enter to continue...")
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

#Help functions for main functionality

def createLocation(dbConnection, zone, aisle, shelf):
    """Create a location in the database."""
    try:
        cursor = dbConnection.cursor()
        cursor.execute("INSERT INTO Location (zone, aisle, shelf) VALUES (%s, %s, %s);", (zone, aisle, shelf))
        dbConnection.commit()
        cursor.close()
        print("Location created successfully.")
        input("Press Enter to continue...")
        return True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        input("Press Enter to continue...")
        return False