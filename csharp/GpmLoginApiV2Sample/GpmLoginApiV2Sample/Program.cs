using GpmLoginApiV2Sample.Libs;
using Newtonsoft.Json.Linq;
using System;

namespace GpmLoginApiV2Sample
{
    internal class Program
    {
        static string apiUrl = "http://127.0.0.1:19995";
        static void Main(string[] args)
        {
            //GPMLoginAPI api = new GPMLoginAPI(apiUrl);
            //Console.Write("Profile id: ");
            //string profileId = Console.ReadLine();
            //JObject startedResult = api.Start(profileId);
            //Console.WriteLine($"selenium_remote_debug_address = {startedResult["selenium_remote_debug_address"]}");
            //Console.WriteLine("Profile stared Enter to exit");
            //Console.ReadLine();

            GPMLoginApi_MoreSample.SampleAllApiFunction();

            //GPMLoginApi_MoreSample.TestLoginGoogle(); // This is test sample, we not support code for it :(
        }
    }
}
