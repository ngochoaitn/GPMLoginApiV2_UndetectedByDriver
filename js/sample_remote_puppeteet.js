// npm install puppeteer
// tested on v18.12.0
// run: node .\sample_remote_puppeteet.js
// require fs and puppeteer

const fs = require("fs");
const http = require('http');

const puppeteer = require("puppeteer");
const apiUrl = 'http://127.0.0.1:19995'

async function startProfile(idProfile){
    return new Promise((resolve, reject) => {
        http.get(`${apiUrl}/v2/start?profile_id=${idProfile}`, (resp) => {
            let data = '';

            resp.on('data', (chunk) => {
                data += chunk;
            });

            resp.on('end', async() => {
                await new Promise(resolve2 => setTimeout(() => resolve(JSON.parse(data)), 2000)); // Chờ 2s để khởi động profile hoặc lâu hơn nếu có proxy
            });
        }).on("error", (err) => {
            reject(err);
        });
    });
}

function stopProfile(idProfile){
    http.get(`${apiUrl}/v2/stop?profile_id=${idProfile}`, (resp) => {});
}

async function getBrowserConnectInfo(debugAddress){
    return new Promise((resolve, reject) => {
        http.get(`http://${debugAddress}/json/version`, (resp) => {
            let data = '';

            resp.on('data', (chunk) => {
                data += chunk;
            });

            resp.on('end', () => {
                resolve(JSON.parse(data));
            });
        }).on("error", (err) => {
            console.error(err)
            reject(err);
        });
    });
}

async function captureScreenshot(webSocketDebuggerUrl) {
    // if screenshots directory is not exist then create one
    if (!fs.existsSync("screenshots")) {
        fs.mkdirSync("screenshots");
    }

    try {
        const browser = await puppeteer.connect({
            browserWSEndpoint: webSocketDebuggerUrl
        });

        // const page = await browser.newPage();
        const page = await browser.pages().then(allPages => allPages[0]);;

        await page.setViewport({ width: 1440, height: 1080 });

        await page.goto("https://giaiphapmmo.net");

        await page.screenshot({ path: `screenshots/profile.jpeg` });
    } catch (err) {
        console.log(`❌ Error: ${err.message}`);
    } finally {
        console.log(`\n🎉 The screenshot has been succesfully generated.`);
    }
}

async function main(){
    let idProfile = '3b9e6faf-72f3-4382-8a76-32688d03e0ff';
    // Bước 1: Khởi động profile
    let startData = await startProfile(idProfile);

    // Bước 2: Lấy webSocketDebuggerUrl
    let connectionInfo = await getBrowserConnectInfo(startData.selenium_remote_debug_address);

    // Bước 3: Kết nối puppeteer với webSocketDebuggerUrl
    captureScreenshot(connectionInfo.webSocketDebuggerUrl);

    // Đóng profile
    stopProfile(idProfile);
}

main()