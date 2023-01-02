from GPMLoginAPI import GPMLoginAPI
from selenium import webdriver
# python3 -m pip install --upgrade pip
# python3 -m pip
# pip install selenium
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options

# from UndetectChromeDriver import UndetectChromeDriver

apiUrl = 'http://127.0.0.1:19995'

if __name__ == '__main__':
    api = GPMLoginAPI(apiUrl) # Alert: copy url api on GPM Login App
    profileId = input('Profile Id: ')
    startedResult = api.Start(profileId)
    print('selenium_remote_debug_address = ', startedResult["selenium_remote_debug_address"])
    print('===============================')
    print('Profile started. Enter to exit')
    input()