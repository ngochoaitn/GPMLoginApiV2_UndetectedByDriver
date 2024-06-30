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

    # driver.get("https://gleam.io/")
    # driver.get("https://nowsecure.nl")
    # driver.get("https://fingerprint.com/products/bot-detection/")
    # driver.get("https://hmaker.github.io/selenium-detector/")
    # driver.get("https://dash.cloudflare.com/login")

    driver.get('https://pro.nansen.ai/auth/signup')

    # driver.get("https://www.redbubble.com/studio/dashboard")
    # try:
    #     btnLogin = driver.find_element(By.XPATH, '//*[@id="RB_React_Component_LoginLink_4"]/a')
    #     btnLogin.click()
    #     time.sleep(2)
    # except:
    #     print('Not found btn login')

    input('Enter to close')

    # driver.close()
    driver.quit()
    api.Stop(profileId)