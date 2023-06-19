from databaseConnection import dbConnection

myDatabase, myCursor = dbConnection()



def flagQueryResult(returnValue,myCursor,gmbDataTableName,category):

    returnList = []
    flagQuery = f'select {returnValue} from {gmbDataTableName} where {returnValue}_done_flag = 1 and category = "{category}"'
    
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

def flagStartQueryResult(returnValue,myCursor,gmbDataTableName,category):

    returnList = []
    flagQuery = f'select distinct {returnValue} from {gmbDataTableName} where {returnValue}_start_flag = 1 and category = "{category}" and {returnValue}_done_flag is null'
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
    print(returnList)
    return returnList


def districtFlagQueryResult(state,returnValue,myCursor,gmbDataTableName,category):

    returnList = []
    flagQuery = f'select {returnValue} from {gmbDataTableName} where {returnValue}_done_flag = 1 and state = "{state}" and category = "{category}"'
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
def flagInsertQuery(insertValue,value,myCursor,myDatabase,gmbDataTableName,category):
    if insertValue == 'pincode':
        insertFlagQuery = f'insert into {gmbDataTableName} ({insertValue},{insertValue}_done_flag,category) values ({value},1,"{category}")'
    else:
        insertFlagQuery = f'insert into {gmbDataTableName} ({insertValue},{insertValue}_done_flag,category) values ("{value}",1,"{category}")'
    try:
        myCursor.execute(insertFlagQuery)
        myDatabase.commit()
    except Exception as e:
        myDatabase,myCursor = dbConnection()
        myCursor.execute(insertFlagQuery)
        myDatabase.commit()
    print(f'insertion done {value}')

def flagStartInsertQuery(insertValue,value,myCursor,myDatabase,gmbDataTableName,category):
    if insertValue == 'pincode':
        insertFlagQuery = f'insert into {gmbDataTableName} ({insertValue},{insertValue}_start_flag,category) values ({value},1,"{category}")'
    else:
        insertFlagQuery = f'insert into {gmbDataTableName} ({insertValue},{insertValue}_start_flag,category) values ("{value}",1,"{category}")'
    try:
        myCursor.execute(insertFlagQuery)
        myDatabase.commit()
    except Exception as e:
        myDatabase,myCursor = dbConnection()
        myCursor.execute(insertFlagQuery)
        myDatabase.commit()
    print(f'insertion done {value}')

def districtFlagInsertQuery(state,insertValue,value,myCursor,myDatabase,gmbDataTableName,category):
    if insertValue == 'pincode':
        insertFlagQuery = f'insert into {gmbDataTableName} ({insertValue},{insertValue}_done_flag,category) values ({value},1,"{category}")'
    else:
        insertFlagQuery = f'insert into {gmbDataTableName} ({insertValue},{insertValue}_done_flag,state,category) values ("{value}",1,"{state}","{category}")'
    try:
        myCursor.execute(insertFlagQuery)
        myDatabase.commit()
    except Exception as e:
        myDatabase,myCursor = dbConnection()
        myCursor.execute(insertFlagQuery)
        myDatabase.commit()
    print(f'insertion done {value} {state}')


def user_state_query(user_state_table_name,myCursor):
    query = f'select user_id,state from {user_state_table_name} where state is not null and state != "None"'
    return_dict = {}
    state_list = []
    try:
        myCursor.execute(query)
        allstate = myCursor.fetchall()
        # print(allstate)
    except:
        try:
            myDatabase, myCursor = dbConnection()
            myCursor.execute(query)
            allstate = myCursor.fetchall()
            # print(allstate)
        except Exception as e:
            print(e)
    try:
        for state in allstate:
            return_dict[state[0]] = state[1]
            state_list.append(state[1])
        # print(return_dict)
        return return_dict,state_list
    except:
        return None
def update_state_in_user_table(user_id,user_state_table_name,state,myCursor,myDatabase):
    query = f'update {user_state_table_name} set state = "{state}" where user_id = {user_id}'
    try:
        myCursor.execute(query)
        myDatabase.commit()
    except:
        try:
            myDatabase,myCursor = dbConnection()
            myCursor.execute(query)
            myDatabase.commit()
        except Exception as e:
            print(e)
def start_update_flag(gmbDataTableName,myCursor,myDatabase,category,state):
    query = f'insert into {gmbDataTableName} (state,state_start_flag,category) values ("{state}",1,"{category}")'
    try:
        myCursor.execute(query)
        myDatabase.commit()
    except:
        try:
            myDatabase,myCursor = dbConnection()
            myCursor.execute(query)
            myDatabase.commit()
        except Exception as e:
            print(e)





if __name__ == '__main__':

    myDatabase, myCursor = dbConnection()
    
    # countries= flagQueryResult(returnValue= 'pincode', myCursor= myCursor)
    flagInsertQuery(insertValue= 'district', value= 'godda',myCursor= myCursor, myDatabase= myDatabase)
    # print(countries)


