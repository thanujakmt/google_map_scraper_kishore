import mysql.connector
from retry_custom import retryFunction

@retryFunction
def dbConnection():
    myDatabase = mysql.connector.connect(
        host = "helenzys-mysql-dev.clyhoefsujtn.us-east-1.rds.amazonaws.com",
        user = "usa_dent_db",
        password = "sw3etSnow21",
        database = "usa_dent_db"
    )
    myCursor = myDatabase.cursor()
    return myDatabase, myCursor

if __name__ == '__main__':
    dbConnection()