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
    print(desired_capabilities)
    # desired_capabilities['goog:loggingPrefs'] = {'browser': 'ALL'}

    driver_path = "D:\\Codes\\gpmproject\\chromium_v115\\src\\out\\Official\\chromedriver.exe" # test
    driver_path = "D:\\Codes\\gpmproject\\chromium_v115\\src\\out\\Debug\\chromedriver.exe"    # test
    print('driver_path: ', driver_path)

    ser = Service(driver_path)
    # driver = webdriver.Chrome(service=ser, options=chrome_options, desired_capabilities=desired_capabilities)
    # input("Enter to quit")
    # driver.quit()

    driver = webdriver.Chrome(service=ser, options=chrome_options, service_args=["--verbose", "--log-path=D:\\gpmdriver.log"]) #, desired_capabilities=desired_capabilities)
    # input("Enter to go gleam")
    driver.get("https://gleam.io/")

    # driver.get("https://hmaker.github.io/selenium-detector/")

    # driver.execute_script('''window.open("https://hmaker.github.io/selenium-detector/","_blank");''') # open page in new tab
    # driver.execute_script('''window.open("https://gleam.io/","_blank");''') # open page in new tab
    # input("Enter to quit")
    # driver.quit()
    # input("Enter to continue")
    # driver = webdriver.Chrome(service=ser, options=chrome_options, service_args=["--verbose", "--log-path=D:\\gpmdriver.log"]) #, desired_capabilities=desired_capabilities)
    # time.sleep(.5)
    print("Title: ", driver.title) # test edit code c++ xem return có khác k
    # print('window_handles[1] = ', driver.window_handles[1]) # Chỉ cần thế này thôi là dính đòn rồi

    # Test xem switch to có gì mà làm bị detect
    # driver.execute_script('''window.open("https://gleam.io","_blank");''') # open page in new tab
    # time.sleep(0.2)

    # driver.switch_to.window(window_name=driver.window_handles[1])   # switch to new tab
    # driver.get("https://gleam.io/")

    # print("Title: ", driver.title) # test edit code c++ xem return có khác k

    # input('Enter to goto genk.vn')
    # print("Title: ", driver.title) # test edit code c++ xem return có khác k
    # driver.get("http://14.225.204.6:81/quan_ly_key")
    # driver.get("https://google.com")

    input('Enter end')


    # # Print the browser logs
    # logs = driver.get_log('browser')
    # for log in logs:
    #     print(log)

    # driver.close()
    driver.quit()

    print('Request stop profile')
    api.Stop(profileId)
    time.sleep(1)

    print('Delete profile')
    api.Delete(profileId)



    print('Done')