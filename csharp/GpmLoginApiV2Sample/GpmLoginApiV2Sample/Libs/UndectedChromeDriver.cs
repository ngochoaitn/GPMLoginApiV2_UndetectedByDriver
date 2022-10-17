using OpenQA.Selenium.Chrome;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace GpmLoginApiV2Sample
{
    public class UndetectChromeDriver : ChromeDriver
    {
        public UndetectChromeDriver(ChromeDriverService service, ChromeOptions options) : base(service, options)
        {
            options.AddAdditionalOption("useAutomationExtension", false);
            options.AddExcludedArgument("enable-automation");
            options.AddArgument("--disable-blink-features");
            options.AddArgument("--disable-blink-features=AutomationControlled");
        }

        public void Get(string url)
        {
            removeCdcProps();

            this.Navigate().GoToUrl(url);
        }

        #region Hook js
        private void removeCdcProps()
        {
            if (!hasCdcProps())
                return;

            var parameters = new Dictionary<string, object>
            {
                ["source"] = "Object.defineProperty(navigator, 'webdriver', { get: () => undefined })"
            };
            this.ExecuteCdpCommand("Page.addScriptToEvaluateOnNewDocument", parameters);

            parameters = new Dictionary<string, object>
            {
                ["source"] = @"let objectToInspect = window,
                        result = [];
                    while(objectToInspect !== null) 
                    { result = result.concat(Object.getOwnPropertyNames(objectToInspect));
                      objectToInspect = Object.getPrototypeOf(objectToInspect); }
                    result.forEach(p => p.match(/.+_.+_(Array|Promise|Symbol)/ig)
                                        &&delete window[p]&&console.log('removed',p))"
            };
            this.ExecuteCdpCommand("Page.addScriptToEvaluateOnNewDocument", parameters);

            bool a = hasCdcProps();
        }

        private bool hasCdcProps()
        {
            string code = @"let objectToInspect = window,
                result = [];
            while(objectToInspect !== null)
            { result = result.concat(Object.getOwnPropertyNames(objectToInspect));
              objectToInspect = Object.getPrototypeOf(objectToInspect); }
            return result.filter(i => i.match(/.+_.+_(Array|Promise|Symbol)/ig))";

            var result = this.ExecuteScript(code);
            ReadOnlyCollection<object> cdcList = (ReadOnlyCollection<object>)result;

            return cdcList.Count > 0;
        }
        #endregion
    }
}
