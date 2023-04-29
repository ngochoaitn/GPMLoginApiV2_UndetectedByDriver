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
    # driver_path = "C:\\Users\\LEGION\\AppData\\Local\\Programs\\GPMLogin\\gpm_browser\\gpm_browser_chromium_core_107\\gpmdriver.exe"
    print('driver_path: ', driver_path)
    ser = Service(driver_path)
    # driver = webdriver.Chrome(executable_path=driver_path, options=chrome_options)
    driver = webdriver.Chrome(service=ser, options=chrome_options)
    # input()
    userName = input('User name: ')
    password = getpass('Password: ')
    driver.get("https://mail.google.com/")
    time.sleep(3)
    try:
        btnLogin = driver.find_element(By.XPATH, '/html/body/header/div/div/div/a[2]')
        btnLogin.click()
        time.sleep(2)
    except:
        print('Not found btn login')

    txtEmailElement = driver.find_element(By.ID, "identifierId")
    txtEmailElement.send_keys(userName)

    btnNext = driver.find_element(By.ID, "identifierNext")
    btnNext.click()

    time.sleep(2)

    txtPasswordElement = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/section[2]/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input")
    txtPasswordElement.send_keys(password)

    btnNext = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button")
    btnNext.click()

    print('Enter for quit')
    input()

    driver.close()
    driver.quit()