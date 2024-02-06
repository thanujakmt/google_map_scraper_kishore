
from HeadlessDriver import headlessDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from loopers import loop
from selenium.webdriver.common.action_chains import ActionChains
# import pandas as pd
import re
import requests
# import neattext.functions as ntx
# from tkinter import Tk
from databaseConnection import dbConnection
from retry_custom import retryFunction
from retry import retry
import random

def webElementFinder(**kwargs):
    if kwargs['actionPerform'] == "send_keys":
        wait = kwargs['wait']
        xpath = kwargs['xpath']
        actionPerform = kwargs['actionPerform']
        actionData = kwargs['actionData']
    elif kwargs['actionPerform'] == 'click':
        wait = kwargs['wait']
        xpath = kwargs['xpath']
        actionPerform = kwargs['actionPerform']
    else:
        wait = wait
        xpath = xpath
        


    
    if actionPerform == 'send_keys' or actionPerform == 'click' or actionPerform == 'one':
        element=wait.until(EC.visibility_of_element_located((By.XPATH,f"{xpath}")))
    else:
        element=wait.until(EC.visibility_of_all_elements_located((By.XPATH,f"{xpath}")))
    

    if actionPerform == 'send_keys':
        element.send_keys(actionData)
    elif actionPerform == 'click':
        element.click()
    else:
        return element

def getContactPage(website,driver):
    # driver,wait = headlessDriver(waitTime=10)
    
        # print(url[0])
        regex = r"^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/\n]+)"
        validUrl = re.finditer(regex,website)
        contact = ['contact','contactus','contacts','contact-us','contact-us.php','contactus.php','contact.php']
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
                
            return 'No Email Found'
@retryFunction
def checkBusinessInBD(allPlace,myCursor,gmbDataTableName):
    searchBusiness =[]
    for g_map_url in allPlace:

        gl_url=(g_map_url.get_attribute('href'))
        query = f'''select gl_url from {gmbDataTableName} where gl_url = "{gl_url}"'''
        try:
            myCursor.execute(query)
            allBusin = myCursor.fetchall()
        except Exception as e:
            print(e)
            myDatabase,myCursor = dbConnection()
            try:
                myCursor.execute(query)
                allBusin = myCursor.fetchall()
            except Exception as e:
                print(e)
                print("Illegal mix of collations")

        print(allBusin)
        if (len(allBusin)) == 0:
                searchBusiness.append(g_map_url)
        print(len(searchBusiness))
    return searchBusiness   
         
