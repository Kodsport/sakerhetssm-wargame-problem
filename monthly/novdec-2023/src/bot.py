from urllib import parse
from playwright.sync_api import sync_playwright

cool_css = """font-family: "BlackOpsOne", "sans-serif";"""
cool_css += "background: linear-gradient(45deg, rgba(255,226,91,1) 0%, rgba(255,83,83,1) 47%, rgba(212,37,255,1) 100%);"
cool_css += "color: white;"


def parse_query(url):
    query = parse.parse_qs(parse.urlparse(url).query)

    if not all(key in query for key in ["content", "image", "text"]):
        return None

    content = f"Flaggan är {open('flag.txt', 'r').read()}. {query['content'][0]}"
    image = query["image"][0]
    text = query["text"][0]
    title = "Flaggkebaben"

    return (title, text, image, content)


def playwright_bot(url, secret_token):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        c = browser.new_context()
        c.route(
            "**/*",
            lambda route: route.continue_()
            if route.request.url.startswith("http://127.0.0.1:5000/")
            else route.abort(),
        )

        page = c.new_page()
        page.goto("http://127.0.0.1:5000/", wait_until="networkidle")
        page.locator("#theme").click()
        page.wait_for_timeout(133.7)

        theme_page = c.pages[1]
        theme_page.locator("#css").fill(cool_css)
        theme_page.locator("#secret").fill(secret_token)
        theme_page.locator("#submit-admin-theme").click()
        theme_page.locator("#secret").fill("")

        page.goto(url, wait_until="networkidle")

        # Check out this cool syntax
        if not (params := parse_query(url)):
            return {"msg": "Inte bra url!"}

        (title, text, image, content) = params
        new_page = c.new_page()
        new_page.goto(
            f"http://127.0.0.1:5000/view?title={title}&text={text}&image={image}&content={content}",
            wait_until="networkidle",
        )
        admin_kebab = new_page.screenshot()
        user_kebab = page.screenshot()

        c.close()
        return (
            {"msg": "Kebabteknikern älskade din kebab!"}
            if admin_kebab < user_kebab
            else {"msg": "Kebabteknikern hatade din kebab!"}
        )
