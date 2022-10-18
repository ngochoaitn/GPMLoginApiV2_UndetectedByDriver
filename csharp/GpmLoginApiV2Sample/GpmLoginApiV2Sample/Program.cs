using GpmLoginApiV2Sample.Libs;
using Newtonsoft.Json.Linq;
using OpenQA.Selenium;
using OpenQA.Selenium.Chrome;
using System;
using System.Collections.Generic;
using System.IO;
using System.Threading;

namespace GpmLoginApiV2Sample
{
    internal class Program
    {
        static void Main(string[] args)
        {
            GPMLoginAPI api = new GPMLoginAPI("http://127.0.0.1:15990");
            Console.Write("Profile id: ");
            string profileId = Console.ReadLine();
            JObject startedResult = api.Start(profileId);
            Console.WriteLine($"selenium_remote_debug_address = {startedResult["selenium_remote_debug_address"]}");
            Console.WriteLine("Profile stared Enter to exit");
            Console.ReadLine();

            // SampleAllApiFunction();
            //TestLoginGoogle(); // This is test sample, we not support code for it :(
        }

        private static void SampleAllApiFunction()
        {
            GPMLoginAPI api = new GPMLoginAPI("http://127.0.0.1:49806");
            
            // Print list off profiles in GPMLogin -------------------------
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("PROFILES ----------------------------");
            Console.ForegroundColor = ConsoleColor.White;

            List<JObject> profiles = api.GetProfiles();
            if (profiles != null)
            {
                foreach (JObject profile in profiles)
                {
                    string name = Convert.ToString(profile["name"]);
                    string id = Convert.ToString(profile["id"]);
                    Console.WriteLine($"ID: {id} | Name: {name}");
                }
            }

            // Create profile and print id -------------------------
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("CREATE PROFILE ------------------");
            Console.ForegroundColor = ConsoleColor.White;

            JObject createdResult = api.Create("giaiphapmmo.net");
            string createdProfileId = null;

            if (createdResult != null)
            {
                bool status = Convert.ToBoolean(createdResult["status"]);
                if (status)
                    createdProfileId = Convert.ToString(createdResult["profile_id"]);
            }

            Console.WriteLine("Created profile ID: " + createdProfileId);

            // Update proxy, note
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("UPDATE PROXY------------------");
            api.UpdateProxy(createdProfileId, "");

            Console.WriteLine("UPDATE NOTE------------------");
            api.UpdateNote(createdProfileId, "Profile create by API");

            Console.ForegroundColor = ConsoleColor.White;

            // Start profile ----------------------------------------
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("START PROFILE ------------------");
            Console.ForegroundColor = ConsoleColor.White;

            JObject startedResult = api.Start(createdProfileId);
            if (startedResult != null)
            {
                bool status = Convert.ToBoolean(createdResult["status"]);
                if (status)
                {
                    string browserLocation = Convert.ToString(startedResult["browser_location"]);
                    string seleniumRemoteDebugAddress = Convert.ToString(startedResult["selenium_remote_debug_address"]);
                    string gpmDriverPath = Convert.ToString(startedResult["selenium_driver_location"]);

                    // Init selenium
                    FileInfo gpmDriverFileInfo = new FileInfo(gpmDriverPath);

                    ChromeDriverService service = ChromeDriverService.CreateDefaultService(gpmDriverFileInfo.DirectoryName, gpmDriverFileInfo.Name);
                    ChromeOptions options = new ChromeOptions();
                    options.BinaryLocation = browserLocation;
                    options.DebuggerAddress = seleniumRemoteDebugAddress;
                    //options.AddAdditionalOption("useAutomationExtension", false);
                    //options.AddExcludedArgument("enable-automation");
                    options.AddArgument("--disable-blink-features");
                    options.AddArgument("--disable-blink-features=AutomationControlled");

                    ChromeDriver driver = new ChromeDriver(service, options);

                    driver.Navigate().GoToUrl("https://fingerprint.com/products/bot-detection/");

                    // Delay 10s, close and delete profile
                    Thread.Sleep(10000);

                    driver.Close();
                    driver.Quit();
                    driver.Dispose();
                }
            }

            // Delete profile ----------------------------------------
            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("DELETE PROFILE ------------------");
            Console.ForegroundColor = ConsoleColor.White;

            api.Delete(createdProfileId);
            Console.WriteLine("Deleted : " + createdProfileId + "\n\n");

            Console.ForegroundColor = ConsoleColor.Green;
            Console.WriteLine("ALL DONE, PRESS ENTER TO EXIT");
            Console.ForegroundColor = ConsoleColor.White;
            Console.ReadLine();
        }

        // Alert: This is test sample, we not support code for it :(
        private static void TestLoginGoogle()
        {
            GPMLoginAPI api = new GPMLoginAPI("http://127.0.0.1:15990");
            Console.Write("Profile id: ");
            string profileId = Console.ReadLine();
            JObject startedResult = api.Start(profileId);

            Console.Write("User name: ");
            string userName = Console.ReadLine();
            Console.Write("Password: ");
            string password = Console.ReadLine();

            string browserLocation = Convert.ToString(startedResult["browser_location"]);
            string seleniumRemoteDebugAddress = Convert.ToString(startedResult["selenium_remote_debug_address"]);
            string gpmDriverPath = Convert.ToString(startedResult["selenium_driver_location"]);

            // Init selenium
            FileInfo gpmDriverFileInfo = new FileInfo(gpmDriverPath);

            ChromeDriverService service = ChromeDriverService.CreateDefaultService(gpmDriverFileInfo.DirectoryName, gpmDriverFileInfo.Name);
            ChromeOptions options = new ChromeOptions();
            options.BinaryLocation = browserLocation;
            options.DebuggerAddress = seleniumRemoteDebugAddress;
            //options.AddAdditionalOption("useAutomationExtension", false);
            //options.AddExcludedArgument("enable-automation");
            options.AddArgument("--disable-blink-features");
            options.AddArgument("--disable-blink-features=AutomationControlled");

            ChromeDriver driver = new ChromeDriver(service, options);

            driver.Navigate().GoToUrl("https://mail.google.com/");
            Thread.Sleep(3000);

            try
            {
                var btnLogin = driver.FindElement(By.XPath("/html/body/header/div/div/div/a[2]"));
                btnLogin.Click();
                Thread.Sleep(2000);
            }
            catch { }

            var txtEmailElement = driver.FindElement(By.Id("identifierId"));
            txtEmailElement.SendKeys(userName);

            var btnNext = driver.FindElement(By.Id("identifierNext"));
            btnNext.Click();
            Thread.Sleep(2000);

            var txtPasswordElement = driver.FindElement(By.XPath("/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[1]/div/form/span/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input"));
            txtPasswordElement.SendKeys(password);

            btnNext = driver.FindElement(By.XPath("/html/body/div[1]/div[1]/div[2]/div/c-wiz/div/div[2]/div/div[2]/div/div[1]/div/div/button"));
            btnNext.Click();

            Console.WriteLine("Profile stared Enter to exit");
            Console.ReadLine();
        }
    }
}
