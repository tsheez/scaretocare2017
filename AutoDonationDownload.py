from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime

updateFrequency = 300 #seconds

driver = webdriver.Chrome(executable_path="C:\\Program Files\\ChromeDriver\\chromedriver.exe")
driver.get("https://streamlabs.com/dashboard/#")
while True:
    try:
        if "My Donations" in driver.title:
            driver.get("https://streamlabs.com/dashboard/donations/export")
            print('downloaded latest at:')
            print(datetime.now().astimezone())
            time.sleep(updateFrequency)
        time.sleep(1) #loops while you login and set up
    except:
        print("Something not good happened. Check the internet or whatever")
        time.sleep(10)
