from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome(executable_path="C:\\Program Files\\ChromeDriver\\chromedriver.exe")
driver.get("https://streamlabs.com/dashboard/#")
while True:
    try:
        if "My Donations" in driver.title:
            driver.get("https://streamlabs.com/dashboard/donations/export")
            print('downloaded latest')
            time.sleep(300)
        time.sleep(5)
    except:
        print("Something not good happened. Check the internet or whatever")
        time.sleep(60)
