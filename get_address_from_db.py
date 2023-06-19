

import re
from HeadlessDriver import headlessDriver
from databaseConnection import dbConnection
from extract_business_details_from_google_map import searchNearbyPlaces
from test import flagQueryResult, flagInsertQuery,districtFlagQueryResult,districtFlagInsertQuery,flagStartInsertQuery,flagStartQueryResult,user_state_query,update_state_in_user_table,start_update_flag
from retry import retry



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

@retry()
def userchoiceData(country,state,district,category,myCursor,myDatabase,gmbDataTableName):
    returnDict={}
    searchQuery = f'select pincode,location,district_id,state_id,country_id,city from {addressTableName} where state= "{state}" and district = "{district}" and country = "{country}"'
    try:
        myCursor.execute(searchQuery)
        searchData = myCursor.fetchall()
    except Exception as e:
        print(e)
        myDatabase, myCursor = dbConnection()
        myCursor.execute(searchQuery)
        searchData = myCursor.fetchall()
    for item in searchData:
        pincode = (item[0])
        address = (item[1])
        district_id =(item[2])
        state_id = (item[3])
        country_id = (item[4])
        city = (item[5])
        print(pincode)
        print(address)
        pincodeDoneResult = flagQueryResult(returnValue= 'pincode', myCursor= myCursor, gmbDataTableName= gmbDataTableName,category= category)
        if pincode in pincodeDoneResult:
            continue
        returnVal = searchNearbyPlaces(address=address,category= category,myDatabase= myDatabase,myCursor= myCursor,country= country,country_id= country_id, state= state, state_id = state_id,district= district,district_id = district_id, gmbDataTableName= gmbDataTableName,city = city)
        if returnVal == 0:
            returnVal = searchNearbyPlaces(address=address,category= category,myDatabase= myDatabase,myCursor= myCursor,country= country,country_id= country_id, state= state, state_id = state_id,district= district,district_id = district_id, gmbDataTableName= gmbDataTableName,city = city)

        flagInsertQuery(insertValue= 'pincode', value= pincode,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName,category= category)
        
        
    flagInsertQuery(insertValue= 'district', value= district,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName,category= category)
    # flagInsertQuery(insertValue= 'state', value= state,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName)
    # flagInsertQuery(insertValue= 'country', value= country,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName)
@retry()
def userchoiceDataTwo(country,state,category,myCursor,myDatabase,gmbDataTableName):
    returnDict={}

    districtQuery = f'select district_name,d_id,s_id,c_id  from district where state_name = "{state}" and country_name = "{country}"'
    try:
        myCursor.execute(districtQuery)
        districts = myCursor.fetchall()
    except Exception as e:
        print(e)
        myDatabase, myCursor = dbConnection()
        myCursor.execute(districtQuery)
        districts = myCursor.fetchall()

    for district in districts:
        district = district[0]
        districtDoneResult = districtFlagQueryResult(state = state,returnValue= 'district', myCursor= myCursor,gmbDataTableName=gmbDataTableName,category= category)
        if district in districtDoneResult:
            continue

        searchQuery = f'select pincode,location,district_id,state_id,country_id,city from {addressTableName} where state= "{state}" and district = "{district}" and country = "{country}"'
        try:
            myCursor.execute(searchQuery)
            searchData = myCursor.fetchall()
        except Exception as e:
            print(e)
            myDatabase, myCursor = dbConnection()
            myCursor.execute(searchQuery)
            searchData = myCursor.fetchall()
        for item in searchData:
            pincode = (item[0])
            address = (item[1])
            district_id =(item[2])
            state_id = (item[3])
            country_id = (item[4])
            city = (item[5])
            print(pincode)
            print(address)
            pincodeDoneResult = flagQueryResult(returnValue= 'pincode', myCursor= myCursor, gmbDataTableName= gmbDataTableName,category= category)
            if pincode in pincodeDoneResult:
                continue
            returnVal = searchNearbyPlaces(address=address,category= category,myDatabase= myDatabase,myCursor= myCursor,country= country,country_id= country_id, state= state, state_id = state_id,district= district,district_id = district_id, gmbDataTableName= gmbDataTableName,city = city)
            if returnVal == 0:
               returnVal =  searchNearbyPlaces(address=address,category= category,myDatabase= myDatabase,myCursor= myCursor,country= country,country_id= country_id, state= state, state_id = state_id,district= district,district_id = district_id, gmbDataTableName= gmbDataTableName,city = city)

            flagInsertQuery(insertValue= 'pincode', value= pincode,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName,category= category)
            
            
        districtFlagInsertQuery(state = state, insertValue= 'district', value= district,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName,category= category)
    flagInsertQuery(insertValue= 'state', value= state,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName,category= category)
    # flagInsertQuery(insertValue= 'country', value= country,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName)
