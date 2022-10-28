

import re
from HeadlessDriver import headlessDriver
from databaseConnection import dbConnection
from extract_business_details_from_google_map import searchNearbyPlaces
from test import flagQueryResult, flagInsertQuery
from retry import retry

def userchoiceData(country,state,district,category,myCursor,myDatabase,gmbDataTableName):
    returnDict={}
    searchQuery = f'select pincode,location from usa_location_meta_data where state= "{state}" and district = "{district}" and country = "{country}"'
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
        print(pincode)
        print(address)
        pincodeDoneResult = flagQueryResult(returnValue= 'pincode', myCursor= myCursor, gmbDataTableName= gmbDataTableName)
        if pincode in pincodeDoneResult:
            continue
        searchNearbyPlaces(address=address,category= category,myDatabase= myDatabase,myCursor= myCursor,country= country, state= state, district= district, gmbDataTableName= gmbDataTableName)

        flagInsertQuery(insertValue= 'pincode', value= pincode,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName)
        
        
    flagInsertQuery(insertValue= 'district', value= district,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName)
    # flagInsertQuery(insertValue= 'state', value= state,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName)
    # flagInsertQuery(insertValue= 'country', value= country,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName)

def userchoiceDataTwo(country,state,category,myCursor,myDatabase,gmbDataTableName):
    returnDict={}

    districtQuery = f'select district_name from district where state_name = "{state}" and country_name = "{country}"'
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
        districtDoneResult = flagQueryResult(returnValue= 'district', myCursor= myCursor,gmbDataTableName=gmbDataTableName)
        if district in districtDoneResult:
            continue

        searchQuery = f'select pincode,location from usa_location_meta_data where state= "{state}" and district = "{district}" and country = "{country}"'
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
            print(pincode)
            print(address)
            pincodeDoneResult = flagQueryResult(returnValue= 'pincode', myCursor= myCursor, gmbDataTableName= gmbDataTableName)
            if pincode in pincodeDoneResult:
                continue
            searchNearbyPlaces(address=address,category= category,myDatabase= myDatabase,myCursor= myCursor,country= country, state= state, district= district, gmbDataTableName= gmbDataTableName)

            flagInsertQuery(insertValue= 'pincode', value= pincode,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName)
            
            
        flagInsertQuery(insertValue= 'district', value= district,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName)
    flagInsertQuery(insertValue= 'state', value= state,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName)
    # flagInsertQuery(insertValue= 'country', value= country,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName)
   
    
    

@retry()
def getAddress(addressTableName,gmbDataTableName):
    # category = input("Enter category : ")
    category = 'dentist'
    print(''' Enter the choice 
    1. Manualy Enter Country, State, And District.
    2. Manualy Enter Country,Satate .
    3. Automtically takes all the inputs. ''')

    myDatabase, myCursor = dbConnection()
    # userchoice = int(input("---> "))
    userchoice = 2
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
        state = 'new york'
        userchoiceDataTwo(country= country,state= state,category=category,myDatabase= myDatabase, myCursor= myCursor,gmbDataTableName=gmbDataTableName)
    else:
        countryQuery = f'select country_name from country'
        myCursor.execute(countryQuery)
        countries = myCursor.fetchall()
        for country in countries:
            country = country[0]
            countriesDoneResult = flagQueryResult(returnValue= 'country',myCursor= myCursor,gmbDataTableName = gmbDataTableName)

            # country = 'United States of America'
            if country in countriesDoneResult:
                continue

            stateQuery = f'select state_name from state where country_name = "{country}"'


            myCursor.execute(stateQuery)
            states = myCursor.fetchall()



            for state in states:
                state = state[0]
                
                stateDoneResult = flagQueryResult(returnValue= 'state', myCursor= myCursor,gmbDataTableName= gmbDataTableName)
                if state in stateDoneResult:
                    continue

                districtQuery = f'select district_name from district where state_name = "{state}" and country_name = "{country}"'
                myCursor.execute(districtQuery)
                districts = myCursor.fetchall()

                for district in districts:
                    district = district[0]

                    districtDoneResult = flagQueryResult(returnValue= 'district', myCursor= myCursor,gmbDataTableName=gmbDataTableName)

                    if district in districtDoneResult:
                        continue

                    try:
                        searchAddressQuery = f'select pincode,location from {addressTableName} where state = "{state}" and district = "{district}"'
                        myCursor.execute(searchAddressQuery)
                        searchData = myCursor.fetchall()
                        # print(searchData)
                        for item in searchData:
                            pincode = (item[0])
                            address = (item[1])
                            print(pincode)
                            print(address)

                            pincodeDoneResult = flagQueryResult(returnValue= 'pincode', myCursor= myCursor,gmbDataTableName= gmbDataTableName)

                            if pincode in pincodeDoneResult:
                                continue

                            searchNearbyPlaces(address=address,category= category,myDatabase= myDatabase,myCursor= myCursor,country= country, state= state, district= district,gmbDataTableName = gmbDataTableName)
                            # returnDict[pincode] = address
                            flagInsertQuery(insertValue= 'pincode', value= pincode,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName)
                        # print(returnDict)
                        flagInsertQuery(insertValue= 'district', value= district,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName)
                    except Exception as e:
                        print(e)
                flagInsertQuery(insertValue= 'state', value= state,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName)
            flagInsertQuery(insertValue= 'country', value= country,myCursor= myCursor, myDatabase= myDatabase,gmbDataTableName=gmbDataTableName)

if __name__ == '__main__':
    addressTableName = 'usa_location_meta_data'
    gmbDataTableName = 'gmp_master_table'
    getAddress(addressTableName,gmbDataTableName)