import re
import time
from playwright.sync_api import Playwright, sync_playwright, expect

def esperar() -> None:
    time.sleep(3.0)

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://the-internet.herokuapp.com/login")
    esperar()
    page.get_by_role("textbox", name="Username").fill("tomsmith")
    esperar()
    page.get_by_role("textbox", name="Password").fill("SuperSecretPassword!")
    esperar()
    page.get_by_role("button", name=" Login").click()
    esperar()
    page.get_by_role("link", name="Logout").click()
    esperar()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
