from getpass import getpass
import os
import time
import sys
sys.path.append("..")
from GPMLoginAPI import GPMLoginAPI
from selenium import webdriver
# python3 -m pip install --upgrade pip
# python3 -m pip
# pip install selenium
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# Alert: This is test sample, we not support code for it :(
if __name__ == '__main__':
    debug_port = 34020
    user_data_dir = "D:\\Codes\\chromium-test-file\\profiles\\CVpUDhVs52-18042023"
    args = f'--user-data-dir="{user_data_dir}" --lang=en-US --disable-encryption --password-store=basic --gpm-disable-machine-id --gpm-disable-encryption --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36" --no-default-browser-check --uniform2f-noise=0.0860361993382854 --load-extension="{user_data_dir}\\Default\\GPMBrowserExtenions\clipboard-ext,{user_data_dir}\\Default\\GPMBrowserExtenions\\cookies-ext-new" --max-vertex-uniform=4037 --max-fragment-uniform=1443 --window-size=2560,1440 --webgl-renderer="ANGLE (Intel, Intel(R) HD Graphics 4000 Direct3D9Ex vs_3_0 ps_3_0, igdumd64.dll)" --remote-debugging-port={debug_port} --disk-cache-size=104857600'
    # print(args)
    os.popen(f'"D:\\Codes\\gpmproject\\chromium_v111\\src\\out\\Official\\Chrome-bin\\chrome.exe" {args}')

    time.sleep(3)

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", f"127.0.0.1:{debug_port}")
    driver_path = "D:\\Codes\\gpmproject\\chromium_v111\\src\\out\\Official\\chromedriver.exe"
    print('driver_path: ', driver_path)
    ser = Service(driver_path)
    driver = webdriver.Chrome(service=ser, options=chrome_options)
    driver.get("https://fingerprint.com/products/bot-detection/")
    # driver.get("https://dash.cloudflare.com/login")
    # driver.get("https://www.redbubble.com/studio/dashboard")

    try:
        btnLogin = driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div[2]/div/div/div/div/div/div[2]')
        btnLogin.click()
        time.sleep(2)
    except:
        print('Not found btn login')

    input('Enter to close')

    driver.close()
    driver.quit()
