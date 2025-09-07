import re
import time
import traceback
from playwright.sync_api import Playwright, sync_playwright, expect

URL_BASE = "https://www.saucedemo.com/"
USER = "standard_user"
PASS_OK = "secret_sauce"
PASS_BAD = "senha_errada"

def esperar(secs=3.0):
    time.sleep(secs)

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    try:
        # positivo
        page.goto(URL_BASE)
        esperar()
        page.fill("#user-name", USER)
        esperar()
        page.fill("#password", PASS_OK)
        esperar()
        page.click("#login-button")
        esperar()
        expect(page).to_have_url(re.compile(r".*inventory.*"), timeout=10000)
        print("✅ SauceDemo: login positivo OK")
        esperar()

        # logout (abrir menu e clicar logout)
        page.click("#react-burger-menu-btn")
        esperar()
        page.click("#logout_sidebar_link")
        esperar()
        expect(page.locator("#login-button")).to_be_visible(timeout=10000)
        print("✅ SauceDemo: logout OK")
        esperar()

        # negativo
        page.goto(URL_BASE)
        esperar()
        page.fill("#user-name", USER)
        esperar()
        page.fill("#password", PASS_BAD)
        esperar()
        page.click("#login-button")
        esperar()
        erro = page.locator('[data-test="error"]')
        expect(erro).to_be_visible(timeout=10000)
        text = erro.inner_text().strip()
        expected = "Epic sadface: Username and password do not match any user in this service"
        if expected in text:
            print("✅ SauceDemo: fluxo negativo detectou mensagem de erro.")
        else:
            print("❌ SauceDemo: mensagem de erro inesperada:", text)

    except Exception:
        print("❌ Exceção em saucedemo_playwright:")
        print(traceback.format_exc())
    finally:
        context.close()
        browser.close()

if __name__ == "__main__":
    with sync_playwright() as pw:
        run(pw)