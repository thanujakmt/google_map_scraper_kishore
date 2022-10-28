from databaseConnection import dbConnection
from googleMapFinal_address import *




def getSpecificLocationGmbDetails(category,address):
    allUrl = []
    myDatabase, myCursor = dbConnection()
    gmbDataTableName = 'videographer_details_for_kim'
    driver, wait, action,allPlace = sendingDataToWebdriver(address= address, category= category)

    searchBusiness = checkBusinessInBD(allPlace= allPlace,myCursor= myCursor,gmbDataTableName=gmbDataTableName)
    for link in searchBusiness:
        # link= (link.find_element(By.XPATH,"//a"))
        url = (link.get_attribute('href'))
        allUrl.append(url)
        
        # print((link.find_element(By.XPATH,"//a")).get_attribut('href'))
    allResult = []
    for url in allUrl:
            
            # url = (link.get_attribute('href'))
        print(url)
        try:
            gmbResultDict=(get_GMB_Details(url,driver,wait))
        except Exception as e:
            print(e)
            driver.quit()
            driver, wait = headlessDriver(waitTime=10)
        print(gmbResultDict)


        if gmbResultDict != None:
                try:
                    query = f'''insert into {gmbDataTableName} (gl_website,gl_business_name,gl_ratings,gl_email,gl_telephone,gl_address,gl_gmb_photos_count,gl_reviews,category) values("{gmbResultDict['gl_website']}","{gmbResultDict['gl_business_name']}","{gmbResultDict['gl_ratings']}","{gmbResultDict['gl_email']}","{gmbResultDict['gl_telephone']}","{gmbResultDict['gl_address']}","{gmbResultDict['gl_gmb_photos_count']}","{gmbResultDict['gl_reviews']}","{category}")'''
                    
                    myCursor.execute(query)
                    myDatabase.commit()
                    print("Database Insertion Done")
                    # myDatabase.close()
                except Exception as e:
                    print(e)
                    
                    if 'Duplicate entry' not in str(e):
                        myDatabase.close()
                        time.sleep(10)
                        myDatabase,myCursor = dbConnection()
                        time.sleep(4)
                        myCursor.execute(query)
                        myDatabase.commit()
                        print("Data Insterion Done")

if __name__ == '__main__':

    category = input("Enter the category : ")
    address = input("Enter the address: ")
    getSpecificLocationGmbDetails(category = category ,address = address)

