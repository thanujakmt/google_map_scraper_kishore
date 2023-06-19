def check_exitsting_of_state(myCursor,state,category,gmbDataTableName):

    query = f"select state, state_done_flag from {gmbDataTableName} where state = '{state}' and category = '{category}' and state_done_flag = 1;"
    try:
        myCursor.execute(query)
        state_exist_in_db = myCursor.fetchall()
    except:
        
        myDatabase, myCursor = dbConnection()
        myCursor.execute(query)
        state_exist_in_db = myCursor.fetchall()

    no_of_states = (len(state_exist_in_db))

    if no_of_states == 0:
        return True
    else:
        return False