# def checkBusinessNameInDB(myCursor,gl_business_name):
#     try:
#         query = f'''select gl_business_name from usa_dent_db.google_map where gl_business_name = "{gl_business_name}"'''
#         myCursor.execute(query)
#         businessName = myCursor.fetchall()
#     except Exception as e:
#         print(e)
#         time.sleep(4)
#         myDatabase,myCursor = dbConnection()
#     if ((len(businessName))>=1):
#         print(businessName[0][0])
#         return 1
#     else:
#         return 0        

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
# @retry()
def get_GMB_Details(url,driver,wait):

    # try:
    # driver.delete_all_cookies()
    driver.get(url)
    time.sleep(2)
    
    # except Exception as e:
    #     print(e)
    #     driver,wait = headlessDriver(waitTime=10)
    #     driver.refresh()
    #     try:
    #         driver.set_page_load_timeout(30)
    #         driver.get(url)
    #     except:
    #         driver.set_page_load_timeout(40)
    #         driver.get(url)
        
    
    try:
        action = ActionChains(driver)
        action.move_by_offset(100,100).perform()

        # business = wait.until(EC.visibility_of_element_located((By.XPATH,"//h1[@class='DUwDvf fontHeadlineLarge']"))).text
        bxpath = "//h1[contains(@class,'DUwDvf')]"
        old_bxpath = "//h1[@class='DUwDvf fontHeadlineLarge']"
        business = driver.find_element(By.XPATH,bxpath).text
        business = str(business).replace("'","").replace('"','')
        print(business)
        # businessInDb = checkBusinessNameInDB(myCursor= myCursor,gl_business_name= business)
        # if businessInDb == 0:
        try:
            gmb_category = driver.find_element(By.XPATH,"//button[@jsaction='pane.rating.category']").text
        except:
            gmb_category = "None"
        try:
            photos = str(driver.find_element(By.XPATH,"//div[@class='YkuOqf']").text).replace(' photos','')
        except:
            photos = '1'
                # allElee= wait.until(EC.visibility_of_all_elements_located((By.XPATH,"//div[@class='Io6YTe fontBodyMedium']")))
        try:
            # ratings = wait.until(EC.visibility_of_element_located((By.XPATH,"((//div[@class='LBgpqf']//div[@role='button']/span)[1]/span/span)[1]"))).text

            ratings = driver.find_element(By.XPATH,"(//div[@class='F7nice ']//span/span)[1]").text
        except: 
            ratings = '0'
        try:
            # reviews = str(wait.until(EC.visibility_of_element_located((By.XPATH,"//button[@jsaction='pane.rating.moreReviews']"))).text).replace(' reviews','').replace(' review','')

            reviews = str(driver.find_element(By.XPATH,"(//div[@class='F7nice ']/span)[2]").text.split('(')[1].split(")")[0])
        except:
            reviews = '0'
                # address = wait.until(EC.visibility_of_element_located((By.XPATH,"(//div[@class='Io6YTe fontBodyMedium'])[1]"))).text
        try:    
            # address = str(wait.until(EC.visibility_of_element_located((By.XPATH,"//button[@data-item-id='address']"))).get_attribute('aria-label')).replace('Address: ','')

            address = str(driver.find_element(By.XPATH,"//button[@data-item-id='address']").get_attribute('aria-label')).replace('Address: ','')
            address = address.replace("'","").replace('"','')
        except Exception as e:
            print(e)
            address = None
        try:
            # website = wait.until(EC.visibility_of_element_located((By.XPATH,"//a[@data-item-id='authority']"))).get_attribute('href')

            website = driver.find_element(By.XPATH,"//a[@data-item-id='authority']").get_attribute('href')
        except:
            website= None
                
            time.sleep(1)
        try:
            # telephone = str(wait.until(EC.visibility_of_element_located((By.XPATH,"(//button[@data-tooltip='Copy phone number'])[1]"))).get_attribute('data-item-id')).replace('phone:tel:','')

            telephone = str(driver.find_element(By.XPATH,"(//button[@data-tooltip='Copy phone number'])[1]").get_attribute('data-item-id')).replace('phone:tel:','')

                # telephone = wait.until(EC.visibility_of_element_located((By.XPATH,"//img[@src='//www.gstatic.com/images/icons/material/system_gm/1x/phone_gm_blue_24dp.png']"))).click()
                # telephone = Tk().clipboard_get()
                # time.sleep(1)
                # Tk().destroy()
                    
                
                # print(e)
        except Exception as e:
            print(e)
            telephone = None
        # if website != 'No Website Found':
        #     email = getContactPage(website=website,driver=driver)
        #     if email == 'No Email Found' or email == None:
        #         email = getEmail(website=website,driver=driver)
        # else: 
        #     email = 'No Email Found'
            
                
            
        gmbResultDict = {'gl_business_name':business,'gl_ratings':ratings,'gl_reviews':reviews,'gl_gmb_photos_count':photos,'gl_telephone':telephone,'gl_website':website,'gl_address':address,'gl_url':url,'gl_url_done_flag':1,"gmb_category":gmb_category}
        action.move_by_offset(-100,-100).perform()
        driver.delete_all_cookies()
        return gmbResultDict
        # else:
        #     time.sleep(4)
        #     action.move_by_offset(-100,-100).perform()
        #     return None
    except Exception as e:
        
        print(e)
        return None
