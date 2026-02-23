import mysql.connector
import os
def menu():
    """Display the menu."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("1. Connect to database")
    print("2. Show assigned orders")
    print("3. Add PickOrder")
    print("4. Add Product")
    print("5. Close connection")
    print("6. Quit")

def connectToDatabase(hostIP="localhost",username="admin", auth="password", dbName="",):
    """Connect to the database."""
    return mysql.connector.connect(
        host=hostIP, user=username, password=auth, database=dbName)

def showAssignedOrders(dbConnection):
    """Show PickOrders."""
    cursor = dbConnection.cursor()
    cursor.execute("SELECT * FROM PickOrder, Users INNER JOIN pickOrd_ID ON Users.user_ID = PickOrder.user_ID")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()

def addPickOrder(dbConnection, user_ID, priority, status, productID, quantity):
    """Add PickOrder to the database."""
    cursor = dbConnection.cursor()
    cursor.execute("INSERT INTO PickOrder (user_ID, productID, quantity, priority, status) VALUES (%s, %s, %s, %s, %s)", (user_ID, productID, quantity, priority, status))
    dbConnection.commit()
    cursor.close()

def addProduct(dbConnection, product_ID, productName, artNum, theType, stock):
    """Add Product to the database."""
    cursor = dbConnection.cursor()
    cursor.execute("INSERT INTO Product (productName, stock) VALUES (%s, %s, %s, %s, %s)", (product_ID, productName, artNum, theType, stock))
    dbConnection.commit()
    cursor.close()

def closeConnection(dbConnection):
    """Close connection to databaase"""
    dbConnection.close()

def quit(dbConnection):
    """Ensures program exits properly."""
    if dbConnection.is_connected():
        dbConnection.close()
        print("Connection closed.")
    print("Exiting program.")