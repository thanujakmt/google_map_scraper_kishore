import mysql.connector
from retry_custom import retryFunction
from niche_details import *

@retryFunction
def dbConnection():
    # print(db_credential)
    user = db_credential[niche]['user']
    print(user)
    myDatabase = mysql.connector.connect(
        host = "helenzys-mysql-dev.clyhoefsujtn.us-east-1.rds.amazonaws.com",
        # user = "usa_dent_db",
        # password = "sw3etSnow21",
        # database = "usa_dent_db"

        # user = "daycare",
        # password = "$illyAnt88",
        # database = "daycare_business_db"
        user = db_credential[niche]['user'],
        password = db_credential[niche]['password'],
        database = db_credential[niche]['database']
        
        

        # host = "localhost",
        # user = "root",
        # password = "Power1234",
        # database = "usa_dent_db",
        # auth_plugin='mysql_native_password'
    )
    myCursor = myDatabase.cursor()
    return myDatabase, myCursor

if __name__ == '__main__':
    dbConnection()
   