@retryFunction  
def sendingDataToWebdriver(address,category):
    driver, wait = headlessDriver(waitTime= 10)
    

    driver.get('https://maps.google.com/')
    action = ActionChains(driver)

    time.sleep(4)
    action.move_by_offset(76,29)
    time.sleep(4)
    webElementFinder(wait = wait, xpath = "//input[@id='searchboxinput']", actionPerform = 'send_keys', actionData = address)
    # wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@id='searchboxinput']"))).send_keys(address)
    time.sleep(4)
    webElementFinder(wait = wait, xpath = "//button[@id='searchbox-searchbutton']", actionPerform = 'click')
    # wait.until(EC.visibility_of_element_located((By.XPATH,"//button[@id='searchbox-searchbutton']"))).click()
    action.move_by_offset(-76,-29)
    try:
        webElementFinder(wait = wait, xpath = "//div[contains(text(),'Nearby')]", actionPerform = 'click')
        # wait.until(EC.visibility_of_element_located((By.XPATH,"//div[contains(text(),'Nearby')]"))).click()
    except Exception as e:
        try:
            webElementFinder(wait = wait, xpath = "(//a[@class='hfpxzc'])[1]", actionPerform = 'click')
            # wait.until(EC.visibility_of_element_located((By.XPATH,"//div[@role='feed']/div[1]"))).click()
            time.sleep(2)

            # action.move_by_offset(-76,-29)
            webElementFinder(wait = wait, xpath = "//div[contains(text(),'Nearby')]", actionPerform = 'click')
            # wait.until(EC.visibility_of_element_located((By.XPATH,"//div[contains(text(),'Nearby')]"))).click()
        except:
            driver.get('https://maps.google.com/')
            webElementFinder(wait = wait, xpath = "//input[@id='searchboxinput']", actionPerform = 'send_keys', actionData = address)
            time.sleep(2)
            webElementFinder(wait = wait, xpath = "//img[@class='hCgzhd']", actionPerform = 'click')
            time.sleep(2)
            webElementFinder(wait = wait, xpath = "//div[contains(text(),'Nearby')]", actionPerform = 'click')



    time.sleep(4)
    webElementFinder(wait = wait, xpath = "//input[@id='searchboxinput']", actionPerform = 'send_keys', actionData = category)

    # wait.until(EC.visibility_of_element_located((By.XPATH,"//input[@id='searchboxinput']"))).send_keys(category)
    webElementFinder(wait = wait, xpath = "//button[@id='searchbox-searchbutton']", actionPerform = 'click')

    # wait.until(EC.visibility_of_element_located((By.XPATH,"//button[@id='searchbox-searchbutton']"))).click()
    time.sleep(4)
    # action = ActionChains(driver)

    action.move_by_offset(100,100).perform()
    s_val = [400,500,600,700,1000,1500]
    try:
        driver.find_element(By.XPATH,"//span[@class='HlvSq']")
        lastElement = 1
    except:
        lastElement = 0
    while lastElement == 0:
        
        query = f'''document.querySelector("div[aria-label='Results for {category}']").scrollBy(0,{random.choice(s_val)})'''
        try:
            driver.execute_script(query)
            time.sleep(2)
            # s_val = s_val + 20
        except:

            print("end")
            break
        try:
            ele= driver.find_element(By.XPATH,"//span[@class='HlvSq']")
            lastElement = 1
        except:
            lastElement = 0
    try:
        
        print(ele.text)
        restart = 0
    except:
        restart = 1
        print('dentist element not found')
    if restart ==0:
        allPlace = wait.until(EC.visibility_of_all_elements_located((By.XPATH,"//a[@class='hfpxzc']")))
        return driver, wait, action,allPlace
    else:
        driver.close()
        return None,None,None,None

def write_data_into_file(data_file_name,gmbResultDict,country,state,district,country_id,state_id,district_id,city,pin_code,category,timezone):
    try:
        listquery = f""",("{gmbResultDict['gl_website']}","{gmbResultDict['gl_business_name']}","{gmbResultDict['gl_ratings']}","{gmbResultDict['gl_telephone']}","{gmbResultDict['gl_address']}","{gmbResultDict['gl_gmb_photos_count']}","{gmbResultDict['gl_reviews']}",{pin_code},"{category}","{gmbResultDict['gmb_category']}","{country}","{state}","{district}","{gmbResultDict['gl_url']}",{gmbResultDict['gl_url_done_flag']},{country_id},{state_id},{district_id},"{city}",\"{timezone}\")"""
        with open(data_file_name,'a') as dataFile:
            dataFile.writelines(listquery)
            print(f'Stored into {data_file_name}')
        dataFile.close()
    except Exception as e:
        print(e)
