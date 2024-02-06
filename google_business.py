
import re
from HeadlessDriver import headlessDriver
from databaseConnection import dbConnection
from extract_business_details_from_google_map import searchNearbyPlaces
from test import flagQueryResult, flagInsertQuery,districtFlagQueryResult,districtFlagInsertQuery,flagStartInsertQuery,flagStartQueryResult,user_state_query,update_state_in_user_table,start_update_flag
from retry import retry
import os
import json
from table_checking import is_table_exist_and_create
import time
from niche_details import *
#location Fetching ................

def get_location(myCursor,location_table_name,status,category):
    if status == "not_start":
        query = f"select * from {location_table_name} where location is not null and location !='None' and location_flag_start is null and location_flag_stop is null order by rand() limit 1"
    elif status == "start":
        query = f"select * from {location_table_name} where location is not null and location !='None' and location_flag_start = 1 and location_flag_stop is null order by rand() limit 1"
    elif status == "stop":
        query = f"select * from {location_table_name} where location is not null and location !='None' and location_flag_start = 1 and location_flag_stop = 1 order by rand() limit 1"

    try:
        myCursor.execute(query)
        location = myCursor.fetchall()
    except:
        try:
            myDatabase, myCursor = dbConnection()
            myCursor.execute(query)
            location = myCursor.fetchall()
        except Exception as e:
            print(e)
            
    try:
        location = location[0] 
        location_id = location[0]
        # pincode = location[1]

        pincode = 0
        address = location[2]
        # district_id = location[3]
        district_id = 0
        district = "None"

        # district = location[4]
        state_id = location[5]
        state = location[6]
        country_id = location[7]
        country = location[8]
        city = location[11]  
        timezone = location[12]
        loc = {"location_count":1,"location_id":location_id,"pincode":pincode,"address":address,"district_code":district_id,"district":district,"state_code":state_id,"state":state,"country_code":country_id,"country":country,"city":city,"timezone":timezone} 
        print('$$$ inside while loop')
        print(loc)
        return loc
    except:
        print('here i am')
        return {"location_count":0}

# get count of not started location................

def get_location_not_start_count(myCursor,location_table_name,category):
    query = f"select count(*) from {location_table_name} where location is not null and location !='None' and location_flag_start is null and location_flag_stop is null"
    try:
        myCursor.execute(query)
        location_count = myCursor.fetchall()
    except:
        try:
            myDatabase,myCursor = dbConnection()
            myCursor.execute(query)
            location_count = myCursor.fetchall()
        except Exception as e:
            print(e)
    
    return location_count[0][0]

# update location start/stop flag .........................

def update_location_flag(myCursor,myDatabase,status,location_id,location_table_name,category):
    if status =='start':
        st = status
        query = f" update {location_table_name} set location_flag_start = 1 where location_id = {location_id}"
    elif status =='stop':
        st= status
        query = f" update {location_table_name} set location_flag_stop = 1 where location_id = {location_id}"
    
    try:
        myCursor.execute(query)
        myDatabase.commit()
        print(f"{location_id} flag {st} insertion is done")
    except:
        try:
            myDatabase, myCursor = dbConnection()
            myCursor.execute(query)
            myDatabase.commit()
            print(f"{location_id} flag {st} insertion is done")
        except Exception as e:
            print(e)
            
#<-----------storing active address into address.txt------------------->
def store_address_into_file(loc):
    with open('address.txt','w') as f:
        f.write(str(loc))
        f.close()
#<-----------fetching pending address from address.txt ------------------->
def fetch_address_from_address_text_file():
    with open('address.txt','r') as f:
        loc = f.readline()
        f.close()
    if len(loc)>0:
        print('location is pending ...')
        loc = loc.replace("'","\"")
        loc = json.loads(loc)
        return loc, len(loc)
    else:
        print('Not having any pending location ...')
        return {"nothing":0},len(loc),
#<-----------------clear address.txt file------------->
def clear_address_text_file():
    with open('address.txt','w') as f:
        pass
#<--------checking location is in progress-------->
def check_is_location_in_progress(myCursor,location_id,location_in_progress_table):
    query = f'select * from {location_in_progress_table} where location_id = {location_id}'
    try:
        myCursor.execute(query)
        data = myCursor.fetchall()
    except:
        myDatabase,myCursor = dbConnection()
        myCursor.execute(query)
        data = myCursor.fetchall()
    if data:
        return True
    else:
        return False

#<---------check and assigning location-------->

def is_location_in_progress(myDatabase,myCursor,location_in_progress_table,instance_id,loc):
    location_id= loc['location_id']
    is_in_progress =  check_is_location_in_progress(myCursor= myCursor, location_id= location_id, location_in_progress_table= location_in_progress_table)

    print(is_in_progress)
    if not is_in_progress:
        
        location_id= loc['location_id']

        update_status =  update_location_id_into_location_in_progress(myDatabase= myDatabase,myCursor= myCursor,location_id= location_id,instance_id= instance_id,location_in_progress_table= location_in_progress_table)
        
        return False
    else:
        return True
        
#<------------update location id into location in progress table----------->

def update_location_id_into_location_in_progress(myDatabase,myCursor,location_id,instance_id,location_in_progress_table):
    update_query = f'update {location_in_progress_table} set  location_id = {location_id} where id = {instance_id}'
    
    try:
        myCursor.execute(update_query)
        myDatabase.commit()
        return True
    except Exception as e:
        if 'Duplicate entry' not in str(e):
            
            try:
                myDatabase,myCursor = dbConnection()
                myCursor.execute(update_query)
                myDatabase.commit()
                
                return True
            except:
                return False
        return False


