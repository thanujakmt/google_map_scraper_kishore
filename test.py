from databaseConnection import dbConnection

myDatabase, myCursor = dbConnection()



def flagQueryResult(returnValue,myCursor,gmbDataTableName):

    returnList = []
    flagQuery = f'select {returnValue} from {gmbDataTableName} where {returnValue}_done_flag = 1'
    try:
        myCursor.execute(flagQuery)
        flagResult = myCursor.fetchall()
    except Exception as e:
        print(e)
        myDatabase, myCursor = dbConnection()
        myCursor.execute(flagQuery)
        flagResult = myCursor.fetchall()

    for flag in flagResult:
        returnList.append(flag[0])
    return returnList
def flagInsertQuery(insertValue,value,myCursor,myDatabase,gmbDataTableName):
    if insertValue == 'pincode':
        insertFlagQuery = f'insert into {gmbDataTableName} ({insertValue},{insertValue}_done_flag) values ({value},1)'
    else:
        insertFlagQuery = f'insert into {gmbDataTableName} ({insertValue},{insertValue}_done_flag) values ("{value}",1)'
    try:
        myCursor.execute(insertFlagQuery)
        myDatabase.commit()
    except Exception as e:
        myDatabase,myCursor = dbConnection()
        myCursor.execute(insertFlagQuery)
        myDatabase.commit()
    print(f'insertion done {value}')


if __name__ == '__main__':

    myDatabase, myCursor = dbConnection()
    
    # countries= flagQueryResult(returnValue= 'pincode', myCursor= myCursor)
    flagInsertQuery(insertValue= 'district', value= 'godda',myCursor= myCursor, myDatabase= myDatabase)
    # print(countries)


