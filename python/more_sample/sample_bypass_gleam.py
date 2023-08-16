from getpass import getpass
import time
import sys
sys.path.append("..")
from GPMLoginAPI import GPMLoginAPI
from selenium import webdriver
# python3 -m pip install --upgrade pip
# python3 -m pip
# pip install selenium
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Alert: This is test sample, we not support code for it :(
# Author: https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/1390
if __name__ == '__main__':
    api = GPMLoginAPI('http://127.0.0.1:19995') # Alert: copy url api on GPM Login App
    profileId = input('Profile Id: ')
    startedResult = api.Start(profileId)

    time.sleep(3)

    chrome_options = Options()
    chrome_options.add_argument("--lang=en-US")
    chrome_options.add_experimental_option("debuggerAddress", startedResult["selenium_remote_debug_address"])

    chrome_options.arguments.extend(["--no-default-browser-check", "--no-first-run"])

    driver_path = startedResult["selenium_driver_location"]
    print('driver_path: ', driver_path)
    ser = Service(driver_path)
    driver = webdriver.Chrome(service=ser, options=chrome_options)


    driver.execute_script('''window.open("https://gleam.io","_blank");''') # open page in new tab
    driver.switch_to.window(window_name=driver.window_handles[1])   # switch to first tab
    time.sleep(8) # wait until page has loaded
    driver.switch_to.window(window_name=driver.window_handles[0])   # switch to first tab
    driver.close() # close first tab
    driver.switch_to.window(window_name=driver.window_handles[0] )  # switch back to new tab
    time.sleep(2)
    driver.get("https://google.com")
    time.sleep(4)
    # driver.get("https://nowsecure.nl") # this should pass cloudflare captchas now

    driver.get("https://gleam.io/")
    # driver.get("https://nowsecure.nl")
    # driver.get("https://fingerprint.com/products/bot-detection/")
    # driver.get("https://dash.cloudflare.com/login")

    # driver.get("https://www.redbubble.com/studio/dashboard")
    # try:
    #     btnLogin = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div/div/div/div/div/div[2]')
    #     btnLogin.click()
    #     time.sleep(2)
    # except:
    #     print('Not found btn login')

    input('Enter to close')

    driver.close()
    driver.quit()