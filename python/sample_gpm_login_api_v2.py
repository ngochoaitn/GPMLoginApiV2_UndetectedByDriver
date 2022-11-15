import time
from GPMLoginAPI import GPMLoginAPI
from selenium import webdriver
# python3 -m pip install --upgrade pip
# python3 -m pip
# pip install selenium
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options

from UndetectChromeDriver import UndetectChromeDriver
apiUrl = 'http://127.0.0.1:19995'

def SampleAllApiFunction():
    api = GPMLoginAPI(apiUrl) # Alert: copy url api on GPM Login App

    #  Print list off profiles in GPMLogin -------------------------
    print('PROFILES ----------------------------')
    profiles = api.GetProfiles()
    if(profiles != None):
        for profile in profiles:
            id = profile['id']
            name = profile['name']
            print(f"Id: {id} | Name: {name}")

    print('CREATE PROFILE ------------------')
    createdResult = api.Create("giaiphapmmo.net")
    createdProfileId = None
    if(createdResult != None):
        status = bool(createdResult['status'])
        if(status):
            createdProfileId = str(createdResult['profile_id'])
    print(f"Created profile ID: {createdProfileId}")

    print('UPDATE PROXY------------------')
    api.UpdateProxy(createdProfileId, '')

    print('UPDATE NOTE ------------------')
    api.UpdateNote(createdProfileId, 'Profile create by API')

    print('START PROFILE ------------------')
    startedResult = api.Start(createdProfileId)
    time.sleep(3)
    if(startedResult != None):
        status = bool(startedResult['status'])
        if(status):
            browserLocation = str(startedResult["browser_location"])
            seleniumRemoteDebugAddress = str(startedResult["selenium_remote_debug_address"])
            gpmDriverPath = str(startedResult["selenium_driver_location"])
            print('gpmDriverPath = ', gpmDriverPath, 'seleniumRemoteDebugAddress = ', seleniumRemoteDebugAddress)
            # Init selenium
            options = Options()
            options.debugger_address = seleniumRemoteDebugAddress
            options.binary_location = browserLocation
            # options.add_experimental_option("useAutomationExtension", False)
            # options.add_experimental_option("enable-automation", False)
            options.add_argument("--disable-blink-features")
            options.add_argument("--disable-blink-features=AutomationControlled")

            myService  = service.Service(gpmDriverPath)
            # driver = UndetectChromeDriver(service = myService, options=options)
            driver = webdriver.Chrome(service = myService, options=options)
            driver.get("https://fingerprint.com/products/bot-detection/")
            time.sleep(10)
            input('Enter to next...')
            driver.close()
            driver.quit()

    print('DELETE PROFILE ------------------')
    api.Delete(createdProfileId)
    print(f"Deleted: {createdProfileId}")

    print('ALL DONE, PRESS ENTER TO EXIT')
    input() # pause

if __name__ == '__main__':
    api = GPMLoginAPI(apiUrl) # Alert: copy url api on GPM Login App
    profileId = input('Profile Id: ')
    startedResult = api.Start(profileId)
    print('selenium_remote_debug_address = ', startedResult["selenium_remote_debug_address"])
    print('===============================')
    print('Profile started. Enter to exit')
    input()

    # SampleAllApiFunction()