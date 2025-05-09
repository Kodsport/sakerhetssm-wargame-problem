module.exports = {
    timeout: 5000,
    async exec(browser, drinkid, cookie) {
        const page = await browser.newPage();
        await page.setCookie({
            name: "admin",
            value: cookie,
            domain: "localhost:3000",
            httpOnly: true,
            sameSite: "Strict",
        });
        await page.goto("http://localhost:3000/drinks/" + drinkid);
        await page.waitForNetworkIdle({
            timeout: 5000,
        });
        await page.close();
    }
}