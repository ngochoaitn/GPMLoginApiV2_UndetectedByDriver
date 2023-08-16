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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Alert: This is test sample, we not support code for it :(
if __name__ == '__main__':
    api = GPMLoginAPI('http://127.0.0.1:19995') # Alert: copy url api on GPM Login App

    createdResult = api.Create("test-gleam")
    profileId = str(createdResult['profile_id'])

    startedResult = api.Start(profileId)

    time.sleep(2)

    chrome_options = Options()
    chrome_options.add_argument("--lang=en-US")
    chrome_options.add_experimental_option("debuggerAddress", startedResult["selenium_remote_debug_address"])

    chrome_options.arguments.extend(["--no-default-browser-check", "--no-first-run"])

    chrome_options.add_argument("--verbose")  # Enable verbose logging
    chrome_options.add_argument("--log-path=D:\\gpmdriver.log")  # Set the path to the log file

    driver_path = startedResult["selenium_driver_location"]
    # Set the desired log level to capture all logs
    desired_capabilities = DesiredCapabilities.CHROME.copy()
    # print(desired_capabilities)
    # desired_capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}

    print('driver_path: ', driver_path)

    ser = Service(driver_path)

    driver = webdriver.Chrome(service=ser, options=chrome_options)

    driver.get("https://gleam.io/")
    time.sleep(5)

    try:
        btnLogin = driver.find_element(By.XPATH, "//a[contains(@href, '/login')]")
        btnLogin.click()

        txtEmail = driver.find_element(By.XPATH, '//*[@id="elm-email"]')
        txtEmail.send_keys("312312312@gmail.com")

        txtPass = driver.find_element(By.XPATH, '//*[@id="elm-password"]')
        txtPass.send_keys(" 1212321")

        btnLogin = driver.find_element(By.XPATH, "//button[@type='submit']")
        btnLogin.click()
    except:
        print('error')

    input('Enter end')

    driver.quit()

    print('Request stop profile')
    api.Stop(profileId)
    time.sleep(1)

    print('Delete profile')
    api.Delete(profileId)

    print('Done')