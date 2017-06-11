from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime
import glob, os


if __name__ == '__main__':
    updateFrequency = 15 #seconds

    driver = webdriver.Chrome(executable_path="C:\\Users\\KastreamAbdulJabbar\\Desktop\\chromedriver.exe")
    driver.get("https://streamlabs.com/dashboard/#")
    while True:
        try:
            if "My Donations" in driver.title:
                files = glob.glob('C:\\Users\\tlsha\\Downloads\\donations*')
                for file in files: os.remove(file)
                print("Cleaned up Files")
                driver.get("https://streamlabs.com/dashboard/donations/export")
                print('downloaded latest at:', end = " ")
                print(datetime.now().astimezone())
                time.sleep(updateFrequency)
            time.sleep(1) #loops while you login and set up
        except:
            print("Something not good happened. Check the internet or whatever")
            time.sleep(10)
