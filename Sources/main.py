import functions
import os
import mysql.connector
def main():
    #Main entry point of the program.
    exit = False
    connected = False
    connect = None
    #Program loop with menu and selection.
    while not exit:
        functions.menu(connected)
        selection = input("Please select an option: ")
        match selection, connected:
            case "1", False:
                #Connect to the database(required before other functionality can be used)
                os.system('cls' if os.name == 'nt' else 'clear')
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
                #Show all pick orders with user assigned to them
                os.system('cls' if os.name == 'nt' else 'clear')
                functions.showAssignedOrders(connect)
            case "3", True:
                #Add a new pick order to the database
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Listing available products:")
                functions.showAllProducts(connect)
                user_ID = input("Enter user ID(Leave empty for auto-assignment): ")
                productID = input("Enter product ID: ")
                quantity = input("Enter quantity: ")
                priority = input("Enter priority: ")
                status = input("Enter status: ")
                functions.addPickOrder(connect, priority, status, productID, quantity, user_ID if user_ID != '' else None)
            case "4", True:
                #Show the status of all orders
                os.system('cls' if os.name == 'nt' else 'clear')
                functions.showOrderStatus(connect)
            case "5", True:
                #Add a new product to the database
                os.system('cls' if os.name == 'nt' else 'clear')
                productName = input("Enter product name: ")
                artNum = input("Enter article number: ")
                theType = input("Enter product type: ")
                stock = input("Enter stock quantity: ")
                functions.addProduct(connect, productName, artNum, theType, stock)
            case "6", True:
                #Shows all produucts in the database
                os.system('cls' if os.name == 'nt' else 'clear')
                functions.showAllProducts(connect)
            case "7", True:
                #Show the stock of a product
                os.system('cls' if os.name == 'nt' else 'clear')
                ID = input("Enter product ID: ")
                functions.showProductStock(connect, ID)
            case "8", True:
                #Search for a product by name or article number
                os.system('cls' if os.name == 'nt' else 'clear')
                searchTerm = input("Enter search term: ")
                functions.searchForProduct(connect, searchTerm)
            
            case "9", True:
                #Show details of a pick order.
                os.system('cls' if os.name == 'nt' else 'clear')
                pickOrd_ID = input("Enter PickOrder ID: ")
                functions.showPickOrderDetails(connect, pickOrd_ID)
            case "10", True:
                #Show which products are low in stock (<=5)
                os.system('cls' if os.name == 'nt' else 'clear')
                functions.showProductsLowInStock(connect)
            case "11", True:
                #Close the connection to the database
                os.system('cls' if os.name == 'nt' else 'clear')
                connect = functions.closeConnection(connect)
                connected = False
            case "12", _:
                #Exit the program
                functions.quit(connect)
                exit = True
            case _, False:
                #Invalid selection if not connected to the database
                print("Please connect to the database first.")
                input("Press Enter to return to main menu...")
            case _, True:
                #Invalid selection if connected to the database
                print("Invalid selection. Please try again.")
                input("Press Enter to return to main menu...")
        

if __name__ == "__main__":
    main()