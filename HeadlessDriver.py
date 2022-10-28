import undetected_chromedriver as uc
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver



def headlessDriver(waitTime):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    
    options = webdriver.ChromeOptions()
    # options.add_argument(f'user-agent={user_agent}')
    # options.headless = True
    options.page_load_strategy = 'eager'
    # , options=options

    driver = uc.Chrome(use_subprocess=True, options= options)
    wait = WebDriverWait(driver,waitTime)
    
    return driver,wait


# Additional Options

# user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"

# options = webdriver.ChromeOptions()
# options.headless = True
# options.add_argument(f'user-agent={user_agent}')
# options.add_argument("--window-size=1920,1080")
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--allow-running-insecure-content')
# options.add_argument("--disable-extensions")
# options.add_argument("--proxy-server='direct://'")
# options.add_argument("--proxy-bypass-list=*")
# options.add_argument("--start-maximized")
# options.add_argument('--disable-gpu')
# options.add_argument('--disable-dev-shm-usage')
# options.add_argument('--no-sandbox')

# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

if __name__ == '__main__':
    driver,wait=headlessDriver(waitTime=6)
    driver.get("https://www.google.com")
    driver.get_screenshot_as_file("pp.png")