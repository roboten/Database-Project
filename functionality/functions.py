import mysql.connector

def connectToDatabase(hostIP,username, auth, dbName,):
    """Connect to the database."""
    return mysql.connector.connect(
        host=hostIP, user=username, password=auth, database=dbName)

#def addLocation(dbConnection, ID, zone, shelf, aisle):
#    """Add location to the database."""
#    dbConnection.query(""
#    return True