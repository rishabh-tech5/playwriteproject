from playwright.sync_api import sync_playwright

URL="https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page=browser.new_page()
    page.goto(URL)
    print("Title",page.title())
    page.wait_for_timeout(5000)
    browser.close