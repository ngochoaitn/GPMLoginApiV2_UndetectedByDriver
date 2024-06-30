// See https://aka.ms/new-console-template for more information
// Console.WriteLine("Hello, World!");


// https://github.com/hardkoded/puppeteer-sharp
using PuppeteerSharp;

/************** Nếu không chạy được thì chạy code tải browser trước */

// Tải Chrome
//var browserFetcher = new BrowserFetcher();
//await browserFetcher.DownloadAsync();
// Tải Fiefox
//var browserFetcher = new BrowserFetcher(SupportedBrowser.Firefox);
//await browserFetcher.DownloadAsync();
/***********/


int debugPort = 47930; // Lấy debug port qua GPM API theo mô tả tại tài liệu https://docs.gpmloginapp.com/api-document/mo-profile

ConnectOptions connectOptions = new ConnectOptions()
{
    BrowserURL = $"http://127.0.0.1:{debugPort}"
};
var browser = await Puppeteer.ConnectAsync(connectOptions);

await using var page = await browser.NewPageAsync();
try { await page.GoToAsync("http://genk.vn"); } catch { }
await page.ScreenshotAsync("D:\\a.png");
Console.ReadLine();