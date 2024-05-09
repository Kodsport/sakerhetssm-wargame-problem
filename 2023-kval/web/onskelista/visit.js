const puppeteer = require('puppeteer');



(async () => {

    const browser = await puppeteer.launch({
        headless: true,
        args: [
          "--no-sandbox",
          "--disable-background-networking",
          "--disk-cache-dir=/dev/null",
          "--disable-default-apps",
          "--disable-extensions",
          "--disable-desktop-notifications",
          "--disable-gpu",
          "--disable-sync",
          "--disable-translate",
          "--disable-dev-shm-usage",
          "--hide-scrollbars",
          "--metrics-recording-only",
          "--mute-audio",
          "--no-first-run",
          "--safebrowsing-disable-auto-update",
          "--window-size=1440,900",
        ],
    });
    const page = await browser.newPage();

    await page.goto("http://localhost:8080/login", {
        waitUntil: "networkidle2",
        timeout: 3000,
    });
    await page.type('input[name="username"]', "admin")
    await page.type('input[name="password"]', "019287430875109438")
    await Promise.all([
        page.click('button[type="submit"]'),
        page.waitForNavigation({
            waitUntil: "networkidle2",
            timeout: 3000,
        })
    ])

    await page.goto(process.argv[2]);
    
    await page.waitForNetworkIdle({
        idleTime: 1000,
        timeout: 10000
    })

    await page.close()

    await browser.close()


})();