@retry()
def auto_state(category,user_id,user_state_table_name,gmbDataTableName,myDatabase, myCursor):

    countryQuery = f'select country_name from country'
    try:
        myCursor.execute(countryQuery)
        countries = myCursor.fetchall()
    except:
        myDatabase,myCursor = dbConnection()
        myCursor.execute(countryQuery)
        countries = myCursor.fetchall()

    for country in countries:
            
        country = country[0]
        countriesDoneResult = flagQueryResult(returnValue= 'country',myCursor= myCursor,gmbDataTableName = gmbDataTableName,category= category)
           
            # country = 'United States of America'
        if country in countriesDoneResult:
            continue

        stateQuery = f'select state_name from state where country_name = "{country}"'

        try:
            myCursor.execute(stateQuery)
            states = myCursor.fetchall()
        except:
            myDatabase,myCursor = dbConnection()
            myCursor.execute(stateQuery)
            states = myCursor.fetchall()

            



        for state in states:
            state = state[0]
            print(state)
            if state == 'Virginia':
                continue
            user_agined_states,state_list = user_state_query(user_state_table_name= user_state_table_name, myCursor= myCursor)
            print(user_agined_states)
            stateDoneResult = flagQueryResult(returnValue= 'state', myCursor= myCursor,gmbDataTableName= gmbDataTableName,category= category)
                
            stateStartResult = flagStartQueryResult(returnValue = 'state',myCursor = myCursor,gmbDataTableName = gmbDataTableName,category = category)
           
            if state in stateDoneResult:
                    continue

            if state not in state_list and state not in stateDoneResult:
               
                if state != 'None' or state is not None:
                    
                    start_update_flag(gmbDataTableName,myCursor,myDatabase,category,state)
                    update_state_in_user_table(user_id,user_state_table_name,state,myCursor,myDatabase)
                   

                # if state not in stateStartResult:

                    

                #     if state != 'None' or state is not None:

                        # flagStartInsertQuery(insertValue = "state",value=state,myCursor= myCursor,myDatabase= myDatabase,gmbDataTableName = gmbDataTableName,category= category)
                    
                        
                    

            

            elif state in stateStartResult and state not in stateDoneResult and state in state_list:

                try:
                   
                    state = user_agined_states[user_id]
                    print(state)
                except:

                    continue

                

                    
                
            districtQuery = f'select district_name from district where state_name = "{state}" and country_name = "{country}"'
            try:
                myCursor.execute(districtQuery)
                districts = myCursor.fetchall()
            except:
                myDatabase,myCursor = dbConnection()
                myCursor.execute(districtQuery)
                districts = myCursor.fetchall()

            districtDoneResult = districtFlagQueryResult(state= state,returnValue= 'district', myCursor= myCursor,gmbDataTableName=gmbDataTableName,category= category)
            for district in districts:
                district = district[0]

                

                if district in districtDoneResult:
                    continue
                searchAddressQuery = f'select pincode,location,district_id,state_id,country_id,city from {addressTableName} where state = "{state}" and district = "{district}"'
                try:
                        
                    myCursor.execute(searchAddressQuery)
                    searchData = myCursor.fetchall()
                except:
                    myDatabase,myCursor = dbConnection()
                    myCursor.execute(searchAddressQuery)
                    searchData = myCursor.fetchall()
                        # print(searchData)
                for item in searchData:
                    pincode = (item[0])
                    address = (item[1])
                    district_id =(item[2])
                    state_id = (item[3])
                    country_id = (item[4])
                    city = (item[5])
                    print(pincode)
                    print(address)
                    pincodeDoneResult = flagQueryResult(returnValue= 'pincode', myCursor= myCursor,gmbDataTableName= gmbDataTableName,category= category)
                    if pincode in pincodeDoneResult:
                        continue
                    returnVal = searchNearbyPlaces(address=address,category= category,myDatabase= myDatabase,myCursor= myCursor,country= country,country_id= country_id, state= state, state_id = state_id,district= district,district_id = district_id,gmbDataTableName = gmbDataTableName,city = city)
                    if returnVal == 0:
                        returnVal = searchNearbyPlaces(address=address,category= category,myDatabase= myDatabase,myCursor= myCursor,country= country,country_id= country_id, state= state, state_id = state_id,district= district,district_id = district_id,gmbDataTableName = gmbDataTableName,city = city)
                        # returnDict[pincode] = address
                    flagInsertQuery(insertValue= 'pincode', value= pincode,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName,category= category)
                        # print(returnDict)
                districtFlagInsertQuery(state = state, insertValue= 'district', value= district,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName,category= category)
            returnValues = check_exitsting_of_state(myCursor,state,category,gmbDataTableName) 
            if returnValues:      
                flagInsertQuery(insertValue= 'state', value= state,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName,category= category)
        # flagInsertQuery(insertValue= 'country', value= country,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName,category= category)


    


def getAddress(addressTableName,gmbDataTableName):
    # category = input("Enter category : ")
    category = 'remodeler'
    #user_id = 3
    user_id = 6
    user_state_table_name = 'gmp_script_instance_users'
    print(''' Enter the choice 
    1. Manualy Enter Country, State, And District.
    2. Manualy Enter Country,Satate .
    3. Automtically takes all the inputs. ''')

    myDatabase, myCursor = dbConnection()
    # userchoice = int(input("---> "))
    userchoice = 3
    returnDict = {}
    if userchoice == 1:
        country = input("Enter Country :")
        state = input("Enter the state : ")
        district = input("Enter the district : ")

        
        
        userchoiceData(country= country,state= state,category=category, district= district,myDatabase= myDatabase, myCursor= myCursor,gmbDataTableName=gmbDataTableName)
    elif userchoice == 2:
        # country = input("Enter Country: ")
        # state = input("Enter State: ")

        country = 'united states of america'
        state = 'georgia'
        userchoiceDataTwo(country= country,state= state,category=category,myDatabase= myDatabase, myCursor= myCursor,gmbDataTableName=gmbDataTableName)
    else:

        auto_state(category = category,user_id = user_id,user_state_table_name = user_state_table_name,gmbDataTableName= gmbDataTableName,myDatabase = myDatabase, myCursor= myCursor)
        
if __name__ == '__main__':
    addressTableName = 'usa_location_meta_data'
    gmbDataTableName = 'gmp_master_table'
    getAddress(addressTableName = addressTableName,gmbDataTableName= gmbDataTableName)