def searchNearbyPlaces(data_file_name,address,category,country,country_id,state,state_id,district,district_id,myDatabase, myCursor,gmbDataTableName,city,timezone):
    
    
    driver,wait,action,allPlace = sendingDataToWebdriver(address,category)
    if driver is not None:
        allUrl = []
        # pin_code = (int(str(address).split(',')[0]))
        pin_code=0
        searchBusiness = checkBusinessInBD(allPlace= allPlace,myCursor= myCursor,gmbDataTableName=gmbDataTableName)
        for link in searchBusiness:
            
            url = (link.get_attribute('href'))

            allUrl.append(url)
            
          
        allResult = []
        for url in allUrl:
            
               
            print(url)
            try:
                gmbResultDict=(get_GMB_Details(url,driver,wait))
            except Exception as e:
                print(e)
          
                driver.quit()
                driver, wait = headlessDriver(waitTime=10)
            print(gmbResultDict)
            if gmbResultDict != None:
               
                write_data_into_file(data_file_name,gmbResultDict,country,state,district,country_id,state_id,district_id,city,pin_code,category,timezone)
                # listquery = f""",("{gmbResultDict['gl_website']}","{gmbResultDict['gl_business_name']}","{gmbResultDict['gl_ratings']}","{gmbResultDict['gl_telephone']}","{gmbResultDict['gl_address']}","{gmbResultDict['gl_gmb_photos_count']}","{gmbResultDict['gl_reviews']}",{pin_code},"{category}","{country}","{state}","{district}","{gmbResultDict['gl_url']}",{gmbResultDict['gl_url_done_flag']},{country_id},{state_id},{district_id},"{city}")"""
                # with open('data.csv','a') as f:
                #     f.writelines(listquery)
                # f.close()


                # query = f'''insert into {gmbDataTableName} (gl_website,gl_business_name,gl_ratings,gl_telephone,gl_address,gl_gmb_photos_count,gl_reviews,pincode,category,country,state,district,gl_url,gl_url_done_flag,country_code,state_code,district_code,city) values("{gmbResultDict['gl_website']}","{gmbResultDict['gl_business_name']}","{gmbResultDict['gl_ratings']}","{gmbResultDict['gl_telephone']}","{gmbResultDict['gl_address']}","{gmbResultDict['gl_gmb_photos_count']}","{gmbResultDict['gl_reviews']}",{pin_code},"{category}","{country}","{state}","{district}","{gmbResultDict['gl_url']}",{gmbResultDict['gl_url_done_flag']},{country_id},{state_id},{district_id},"{city}")'''
                # try:   
                #     myCursor.execute(query)
                #     myDatabase.commit()
                #     print("Database Insertion Done")
                #     # myDatabase.close()
                # except Exception as e:
                #     print(e)
                    
                #     if 'Duplicate entry' not in str(e):
                #         # myDatabase.close()
                #         time.sleep(1)
                #         myDatabase,myCursor = dbConnection()
                #         try:
                #             myCursor.execute(query)
                #             myDatabase.commit()
                #             print("Data Insterion Done")
                #         except Exception as e:
                #             print(e)
                #     else:
                        
                     
                #         print(e)
                    
                allResult.append(gmbResultDict)
                
                # print("no value found")
        driver.quit()
        return 1
    else:
        return 0
 
@retryFunction
def firstLastPincode(myCursor,category):
    firstPinCodeQuery = f"select pin_code, category from usa_dent_db.google_map where category = '{category}'  limit 1"
    lastPinCodeQuery = f"select pin_code , category from usa_dent_db.google_map where category = '{category}' order by gl_id desc limit 1;"
    try:
        
        myCursor.execute(firstPinCodeQuery)
        
        firstPinCode =  myCursor.fetchall()
        

        myCursor.execute(lastPinCodeQuery)
        
        lastPinCode = myCursor.fetchall()
        
        
    except Exception as e:
        print(e)
        myDatabase,myCursor = dbConnection()
        myCursor.execute(firstPinCodeQuery)
        firstPinCode =  myCursor.fetchall()

        myCursor.execute(lastPinCodeQuery)
        lastPinCode = myCursor.fetchall()
        
    if len(firstPinCode) == 0 and len(lastPinCode) == 0:
        return 0,0
    else:
        return firstPinCode[0][0],lastPinCode[0][0]


if __name__ == '__main__':

    driver,wait = headlessDriver(waitTime=10)
    driver.set_page_load_timeout(20)

    myDatabase, myCursor = dbConnection()
    
    

    driver.get('https://getmypincode.com/pincode/code/US/New-York/New-York/New-York')
    
    allPinCode = wait.until(EC.visibility_of_all_elements_located((By.XPATH,"(//ul[@class='banks-list'])[1]/li/a")))
   
    category= (input('Enter Category: ')).lower()
    firstPincode,lastPinCode = firstLastPincode(myCursor=myCursor,category=category)
    
    allAddress = []
    for pin in allPinCode:
        address= (pin.get_attribute('title'))
        allAddress.append(address)
        
     
    driver.quit()
    for address in allAddress:
        print(address)
        pin_code = (int(str(address).split(',')[0]))
       
        if (firstPincode) != 0 and (lastPinCode) !=0:
            if pin_code in range(firstPincode,lastPinCode):
                continue
        

        searchNearbyPlaces(address=address,category= category,myDatabase= myDatabase,myCursor= myCursor,lastPinCode= lastPinCode)

        
