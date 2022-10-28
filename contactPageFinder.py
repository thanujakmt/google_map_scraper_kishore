

from HeadlessDriver import headlessDriver
import re
import requests
from googleMapFinal import getEmail
from databaseConnection import dbConnection


# url= input('Enter URL')
def getContactPage(driver,wait,myCursor):
    driver,wait = headlessDriver(waitTime=10)
    for url in website:
        print(url[0])
        regex = r"^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/\n]+)"
        validUrl = re.finditer(regex,url[0])
        contact = ['contact','contactus','contacts','contact-us','contact-us.php','contactus.php','contact.php']
        print(validUrl)
        
        for item in validUrl:
            # print(item[0])
            for contact in contact:
                contactUrl= (f'{item[0]}/{contact}')
                print(contactUrl)
                if 'No Website' not in contactUrl:
                    status_code = 0
                    try:
                        status_code= requests.get(contactUrl).status_code
                    except Exception as e:
                        status_code = 0
                        print(e)
                    print(status_code)
                    if status_code == 200:
                        print(getEmail(website=contactUrl,driver= driver))
                        break
                if status_code == 200:
                    break
            
# def checkBusinessInDB(myCursor,gl_business_name):
#     query = 'select gl_business_name from usa_dent_db.dentist_table where pin_code = 10029'
#     myCursor.execute(query)
#     business = myCursor.fetchall()
#     for busin in business:
#         if gl_business_name == busin[0]:
#             print("yes")
#             return 1
#     print('no')
#     return 0  
# 
def checkBusinessNameInDB(myCursor,gl_business_name):
        query = f"select gl_business_name from usa_dent_db.dentist_table where gl_business_name = '{gl_business_name}'"
        myCursor.execute(query)
        businessName = myCursor.fetchall()
        if ((len(businessName))>=1):
            print(businessName[0][0])
            return 1
        else:
            return 0
             
if __name__ == '__main__':
    
    myDatabse,myCursor = dbConnection()
    gl_business_name = 'P & R Executive Dental Management'
    # query = f"select gl_business_name from usa_dent_db.dentist_table where gl_business_name = '{gl_business_name}'"
    # myCursor.execute(query)
    # businessName = myCursor.fetchall()
    # print(len(businessName))
    print(checkBusinessNameInDB(myCursor=myCursor, gl_business_name=gl_business_name))
    
    # val=checkBusinessInDB(myCursor=myCursor,gl_business_name=gl_business_name)
    # print(val)
    


    




    # query = 'select gl_website from dentist_table'
    # myCursor.execute(query)
    # website = myCursor.fetchall()
    # query = 'select gl_business_name from usa_dent_db.dentist_table where pin_code = 10029'
    # myCursor.execute(query)
    # business = myCursor.fetchall()
    # # print(business[0])
    # for busin in business:
    #     print(busin[0])
    #     if 'Dr. Gilda Duarte' in busin[0]:
    #         print("yes")

            
    # print("completed")



   

# driver, wait = headlessDriver()
# contact = ['contact','contactus','contacts']
# driver.get(url)


# ("((http|https)://)(www.)?" +
#              "[a-zA-Z0-9@:%._\\+~#?&//=]" +
#              "{2,256}\\.[a-z]" +
#              "{2,6}\\b([-a-zA-Z0-9@:%" +
#              "._\\+~#?&//=]*)")