def create_new_instance_id(myDatabase,myCursor,location_id,instance_id,location_hold_table):
    insert_query = f'insert into {location_hold_table} (id,location_id) values ({instance_id},{location_id})'

    try:
        myCursor.execute(insert_query)
        myDatabase.commit()
    except:
        try:
            myDatabase,myCursor = dbConnection()
            myCursor.execute(insert_query)
            myDatabase.commit()
            
        except:
            pass
#<----------insert and replace data from data.csv to database------------>
@retry()
def insert_and_replace_data_csv_file(myCursor,myDatabase,gmbDataTableName,data_file_name):

    #Generating query in data.csv file

    with open(data_file_name,'r') as f:
        query = f.readline()

    finalQuery = f'replace into {gmbDataTableName} (gl_website,gl_business_name,gl_ratings,gl_telephone,gl_address,gl_gmb_photos_count,gl_reviews,pincode,category,gmb_category,country,state,district,gl_url,gl_url_done_flag,country_code,state_code,district_code,city,timezone) values {query.removeprefix(",")}'
   
    #updating data into database
    try:
        myCursor.execute(finalQuery)
        myDatabase.commit()
        print('All Data Insertion Done')
        f.close()

        with open(data_file_name,'w') as f:
            pass
        f.close()
        print('Data file clear')

    except:
        try:
            myDatabase,myCursor = dbConnection()
            myCursor.execute(finalQuery)
            myDatabase.commit()
            print('All Data Insertion Done')
            f.close()

            with open(data_file_name,'w') as f:
                pass
            f.close()
            print('Data file clear')
        except Exception as e:
            print(e)

#<------- checking data.csv file --------->
def check_data_file_having_any_data(data_file_name):

    with open(data_file_name,'r') as checkDataFile:
        data = checkDataFile.readline()
    if data:
        checkDataFile.close()
        return True
    else:
        checkDataFile.close()
        return False

# main function ................................
# @retry()
def main_function():

#<----------static variable declearation------------->
   
    myDatabase, myCursor = dbConnection()
    time.sleep(6)
    is_table_exist_and_create(myDatabase= myDatabase, myCursor= myCursor, category= category,country = country , country_code= country_code) 
    time.sleep(3)

#<----------fetching not start location's counts------------->

    location_count = get_location_not_start_count(myCursor= myCursor,location_table_name= location_table,category= category)
    
    while location_count>0:

#<----------condition 1 location_flag_start =1 and location_flag_stop = null------------->
        status = 'start'

        data_file_status = check_data_file_having_any_data(data_file_name)
        if data_file_status:
            print('Having Panding Data ...')
            insert_and_replace_data_csv_file(myCursor,myDatabase,gmbDataTableName,data_file_name)
            print('Pending data insertion done ...')
        else:
            print('Not Having any panding data to insert')

        loc,lenloc = fetch_address_from_address_text_file()
        if lenloc>0:
            loc = loc
            

          
        else:
#<----------condition 1 location_flag_start = null and location_flag_stop = null------------->
            status = 'not_start'
            

            loc = get_location(myCursor= myCursor, location_table_name= location_table, status= status,category= category)
#<-----------checking location is in progress or not--------------------------------------->
            location_in_progress_status = is_location_in_progress(myDatabase= myDatabase,myCursor= myCursor,location_in_progress_table= location_in_progress_table,instance_id= instance_id,loc= loc)
            while location_in_progress_status:
                status = 'not_start'
                print('I am inside while loop')

                loc = get_location(myCursor= myCursor, location_table_name= location_table, status= status,category= category)

                
                location_in_progress_status = is_location_in_progress(myDatabase= myDatabase,myCursor= myCursor,location_in_progress_table= location_in_progress_table,instance_id= instance_id,loc= loc)
                if location_in_progress_status:
                    print(f"$$$$$$$$$$$$")
                    print(loc)
                    print(f"$$$$$$$$$$$$")
            #<-------- confliction------->

            # 1205 (HY000): Lock wait timeout exceeded; try restarting transaction
            

#<----------updating location_flag_start------------->

            status= 'start'

            update_location_flag(myCursor= myCursor, myDatabase= myDatabase, status= status,location_id= loc['location_id'], location_table_name= location_table, category= category)

#-----------creating and storing static location file--------->
            store_address_into_file(loc)

#<----------scrapping data from google map------------->
        print(f'start: {loc["address"]}')
        
        try:
            searchNearbyPlaces(data_file_name= data_file_name,address= loc['address'],
                                category= category,
                                country= loc['country'],
                                country_id= loc['country_code'],
                                state= loc['state'],
                                state_id= loc['state_code'],
                                district= loc['district'],
                                district_id= loc['district_code'],
                                myDatabase= myDatabase,
                                myCursor= myCursor,
                                gmbDataTableName= gmbDataTableName,
                                city= loc['city'],
                                timezone = loc['timezone'])

    #<----------updating location_flag_stop------------->

            status= 'stop'

            #inserting Data into Database

            insert_and_replace_data_csv_file(myCursor,myDatabase,gmbDataTableName,data_file_name)
        except Exception as e:
            print(e)

        update_location_flag(myCursor= myCursor, myDatabase= myDatabase, status= status,location_id= loc['location_id'], location_table_name= location_table, category= category)

#------------deleting static location file-------------------->
        clear_address_text_file()   

#<----------fetching not start location's counts------------->
        location_count = get_location_not_start_count(myCursor= myCursor,location_table_name= location_table,category= category)

if __name__ == '__main__':
   
    main_function()
    # print(location)

   
    # print(location_count)

        


