
import functions
import mysql.connector
def main():
    """Main entry point of the program."""
    ip = input("Enter database IP (default: localhost): ") or "localhost"
    username = input("Enter database username (default: admin): ") or "admin"
    password = input("Enter database password (default: password): ") or "password"
    dbName = input("Enter database name: ")
    connect = functions.connectToDatabase(ip, username, password, dbName)
    if connect.is_connected():
        print("Connected to database.")
        connect.close()

if __name__ == "__main__":
    main()