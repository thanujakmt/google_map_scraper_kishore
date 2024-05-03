
from urllib3 import disable_warnings
from HeadlessDriver import headlessDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from databaseConnection import dbConnection
import time
import re
import requests
from retry_custom import retryFunction

def get_gl_id_and_gl_website(myCursor,gmbDataTableName):
    query = f'select gl_id, gl_website from {gmbDataTableName} where gl_website != "No Website Found"'

    myCursor.execute(query)
    rowData = myCursor.fetchall()
    return rowData
    # print(rowData)
    
def updateQuery(myCursor,myDatabase,email,gl_id,gmbDataTableName,gl_email_flag):
    if email is not None:
        query = f'''update {gmbDataTableName} set gl_email2 = "{email}" ,{gl_email_flag} = 1 where gl_id = {gl_id}'''
    else:
        query = f'update {gmbDataTableName} set {gl_email_flag} = 0 where gl_id = {gl_id}'
    try:
        myCursor.execute(query)
        myDatabase.commit()
    except Exception as e:
        print(e)
        myDatabase, myCursor = dbConnection()

        myCursor.execute(query)
        myDatabase.commit()

    print(f'update is done {gl_id} ')

def skip_website(myCursor,gmbDataTableName):
    query = f'select gl_id from {gmbDataTableName} where gl_email2_done_flag = 1 or gl_custom_email2_done_flag = 1 or gl_custom_email2_done_flag = 0'

    try:
        myCursor.execute(query)
        row_gl_id = myCursor.fetchall()
    except Exception as e:
        print(e)
        myCursor.execute(query)
        row_gl_id = myCursor.fetchall()

    # print(all_gl_id)
    all_gl_id = []
    for item in row_gl_id:
        all_gl_id.append(item[0])
    return all_gl_id


def updateEmailInDB(rowData,driver,wait,myDatabase,myCursor,gmbDataTableName):
    all_gl_id = skip_website(myCursor= myCursor, gmbDataTableName= gmbDataTableName)

    for item in rowData:
        
        gl_id = item[0]
        if gl_id in all_gl_id:
            print(f'{gl_id} is skipped' )
            continue
        gl_website = item[1]
        print(gl_id)
        print(gl_website)

        email = getEmail(website= gl_website, driver= driver)

        if email is not None:
            gl_email_flag = 'gl_email2_done_flag'
            

            updateQuery(myCursor= myCursor,myDatabase = myDatabase,email =email,gl_id = gl_id,gmbDataTableName = gmbDataTableName,gl_email_flag= gl_email_flag)

        elif email is None:
            gl_email_flag = 'gl_custom_email2_done_flag'

            email = getContactPage(website= gl_website, driver= driver)
            if email is not None: 

                updateQuery(myCursor= myCursor,myDatabase = myDatabase,email =email,gl_id = gl_id,gmbDataTableName = gmbDataTableName,gl_email_flag= gl_email_flag)
            else : 

                updateQuery(myCursor= myCursor,myDatabase = myDatabase,email =email,gl_id = gl_id,gmbDataTableName = gmbDataTableName,gl_email_flag= gl_email_flag)
                



def getContactPage(website,driver):
    # driver,wait = headlessDriver(waitTime=10)
    
        # print(url[0])
        regex = r"^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/\n]+)"
        validUrl = re.finditer(regex,website)
        contact = ['contact','contactus','contacts','contact-us','contact-us.php','contactus.php','contact.php','contactus.html','about-us','aboutus']
        # print(validUrl)
        
        for item in validUrl:
            # print(item[0])
            for contact in contact:
                contactUrl= (f'{item[0]}/{contact}')
                print(contactUrl)
                if 'No Website' not in contactUrl:
                    status_code = 0
                    try:
                        status_code= requests.get(contactUrl , timeout= 2).status_code
                    except Exception as e:
                        status_code = 0
                        print(e)
                    print(status_code)
                    print("status check done")
                    if status_code == 200:
                        print("checking email")
                        email = (getEmail(website=contactUrl,driver= driver))
                        
                        
                if status_code == 200:
                    return email
                
            return None      

def getEmail(website,driver):
    try:
        print("page loading")
        driver.set_page_load_timeout(20)
        driver.get(website)
        print("page loding done")
        parsed_html = str(driver.page_source)
    except Exception as e:
        print(e)
    
    email_regex = re.compile(r'''(
                [a-zA-Z0-9._%+-]+
                @
                [a-zA-Z0-9.-]+
                (\.[a-zA-Z]{2,4})
                )''', re.VERBOSE)
    try:
        text = str(parsed_html)
        matches = set([groups[0] for groups in email_regex.findall(text)])
        return matches if matches else None
    except Exception as err:
        print(" {} \nFailed to read page!".format(err))
        return None

if __name__ == '__main__':
    driver, wait = headlessDriver(waitTime= 10)
    myDatabase, myCursor = dbConnection()
    gmbDataTableName = 'dentist_in_new_jersey'
    rowData = get_gl_id_and_gl_website(myCursor= myCursor, gmbDataTableName= gmbDataTableName)
    updateEmailInDB(rowData = rowData,driver = driver,wait= wait,myDatabase= myDatabase,myCursor = myCursor,gmbDataTableName= gmbDataTableName)

    # print(skip_website(myCursor= myCursor, gmbDataTableName= gmbDataTableName))
