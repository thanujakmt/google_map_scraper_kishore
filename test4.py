from google_business import check_is_location_in_progress,update_location_id_into_location_in_progress,create_new_instance_id
from databaseConnection import dbConnection



def is_location_hold(myDatabase,myCursor,location_id,location_hold_table,instance_id):
    is_hold =  check_is_location_in_progress(myCursor= myCursor, location_id= location_id, location_hold_table= location_hold_table)

    print(is_hold)
    if is_hold:
        print('new address')
        location_id= 46

        valuesss=  update_location_id_into_location_in_progress(myDatabase= myDatabase,myCursor= myCursor,location_id= location_id,instance_id= instance_id,location_hold_table= location_hold_table)
        
        print(valuesss)

if __name__ == '__main__':
    # myDatabase,myCursor = dbConnection()
    # location_id = 1304
    # location_hold_table = 'location_hold'
    # location_in_progress_table = 'location_in_progress'
    # instance_id = 4

    # rr = check_is_location_in_progress(myCursor,location_id,location_in_progress_table)
    # print(rr)
    # is_location_hold(myDatabase= myDatabase, myCursor= myCursor, location_id= location_id, location_hold_table= location_hold_table, instance_id= instance_id)
    tt = False
    if not tt:
        print('aa')