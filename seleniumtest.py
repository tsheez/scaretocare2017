from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome(executable_path="C:\\Program Files\\ChromeDriver\\chromedriver.exe")
driver.get("https://streamlabs.com/dashboard/#")
while True:
    print(driver.title)
    if "My Donations" in driver.title:
        print('woo!')
        driver.get("https://streamlabs.com/dashboard/donations/export")
    time.sleep(10)

