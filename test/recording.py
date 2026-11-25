import re
from playwright.sync_api import Page, expect


def test_example(page: Page) -> None:
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
    expect(page.get_by_text("Log in to Facebook")).to_be_visible()
    page.get_by_role("textbox", name="Password").click()
    page.get_by_role("textbox", name="Email address or mobile number").click()
    page.get_by_role("link", name="Create new account").click()
    page.get_by_role("textbox", name="Name First name Surname").click()
    page.get_by_role("textbox", name="Name First name Surname").fill("Rishabh")
    page.get_by_role("textbox", name="Surname", exact=True).click()
    expect(page.get_by_role("textbox", name="Name First name Surname There")).to_be_visible()
