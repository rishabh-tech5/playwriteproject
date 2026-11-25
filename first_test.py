import re
from playwright.sync_api import expect,Page
def test_google(page:Page):
    page.goto("https://www.google.com/ncr")

    try:
        page.get_by_role("button",name="Accept all").click(timeout=2000)
    except:
        print("No popup accept")

    page.get_by_role("combobox",name="Search").fill("Playwright Python")

    page.keyboard.press("Enter")

    expect(page).to_have_title(re.compile("Playwright",re.IGNORECASE))
    page.close()