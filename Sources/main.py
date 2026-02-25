import functions
import mysql.connector
def main():
    """Main entry point of the program."""
    exit = False
    connected = False
    connect = None
    while not exit:
        functions.menu(connected)
        selection = input("Please select an option: ")
        match selection, connected:
            case "1", False:
                ip = input("Enter database IP (default: localhost): ") or "localhost"
                username = input("Enter database username (default: admin): ") or "admin"
                password = input("Enter database password (default: password): ") or "password"
                dbName = input("Enter database name: ")
                connect = functions.connectToDatabase(ip, username, password, dbName)
    
                if connect != None:
                    print("Connected to database.")
                    connected = True
                    input("Press Enter to return to main menu...")
                else:
                    print("Failed to connect to database. Please check your credentials and try again.")
                    input("Press Enter to return to main menu...")
            case "2", True:
                functions.showAssignedOrders(connect)
            case "3", True:
                user_ID = input("Enter user ID: ")
                productID = input("Enter product ID: ")
                quantity = input("Enter quantity: ")
                priority = input("Enter priority: ")
                status = input("Enter status: ")
                functions.addPickOrder(connect, user_ID, priority, status, productID, quantity)
            case "4", True:
                product_ID = input("Enter product ID: ")
                productName = input("Enter product name: ")
                artNum = input("Enter article number: ")
                theType = input("Enter product type: ")
                stock = input("Enter stock quantity: ")
                location = input("Enter location ID: ")
                functions.addProduct(connect, product_ID, productName, artNum, theType, stock, location)
            case "5", True:
                product_ID = input("Enter product ID: ")
                functions.showProductStock(connect, product_ID)
            case "6", True:
                functions.showAllProducts(connect)
            case "7", True:
                ID = input("Enter product ID: ")
                functions.showProductStock(connect, ID)
            case "8", True:
                searchTerm = input("Enter search term: ")
                functions.searchForProduct(connect, searchTerm)
            
            case "9", True:
                functions.showPickOrderDetails(connect)
            case "10", True:
                functions.showProductsLowInStock(connect)
            case "11", True:
                connect = functions.closeConnection(connect)
                connected = False
            case "12", _:
                functions.quit(connect)
                exit = True
            case _, False:
                print("Please connect to the database first.")
                input("Press Enter to return to main menu...")
            case _, True:
                print("Invalid selection. Please try again.")
                input("Press Enter to return to main menu...")
        

if __name__ == "__main__":
    main()