from encodings import search_function
from multiprocessing import set_forkserver_preload
from selenium.webdriver.chrome import service
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class UndetectChromeDriver(webdriver.Chrome):
    def __init__(self, service : service.Service, options : Options):
        super(UndetectChromeDriver, self).__init__(service = service, options=options)
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option("useAutomationExtension", False)
        options.add_argument('--disable-blink-features')
        options.add_argument('--turn-off-whats-new')
        

    def hasCdcProps(self):
        return self.execute_script(
            """
            let objectToInspect = window,
                result = [];
            while(objectToInspect !== null)
            { result = result.concat(Object.getOwnPropertyNames(objectToInspect));
              objectToInspect = Object.getPrototypeOf(objectToInspect); }
            return result.filter(i => i.match(/.+_.+_(Array|Promise|Symbol)/ig))
            """
        )

    def removeCdcProps(self):
        self.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
            },
        )

        if self.hasCdcProps():
            self.execute_cdp_cmd(
                "Page.addScriptToEvaluateOnNewDocument",
                {
                    "source": """
                        let objectToInspect = window,
                            result = [];
                        while(objectToInspect !== null) 
                        { result = result.concat(Object.getOwnPropertyNames(objectToInspect));
                        objectToInspect = Object.getPrototypeOf(objectToInspect); }
                        result.forEach(p => p.match(/.+_.+_(Array|Promise|Symbol)/ig)
                                            &&delete window[p]&&console.log('removed',p))
                        """
                },
            )

    def GetByGpm(self, url : str):
        self.removeCdcProps()
        super().get(url)

