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

# from UndetectChromeDriver import UndetectChromeDriver

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
    # startedResult = api.Start('e20e14ee-b825-4d36-8eb3-ccea61562aa4')
    time.sleep(3)
    if(startedResult != None):
        status = bool(startedResult['status'])
        if(status):
            seleniumRemoteDebugAddress = str(startedResult["selenium_remote_debug_address"])
            gpmDriverPath = str(startedResult["selenium_driver_location"])
            print('gpmDriverPath = ', gpmDriverPath, 'seleniumRemoteDebugAddress = ', seleniumRemoteDebugAddress)
            # Init selenium
            options = Options()
            options.debugger_address = seleniumRemoteDebugAddress
            # options.add_experimental_option("useAutomationExtension", False)
            # options.add_experimental_option("enable-automation", False)
            options.add_argument("--disable-blink-features")
            options.add_argument("--disable-blink-features=AutomationControlled")

            myService  = service.Service(gpmDriverPath)
            # myService  = service.Service("C:\\Users\\LEGION\\AppData\\Local\\Programs\\GPMLogin\\chromedriver_v109_patched.exe")
            # driver = UndetectChromeDriver(service = myService, options=options)
            driver = webdriver.Chrome(service = myService, options=options)

            cdc_props = driver.execute_script('const j=[];for(const p in window){'
                                  'if(/^[a-z]{3}_[a-z]{22}_.*/i.test(p)){'
                                  'j.push(p);delete window[p];}}return j;')
            if len(cdc_props) > 0:
                cdc_props_js_array = '[' + ','.join('"' + p + '"' for p in cdc_props) + ']'
                print(cdc_props_js_array)
                driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                          {'source': cdc_props_js_array + '.forEach(k=>delete window[k]&&console.log("remove ",k));'})

            driver.get("https://fingerprint.com/products/bot-detection/")
            # time.sleep(10)
            input('Enter to close browser...')
            driver.close()
            driver.quit()

    print('DELETE PROFILE ------------------')
    input('Enter to delete profile')
    api.Delete(createdProfileId)
    print(f"Deleted: {createdProfileId}")

    print('ALL DONE')
    # input() # pause

if __name__ == '__main__':
    SampleAllApiFunction()