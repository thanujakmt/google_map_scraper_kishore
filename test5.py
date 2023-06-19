from HeadlessDriver import headlessDriver
from selenium.webdriver.common.by import By
import time
import random


url = 'https://www.google.com/maps/place/Alabama+Family+Chiropractic+Clinic+LLC/@32.3657858,-86.2753316,15z/data=!4m6!3m5!1s0x888e81bb668cb983:0x679b261213824d94!8m2!3d32.363727!4d-86.2852851!16s%2Fg%2F11f1kbwr0b?authuser=0&hl=en'


def get_reviews(url,driver): 
    # driver, wait = headlessDriver(waitTime=10)
    allReviews = []
    driver.get(url)
    time.sleep(5)
    business = driver.find_element(By.XPATH,"//h1[@class='DUwDvf fontHeadlineLarge']").text
    business = str(business).replace("'","").replace('"','')
    try:
        review = driver.find_element(By.XPATH, "(//div[@jsaction='pane.rating.moreReviews']//span)[12]")
        # total_reviews = int(review.text.split()[0])
        review.click()
    except:
        try:
            time.sleep(2)
            review = driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]/div[2]/div[2]")
            review.click()
        except:
            try:
                review = driver.find_element(By.XPATH,"/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[1]/div[1]/div[2]/div/div[1]/div[2]/span[2]/span[1]/span")
                review.click()
            except:
                pass
    time.sleep(2)

    s_val = [1000,1500]

    counter = 0

    # try:
    #        driver.find_element(By.XPATH, "//span[@class='HlvSq']")
    #        lastElement = 1
    # except:
    #        lastElement = 0
    while counter<5:
        time.sleep(1)
        query = f'''document.querySelector(".m6QErb.DxyBCb.kA9KIf.dS8AEf").scrollBy(0,{random.choice(s_val)})'''
        driver.execute_script(query)
        counter = counter +1
    try:
        
        time.sleep(2)
        temp_reviews = driver.find_elements(By.XPATH,"(//div[@class='GHT2ce'])")
        # print(len(temp_reviews))
        
        for i in range(len(temp_reviews)):
            
            #  print(temp_reviews[i].text)
            #  print((reviews.find_element(By.XPATH,"(//span[@class ='wiI7pd'])[2]")).text)
        
            time.sleep(2)
            try:
                temp_reviews[i].find_element(By.XPATH,"(//button[@aria-label=' See more '][normalize-space()='More'])[1]").click()
                #-----------------------------------------------------------
                #  try:
                #     rating = temp_reviews[i].find_element(By.XPATH,f"(//span[@class='kvMYJc'])[{i+1}]").get_attribute('aria-label')
                #     print(rating)
                #     if "5 stars" in rating:
                        
                #         print(i)
                #         # print((temp_reviews[i].find_element(By.XPATH,f"(//span[@class ='wiI7pd'])[{i+1}]")).text)
                #  except Exception as e:
                #     print(e)
            except:
                pass
    except:
        pass
    try:
        temp_reviews = driver.find_elements(By.XPATH,"(//div[@class='GHT2ce'])")
    except:
        pass

    for i in range (len(temp_reviews)):
        content = (temp_reviews[i].text)
        rating = temp_reviews[i].find_element(By.XPATH,f"(//span[@class='kvMYJc'])[{i+1}]").get_attribute('aria-label')
        # print(rating)

        if '5 stars' in rating:
            # print(content)
        
            comment = (content.splitlines()) 
            try:
                commentLen = (len(comment[1].split(" ")))
                print(commentLen)
                if commentLen>40 and commentLen<200:
                    allReviews.append(comment[1])
            except:
                pass
   
    return {"Business":business,"URL":url,"Reviews":allReviews}

if __name__ == '__main__':
    # url = 'https://www.google.com/maps/place/GO+PHYSIO+Physical+Therapy+%26+Bike+Fitting/@44.9609729,-93.1793152,17z/data=!3m1!5s0x52b32ca9f39711c7:0xce59989866204937!4m6!3m5!1s0x87f629d0efa15555:0xeca07f5868b02a14!8m2!3d44.9609729!4d-93.1793152!16s%2Fg%2F11f4qysdyk?authuser=0&hl=en'
    # review_dict= get_reviews(url)
    # print(review_dict)
    
    print(str(random.random()).split(".")[1])

